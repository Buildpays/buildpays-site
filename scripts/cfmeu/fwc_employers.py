#!/usr/bin/env python3
"""Build data/cfmeu-employers.json from the Fair Work Commission's published agreement lists.

The Commission publishes a spreadsheet of every enterprise agreement it approves each
year (fwc.gov.au/documents/agreements/resources/agreementsYYYY.xlsx). Every agreement
made with the CFMEU's Victorian Construction and General Division is titled
"<Employer> and the CFMEU (Victorian Construction and General Division) <Trade>
Enterprise Agreement 2024 - 2027", so the lists give a verifiable, dated register of
which companies have a CFMEU Victorian construction EBA in force. No figure on the site
comes from this file; it feeds the employer list on the "CFMEU EBA jobs" guide only.

Run from the repo root:

    python scripts/cfmeu/fwc_employers.py                # rebuild the JSON from the live lists
    python scripts/cfmeu/fwc_employers.py --offline DIR  # read agreementsYYYY.xlsx from DIR
    python scripts/cfmeu/fwc_employers.py --publish      # in CI: rebuild, regenerate the guides,
                                                         # commit and push if the list changed

Gates before a publish: at least MIN_ROWS employers, the count within 0.7x-1.3x of the
previous list, and every year's file parsed. A failed gate opens a GitHub issue.
"""
import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from collections import OrderedDict
from datetime import date, datetime

import openpyxl
import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "cfmeu-employers.json")
LIST_URL = "https://www.fwc.gov.au/documents/agreements/resources/agreements{year}.xlsx"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36 PayKicker-figures-watch",
      "Accept": "*/*", "Accept-Language": "en-AU,en;q=0.9"}
MIN_ROWS = 300
DIVISION = re.compile(r"CFMEU[\s,]*\(?\s*Victorian\s*Construction\s*(and\s*|&\s*)?General\s*Division", re.I)  # titles vary: 'CFMEU,(Victorian', 'Construction General'
YEARS_BACK = 3  # the 2024-2027 agreements were first approved in 2023; older lists cannot hold a current one


def log(*a):
    print("[fwc-employers]", *a, flush=True)


# ---------------------------------------------------------------- title parsing

SEP = re.compile(r"\s*(?:,|and\s*the|and|&\s*the|&|/)?\s*(?:the\s*)?CFMEU\b", re.I)  # no word boundary before 'and': 'PTY LTDand the CFMEU' occurs


def employer_from(title):
    t = re.sub(r"^\s*Application for approval of the\s+", "", title, flags=re.I)
    return re.sub(r"\s+", " ", SEP.split(t, 1)[0]).strip(" ,-–")


TRADE_FIX = [
    (r"Sub-?\s*con-?\s*tractors\s*", "Subcontractors "),
    (r"Concrete Sawing\s*and\s*Drilling", "Concrete Sawing and Drilling"),
    (r"Asphalt\s*&\s*Linemarking", "Asphalt & Linemarking"),
    (r"^Rail Corridor Mobile Crane Hiring Industry$", "Mobile Crane Hiring Industry"),
    (r"Non\s*-?\s*Destructive\s*Digg(er|ing)\b.*", "Non-Destructive Digging"),
    (r"Earth-?\s*moving,?\s*Excavation\s*(and|&)\s*Drainage", "Earthmoving, Excavation and Drainage"),
    (r"Carpentry\s*(and|&)\s*Joinery", "Carpentry & Joinery"),
    (r"Painting\s*(and|&)\s*Decorating", "Painting & Decorating"),
    (r"Caulking\s*(and|&)\s*Sealing", "Caulking & Sealing"),
    (r"Cladding\s*(and|&)\s*Fa\S*ade", "Cladding & Facade"),
    (r"Architectural Features\s*(and|&)\s*Fittings", "Architectural Features & Fittings"),
    (r"Concrete Kerb.*", "Concrete Kerb, Channel & Pavement"),
    (r"Signage\s*(and|&)\s*Sign Writers", "Signage & Sign Writers"),
    (r"Steel\s*fixing", "Steelfixing"),
    (r"Brick\s*laying", "Bricklaying"),
    (r"Self-?\s*Propelled Modular Transporter.*", "Self-Propelled Modular Transporter (SPMT)"),
    (r"Rigger\s*(and|&)\s*Gantry.*", "Rigger & Gantry Crane"),
    (r"Builder\s+Enter-?\s*prise", "Builder"),
    (r"^Commercial Pool Builder$", "Subcontractors Commercial Pool Builder"),
    (r"^(Onsite Shopfitters|Subcontractors Shopfitters Onsite)$", "Subcontractors Onsite Shopfitters"),
    (r"^Subcontractors Cladding Installation$", "Subcontractors Cladding & Facade"),
    (r"^Subcontractors Solid Plastering$", "Subcontractors Plastering"),
    (r"^Subcontractors Structural Remedial Concrete$", "Subcontractors Remedial Concrete and Access Flooring"),
    (r"^Subcontractors Onsite Precast Panel Installation$", "Subcontractors Precast Panel"),
    (r"^Subcontractors Civil and Infrastructure$", "Civil & Infrastructure"),
    (r"^Civil Infrastructure Subcontractors Formwork$", "Subcontractors Formwork"),
    (r"^Subcontractors Specialist Signage$", "Subcontractors Signage & Sign Writers"),
    (r"^Subcontractors Traffic Control Indigenous.*", "Subcontractors Traffic Control"),
    (r"^Subcontractors Civil Line Marker.*", "Subcontractors Traffic Control"),
]
STRIP = re.compile(r"\s*(Greenfields|Indigenous Employment\s*(and|&)\s*Training|Indigenous|Enterprise|Employment\s*(and|&)\s*Training)\s*$", re.I)


def trade_from(title):
    m = re.search(r"Division\)\s*(.*?)\s*(Enterprise\s+)?(Collective\s+)?Agreement\b", title, re.I | re.S)
    t = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    t = re.sub(r"^\S.*?Project\s+(?=Subcontractors)", "", t)  # 'Spark - North East Link Project Subcontractors ...'
    for pat, rep in TRADE_FIX:
        t = re.sub(pat, rep, t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip()
    while True:
        t2 = STRIP.sub("", t).strip()
        if t2 == t:
            break
        t = t2
    t = re.sub(r"Subcontractors(?=[A-Z])", "Subcontractors ", t)
    return t


SECTOR_OF = {  # display sector for the guide, in the order the page shows them
    "": "Head contractors and builders",  # '<Builder> and the CFMEU (...) Enterprise Agreement 2024-2027': no trade in the title
    "Builder": "Head contractors and builders",
    "Subcontractors Labour Hire": "Labour hire",
    "Subcontractors Formwork": "Formwork",
    "Subcontractors Steelfixing": "Steelfixing",
    "Subcontractors Concrete Placement": "Concrete placement",
    "Subcontractors Concrete Pumping": "Concrete pumping",
    "Subcontractors Post-Tensioning": "Post-tensioning",
    "Subcontractors Precast Panel": "Precast panels",
    "Subcontractors Carpentry & Joinery": "Carpentry and joinery",
    "Subcontractors Onsite Shopfitters": "Shopfitting",
    "Subcontractors Bricklaying": "Bricklaying",
    "Subcontractors Plastering": "Plastering",
    "Subcontractors Tilelayer": "Tiling",
    "Subcontractors Painting & Decorating": "Painting and decorating",
    "Subcontractors Industrial Painting": "Painting and decorating",
    "Subcontractors Cladding & Facade": "Cladding and facades",
    "Subcontractors Aluminium & Glass": "Aluminium and glass",
    "Subcontractors Caulking & Sealing": "Caulking and sealing",
    "Subcontractors Waterproofing": "Waterproofing",
    "Subcontractors Passive Fire": "Passive fire",
    "Subcontractors Safety Systems": "Safety systems and barriers",
    "Subcontractors Safety Barrier Installation": "Safety systems and barriers",
    "Subcontractors Contract Scaffolding": "Scaffolding",
    "Subcontractors Scaffold Yard": "Scaffolding",
    "Subcontractors Mast Climbing Access Equipment": "Hoists and mast climbers",
    "Subcontractors Rigger/Steel Erector": "Rigging and steel erection",
    "Subcontractors Tower Crane Riggers": "Tower crane riggers",
    "Subcontractors Rigger & Gantry Crane": "Rigging and steel erection",
    "Mobile Crane Hiring Industry": "Mobile crane hire",
    "Subcontractors Self-Propelled Modular Transporter (SPMT)": "Heavy haulage (SPMT)",
    "Specialised Rope Access": "Rope access",
    "Subcontractors Earthmoving, Excavation and Drainage": "Earthmoving, excavation and drainage",
    "Subcontractors Non-Destructive Digging": "Non-destructive digging",
    "Non-Destructive Digging": "Non-destructive digging",
    "Subcontractors Ground Services Locating": "Non-destructive digging",
    "Subcontractors Piling": "Piling",
    "Subcontractors Directional Drilling": "Directional drilling",
    "Subcontractors Rockbreaker": "Rockbreaking",
    "Civil & Infrastructure": "Civil and infrastructure",
    "Subcontractors Concrete Kerb, Channel & Pavement": "Kerb, channel and pavement",
    "Asphalt & Linemarking": "Asphalt and line marking",
    "Subcontractors Traffic Control": "Traffic control",
    "Subcontractors Fencing": "Fencing",
    "Subcontractors Landscape Construction": "Landscape construction",
    "Subcontractors Landscape Furniture Installation": "Landscape construction",
    "Subcontractors Onsite Arboriculture": "Landscape construction",
    "Subcontractors Demolition": "Demolition",
    "Subcontractors Asbestos Removal": "Asbestos removal",
    "Subcontractors Concrete Sawing and Drilling": "Concrete sawing and drilling",
    "Subcontractors Remedial Concrete and Access Flooring": "Remedial concrete and access flooring",
    "Subcontractors Marking and Setting Out": "Marking and setting out",
    "Architectural Features & Fittings": "Architectural features and fittings",
    "Subcontractors Architectural Features & Fittings": "Architectural features and fittings",
    "Subcontractors Signage & Sign Writers": "Signage",
    "Subcontractors Cleaning": "Site cleaning",
    "Subcontractors Site Amenities Installation": "Site amenities",
    "Subcontractors Coolroom Builder": "Coolrooms and saunas",
    "Subcontractors Coolroom and Sauna Builder": "Coolrooms and saunas",
    "Subcontractors Commercial Pool Builder": "Commercial pools",
    "Subcontractors Wind Turbine Erection": "Wind turbine erection",
    "Industrial Services": "Industrial services",
}
OTHER = "Other agreements"


# ---------------------------------------------------------------- employer name tidy

SMALL = {"and", "of", "the", "for", "as", "at", "by", "in", "on", "to", "a", "an"}
KEEP_UPPER = {"PTY", "LTD"}  # handled below; listed so the loop skips the vowel test


def tidy_word(w, first):
    core = re.sub(r"[^A-Za-z]", "", w)
    if not core:
        return w
    low = core.lower()
    if low == "pty":
        return w.replace(core, "Pty")
    if low == "ltd":
        return w.replace(core, "Ltd")
    if low == "t/as" or w.upper() in ("T/AS", "T/A"):
        return w.replace(core, core.lower()).replace("T/", "t/")
    if low in SMALL and not first:
        return w.replace(core, low)
    if len(core) <= 4 and not re.search(r"[AEIOUaeiou]", core):
        return w  # consonant-only short word: an initialism (HRV, JCO, ATF, NSW)
    if len(core) <= 2:
        return w
    return w.replace(core, core[0].upper() + core[1:].lower())


def tidy_name(name):
    if re.search(r"[a-z]", re.sub(r"\bT/As?\b|\bPty\.?\b|\bLtd\.?\b", "", name)):
        return name  # already mixed case, as registered
    words = name.split(" ")
    out = []
    for i, w in enumerate(words):
        if "/" in w and w.upper() not in ("T/AS", "T/A"):
            out.append("/".join(tidy_word(p, i == 0) for p in w.split("/")))
        elif "-" in w:
            out.append("-".join(tidy_word(p, i == 0) for p in w.split("-")))
        else:
            out.append(tidy_word(w, i == 0))
    s = " ".join(out)
    s = re.sub(r"\(the Trustee For\)", "(The Trustee For)", s, flags=re.I)
    return s


def polish(name):
    """Applied to every name, tidied or as registered: t/as, Pty Ltd and Pty Limited in one style."""
    name = re.sub(r"\bT/AS?\b", lambda m: m.group(0).lower(), name, flags=re.I)
    name = re.sub(r"\bPTY\.?\s+LTD\.?", "Pty Ltd", name, flags=re.I)
    name = re.sub(r"\bPTY\.?\s+LIMITED\b", "Pty Limited", name, flags=re.I)
    name = re.sub(r"\s*&\s*", " & ", name)
    return name.replace("�", "'")  # the Commission's export drops the odd apostrophe


# ---------------------------------------------------------------- fetch + parse

def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_year(year, offline):
    if offline:
        p = os.path.join(offline, f"agreements{year}.xlsx")
        if not os.path.exists(p):
            return None, None
        data = open(p, "rb").read()
    else:
        r = requests.get(LIST_URL.format(year=year), headers=UA, timeout=120)
        if r.status_code == 404:
            return None, None
        r.raise_for_status()
        data = r.content
        if not data.startswith(b"PK"):
            raise RuntimeError(f"agreements{year}.xlsx is not a spreadsheet (bot challenge?)")
    wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True)
    ws = wb[wb.sheetnames[0]]
    rows, generated = [], None
    for row in ws.iter_rows(values_only=True):
        if not row or not row[0]:
            continue
        if isinstance(row[0], str) and row[0].startswith("List of Agreements"):
            m = re.search(r"Report generated on (\d{1,2} \w+ \d{4})", row[0])
            if m:
                generated = datetime.strptime(m.group(1), "%d %B %Y").date().isoformat()
            continue
        title = row[0] if isinstance(row[0], str) else None
        if not title or not isinstance(row[1], str) or not row[1].startswith("AE"):
            continue
        op, ex = row[6], row[7]
        if not isinstance(op, datetime) or not isinstance(ex, datetime):
            continue
        rows.append(dict(title=re.sub(r"\s+", " ", title).strip(), id=row[1], industry=row[5] or "",
                         operative=op.date().isoformat(), expiry=ex.date().isoformat()))
    return dict(year=year, url=LIST_URL.format(year=year), sha256=sha(data), generated=generated, rows=len(rows)), rows


def build(offline=None, today=None):
    today = today or date.today()
    files, current = [], {}
    for year in range(today.year - YEARS_BACK, today.year + 1):
        meta, rows = load_year(year, offline)
        if meta is None:
            log(f"agreements{year}.xlsx: not available")
            continue
        files.append(meta)
        n = 0
        for r in rows:
            if not DIVISION.search(r["title"]):
                continue
            if (today - date.fromisoformat(r["expiry"])).days > 365:
                continue  # an agreement keeps operating past its nominal expiry until replaced; keep a year of grace, flagged
            emp = employer_from(r["title"])
            trade = trade_from(r["title"])
            sector = SECTOR_OF.get(trade, OTHER)
            if sector == OTHER:
                log("unmapped trade:", trade or "(blank)", "|", r["title"][:90])
            key = (re.sub(r"[^a-z0-9]", "", emp.lower()), sector)
            rec = dict(name=polish(tidy_name(emp)), sector=sector, trade=trade, agreement_id=r["id"], operative=r["operative"], expiry=r["expiry"],
                       nominal_expiry_passed=date.fromisoformat(r["expiry"]) < today)
            if key not in current or current[key]["operative"] < rec["operative"]:
                current[key] = rec
            n += 1
        log(f"agreements{year}.xlsx: {meta['rows']} agreements, {n} current CFMEU Victorian C&G, report generated {meta['generated']}")
    if not files:
        raise RuntimeError("no FWC list could be read")
    order = list(OrderedDict.fromkeys(SECTOR_OF.values())) + [OTHER]
    sectors = OrderedDict()
    for s in order:
        items = sorted((r for r in current.values() if r["sector"] == s), key=lambda r: re.sub(r"^(the )", "", r["name"].lower()))
        if items:
            sectors[s] = [dict(name=r["name"], agreement_id=r["agreement_id"], operative=r["operative"], expiry=r["expiry"],
                               nominal_expiry_passed=r["nominal_expiry_passed"]) for r in items]
    return dict(
        _comment="Employers with a CFMEU (Victorian Construction and General Division) enterprise agreement in force, from the Fair Work Commission's yearly lists of approved agreements. Built by scripts/cfmeu/fwc_employers.py; do not edit by hand.",
        as_at=today.isoformat(),
        list_generated=max(f["generated"] for f in files if f["generated"]),
        source_url="https://www.fwc.gov.au/work-conditions/enterprise-agreements/find-enterprise-agreement",
        search_url="https://www.fwc.gov.au/document-search?search-ui=agreements",
        files=files,
        count=sum(len(v) for v in sectors.values()),
        sectors=sectors,
    )


# ---------------------------------------------------------------- gates, diff, publish

def names(d):
    return {(s, r["name"], r["agreement_id"]) for s, v in d.get("sectors", {}).items() for r in v}


def validate(new, old):
    problems = []
    if new["count"] < MIN_ROWS:
        problems.append(f"only {new['count']} employers found (minimum {MIN_ROWS})")
    if old and old.get("count"):
        ratio = new["count"] / old["count"]
        if not 0.7 <= ratio <= 1.3:
            problems.append(f"count moved from {old['count']} to {new['count']} ({ratio:.2f}x); outside 0.7x-1.3x")
    if any(f["rows"] == 0 for f in new["files"]):
        problems.append("a yearly list parsed to zero agreements")
    return problems


def sh(*cmd, check=True):
    log("$", " ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT, check=check, text=True, capture_output=True)


def open_issue(title, body):
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo or not os.environ.get("GH_TOKEN"):
        log("ISSUE (no GH_TOKEN, printing instead):", title, "\n", body)
        return
    sh("gh", "issue", "create", "-R", repo, "-t", title, "-b", body, "-l", "cfmeu-figures", check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", help="directory holding agreementsYYYY.xlsx files")
    ap.add_argument("--publish", action="store_true", help="CI: regenerate, commit and push when the list changed")
    ap.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    old = json.load(io.open(OUT, encoding="utf-8")) if os.path.exists(OUT) else None
    try:
        new = build(args.offline)
    except Exception as e:
        if args.publish:
            open_issue("CFMEU employers: list rebuild errored", f"Error: `{type(e).__name__}: {e}`\n\nNothing was published.")
        log("ERROR:", repr(e))
        return 1

    added = sorted(names(new) - names(old)) if old else []
    removed = sorted(names(old) - names(new)) if old else []
    log(f"{new['count']} employers in {len(new['sectors'])} sectors; FWC lists generated up to {new['list_generated']}")
    if old and not added and not removed:
        log("changed: nothing")
        return 0
    if old:
        log(f"added {len(added)}, removed {len(removed)}")
    for s, n, i in added[:40]:
        log("  +", s, "|", n, i)
    for s, n, i in removed[:40]:
        log("  -", s, "|", n, i)

    problems = validate(new, old)
    if problems:
        body = "The Fair Work Commission list parsed but failed the sanity gates:\n\n" + "\n".join(f"- {p}" for p in problems) + "\n\nNothing was published."
        if args.publish:
            open_issue("CFMEU employers: list failed sanity gates", body)
        log("GATES FAILED:\n" + body)
        return 1
    if args.dry_run:
        return 0

    json.dump(new, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    log("wrote", os.path.relpath(OUT, ROOT))
    if not args.publish:
        return 0

    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "cfmeu", "build_guides.py")], cwd=ROOT, text=True, capture_output=True)
    if r.returncode != 0:
        open_issue("CFMEU employers: page build failed", r.stdout + "\n" + r.stderr)
        return 1
    summary = f"{new['count']} employers (was {old['count'] if old else 'none'}); {len(added)} added, {len(removed)} removed. FWC lists generated up to {new['list_generated']}."
    detail = "\n".join(f"- + {s}: {n} ({i})" for s, n, i in added[:60]) + ("\n" if added and removed else "") + "\n".join(f"- − {s}: {n} ({i})" for s, n, i in removed[:60])
    sh("git", "config", "user.name", "paykicker-figures-bot")
    sh("git", "config", "user.email", "operations@paykicker.com.au")
    sh("git", "add", "data", "public")
    sh("git", "commit", "-m", f"CFMEU employers: refresh from the FWC lists\n\n{summary}\n\nAutomated by scripts/cfmeu/fwc_employers.py; gates passed.")
    sh("git", "push")
    open_issue("CFMEU employer list updated and published", summary + "\n\n" + detail + "\n\nPublished to main automatically; Cloudflare Pages deploys it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
