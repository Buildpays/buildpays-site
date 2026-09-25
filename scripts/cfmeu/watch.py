#!/usr/bin/env python3
"""Watch the CFMEU Victoria wage sheets and republish the guides when they change.

Run by .github/workflows/cfmeu-figures.yml (weekly, and by hand). Steps:

1. Fetch vic.cfmeu.org/wages and /rdo-calendars, find the current sheet links.
2. Download each sheet and hash it. Compare with data/cfmeu-sources.json.
3. Nothing changed -> exit 0.
4. Something changed -> extract the new figures (Claude reads the PDF text into a
   fixed JSON schema; the RDO ICS is parsed directly), then run the sanity gates:
   every key present, every figure within a plausible band of the previous one,
   weekly = hourly x 36, dates parse and never go backwards.
5. Gates pass -> write data/cfmeu-figures.json, regenerate the pages, commit and push
   (Cloudflare Pages deploys main). Any gate fails -> open a GitHub issue with the
   details and publish nothing.

Environment: ANTHROPIC_API_KEY (extraction), GH_TOKEN (issue + push), GITHUB_REPOSITORY.
Flags: --dry-run (no write, no push, no issue), --force (treat every sheet as changed),
       --offline DIR (read sheets from files in DIR instead of downloading).
"""
import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta

import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FIG = os.path.join(ROOT, "data", "cfmeu-figures.json")
SRC = os.path.join(ROOT, "data", "cfmeu-sources.json")
BASE = "https://vic.cfmeu.org"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36 PayKicker-figures-watch",
      "Accept": "text/html,application/xhtml+xml,application/pdf,text/calendar,*/*;q=0.8", "Accept-Language": "en-AU,en;q=0.9"}
MODEL = "claude-opus-5"

# What we look for on the union's pages. Each entry: label, page, link regex (case-insensitive).
SHEETS = {
    "wages": ("/wages", r'href="([^"]*Onsite-EBA-Rates[^"]*\.pdf)"'),
    "allowances": ("/wages", r'href="([^"]*Onsite-Allowances[^"]*\.pdf)"'),
    "site_allowance": ("/wages", r'href="([^"]*Site-Allowance[^"]*\.pdf)"'),
    "rdo_ics": ("/rdo-calendars/", r'href="([^"]*36hr-onsite-rdo-calendar[^"]*\.ics)"'),
}


def log(*a):
    print("[cfmeu-watch]", *a, flush=True)


def fetch(url):
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    body = r.content
    if url.lower().endswith((".pdf", ".ics")) and body.lstrip()[:15].lower().startswith((b"<!doctype", b"<html")):
        raise RuntimeError(f"{url} returned an HTML page instead of the file (bot challenge?)")
    if url.lower().endswith(".pdf") and not body.startswith(b"%PDF"):
        raise RuntimeError(f"{url} is not a PDF")
    return body


def find_links(offline):
    links = {}
    for key, (page, pat) in SHEETS.items():
        if offline:
            for f in os.listdir(offline):
                if f.startswith(key + "."):
                    links[key] = os.path.join(offline, f)
            continue
        html = fetch(BASE + page).decode("utf-8", "replace")
        found = re.findall(pat, html, re.I)
        if not found:
            raise RuntimeError(f"no link for {key} on {page}")
        # newest upload path wins (they are /uploads/YYYY/MM/...)
        url = sorted(set(found))[-1]
        links[key] = url if url.startswith("http") else BASE + url
    return links


def load(path, default):
    return json.load(io.open(path, encoding="utf-8")) if os.path.exists(path) else default


def pdf_text(data):
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(data))
    return "\n\n".join((p.extract_text() or "") for p in reader.pages)


# ---------------------------------------------------------------- extraction

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["wages", "allowances", "site_allowance"],
    "properties": {
        "wages": {
            "type": "object", "additionalProperties": False,
            "required": ["source_title", "rates_from", "cw3_hour", "cw3_week", "cw2_hour", "cw2_week", "cw1_hour", "cw1_week",
                         "benefits_from", "travel_daily", "super_weekly", "super_pct", "incolink_weekly", "ot_meal", "laha_week", "laha_day", "overnight"],
            "properties": {
                "source_title": {"type": "string", "description": "The sheet's title as printed, e.g. '2026 EBA Wages, On-Site Construction 36 Hour Week'"},
                "rates_from": {"type": "string", "description": "ISO date the hourly rates begin on/after"},
                "cw3_hour": {"type": "string", "description": "CW3 100% Carpenter/Joiner row, rate per hour, e.g. '62.21'"},
                "cw3_week": {"type": "string", "description": "CW3 100% Carpenter/Joiner row, rate per week"},
                "cw2_hour": {"type": "string", "description": "Labourers CW2 96% Grade 2 (Scaffolder, Steel Fixer, Concrete Finisher) rate per hour"},
                "cw2_week": {"type": "string"},
                "cw1_hour": {"type": "string", "description": "Labourers CW1 92.4% Grade 3 (Trades Labourer, Concrete Gang) rate per hour"},
                "cw1_week": {"type": "string"},
                "benefits_from": {"type": "string", "description": "ISO date the 'other EBA benefits' begin on/after"},
                "travel_daily": {"type": "string", "description": "Travel allowance per day"},
                "super_weekly": {"type": "string", "description": "Superannuation dollars per week (the fixed figure)"},
                "super_pct": {"type": "string", "description": "Superannuation percentage of ordinary time earnings, digits only"},
                "incolink_weekly": {"type": "string"},
                "ot_meal": {"type": "string", "description": "Overtime meal allowance"},
                "laha_week": {"type": "string", "description": "Living away from home allowance per week"},
                "laha_day": {"type": "string", "description": "Living away from home allowance per day"},
                "overnight": {"type": "string", "description": "Additional overnight allowance per night"},
            },
        },
        "allowances": {
            "type": "object", "additionalProperties": False,
            "required": ["source_title", "correct_at", "multistorey_1_15", "multistorey_16_30", "multistorey_31_45", "multistorey_46_60", "multistorey_61_plus",
                         "leading_hand_1", "leading_hand_2_5", "leading_hand_6_10", "leading_hand_11_plus", "own_vehicle_transfer_km", "own_vehicle_outside_km",
                         "wet_dirty_cold", "hot_46_54", "hot_over_54", "confined_space", "explosive_tool_day", "demolition_direct", "demolition_alongside"],
            "properties": {
                "source_title": {"type": "string", "description": "e.g. 'On-Site EBA Allowances 01-03-2026'"},
                "correct_at": {"type": "string", "description": "ISO date the sheet says the rates are correct at"},
                "multistorey_1_15": {"type": "string"}, "multistorey_16_30": {"type": "string"}, "multistorey_31_45": {"type": "string"},
                "multistorey_46_60": {"type": "string"}, "multistorey_61_plus": {"type": "string"},
                "leading_hand_1": {"type": "string"}, "leading_hand_2_5": {"type": "string"}, "leading_hand_6_10": {"type": "string"}, "leading_hand_11_plus": {"type": "string"},
                "own_vehicle_transfer_km": {"type": "string", "description": "Own vehicle allowance per km when transferring between sites during working hours"},
                "own_vehicle_outside_km": {"type": "string", "description": "Own vehicle allowance per km to a job outside the required work boundaries"},
                "wet_dirty_cold": {"type": "string", "description": "Wet work per hour (same as dirty work and cold work)"},
                "hot_46_54": {"type": "string"}, "hot_over_54": {"type": "string"}, "confined_space": {"type": "string"},
                "explosive_tool_day": {"type": "string"}, "demolition_direct": {"type": "string"}, "demolition_alongside": {"type": "string"},
            },
        },
        "site_allowance": {
            "type": "object", "additionalProperties": False,
            "required": ["source_title", "applies_from", "cpi_pct", "threshold_m", "inner_cap_m", "inner_new", "inner_reno", "bands", "projects"],
            "properties": {
                "source_title": {"type": "string"},
                "applies_from": {"type": "string", "description": "ISO date the figures apply from"},
                "cpi_pct": {"type": "string", "description": "CPI increase percentage, digits only"},
                "threshold_m": {"type": "string", "description": "Lowest project value in $ million that attracts site allowance, e.g. '6.2'"},
                "inner_cap_m": {"type": "string", "description": "Upper project value in $ million for the Melbourne inner suburbs flat rate, e.g. '315.6'"},
                "inner_new": {"type": "string", "description": "Melbourne inner suburbs and shopping centres, new projects, $ per hour"},
                "inner_reno": {"type": "string", "description": "Renovations, restorations and refurbishments, $ per hour"},
                "bands": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["lo_m", "hi_m", "rate"],
                          "properties": {"lo_m": {"type": "string"}, "hi_m": {"type": "string"}, "rate": {"type": "string"}}},
                          "description": "New projects elsewhere table, in order, values in $ million and $ per hour"},
                "projects": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["name", "rate"],
                             "properties": {"name": {"type": "string"}, "rate": {"type": "string"}}},
                             "description": "Project specific allowance rates"},
            },
        },
    },
}

SYSTEM = (
    "You extract figures from CFMEU Victoria wage sheets into a fixed JSON schema for a payroll reference page. "
    "Copy every number exactly as printed, as a decimal string with no dollar sign, commas or units. "
    "Dates are ISO (YYYY-MM-DD); a sheet titled '01-03-2026' means 1 March 2026 and 'begin on/after 1 February 2026' is 2026-02-01. "
    "Never estimate, round or infer a figure that is not printed; if a required figure is genuinely absent from the text, write the string 'MISSING' for it. "
    "The three documents are separated by headings that name them."
)


def extract(texts):
    import anthropic
    client = anthropic.Anthropic()
    user = "\n\n".join(f"===== DOCUMENT: {k} =====\n{v}" for k, v in texts.items())
    kwargs = dict(model=MODEL, max_tokens=16000, system=SYSTEM,
                  messages=[{"role": "user", "content": user}],
                  output_config={"format": {"type": "json_schema", "schema": SCHEMA}})
    try:
        resp = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs)
    except anthropic.BadRequestError:
        resp = client.messages.create(**kwargs)
    if resp.stop_reason == "refusal":
        raise RuntimeError("extraction refused: " + str(getattr(resp, "stop_details", None)))
    text = next(b.text for b in resp.content if b.type == "text")
    return json.loads(text)


# ---------------------------------------------------------------- RDO ICS

def parse_ics(data):
    text = data.decode("utf-8", "replace").replace("\r\n", "\n").replace("\n ", "")
    events = []
    for block in text.split("BEGIN:VEVENT")[1:]:
        m_d = re.search(r"DTSTART(?:;[^:\n]*)?:(\d{8})", block)
        m_s = re.search(r"SUMMARY(?:;[^:\n]*)?:(.*)", block)
        if m_d and m_s:
            d = m_d.group(1)
            events.append((f"{d[:4]}-{d[4:6]}-{d[6:]}", m_s.group(1).strip()))
    years = {}
    for iso, summ in sorted(events):
        y = years.setdefault(iso[:4], {"rdo": [], "public_holidays": [], "annual_leave": [], "lockdown_weekends": [], "other": []})
        s = summ.lower()
        if "rostered day off" in s or s == "rdo":
            y["rdo"].append(iso)
        elif "annual leave" in s:
            y["annual_leave"].append(iso)
        elif "lockdown" in s:
            y["lockdown_weekends"].append(iso)
        elif "public holiday" in s or any(k in s for k in ("new year", "australia day", "anzac", "christmas", "boxing", "labour day", "cup day", "easter", "good friday", "king", "queen")):
            name = re.sub(r"\s*-?\s*public holiday\s*", "", summ, flags=re.I).strip() or "Public holiday"
            y["public_holidays"].append({"date": iso, "name": name})
        elif "branch meeting" in s or "women" in s or "remembrance" in s:
            continue
        else:
            y["other"].append({"date": iso, "name": summ})
    return years


# ---------------------------------------------------------------- gates

class Gate(Exception):
    pass


def num(s):
    try:
        return float(str(s).replace(",", ""))
    except ValueError:
        raise Gate(f"not a number: {s!r}")


def iso(s):
    try:
        return date.fromisoformat(s)
    except ValueError:
        raise Gate(f"not an ISO date: {s!r}")


def check_num(path, new, old, lo=0.5, hi=1.5):
    n = num(new)
    if new == "MISSING":
        raise Gate(f"{path} missing from the sheet")
    if old is not None:
        o = num(old)
        if o > 0 and not (lo * o <= n <= hi * o):
            raise Gate(f"{path} = {n} is outside {lo}x to {hi}x the previous {o}")
    if n < 0:
        raise Gate(f"{path} negative")


def check_date(path, new, old):
    d = iso(new)
    if old is not None and d < iso(old):
        raise Gate(f"{path} {new} is earlier than the previous {old}")
    if d > date.today() + timedelta(days=200):
        raise Gate(f"{path} {new} is more than 200 days in the future")


def keep_title(new_title, old_title):
    """Sheet titles are printed in capitals; keep our typeset title unless the words changed."""
    norm = lambda t: re.sub(r"[^a-z0-9]", "", str(t).lower())
    if old_title and norm(new_title) == norm(old_title):
        return old_title
    words = []
    for w in str(new_title).split():
        words.append(w if (w.isupper() and len(w) <= 5) or w[:1].isdigit() else w.capitalize())
    return " ".join(words)


def validate(new, old, changed):
    """Compare every figure with the previous JSON. Only sections whose sheet changed are re-read;
    the others are copied from the old file so an unchanged sheet can never drift."""
    out = json.loads(json.dumps(old))
    if "wages" in changed:
        w, ow = new["wages"], old["wages"]
        for k in ("cw3_hour", "cw3_week", "cw2_hour", "cw2_week", "cw1_hour", "cw1_week", "travel_daily", "super_weekly", "incolink_weekly", "ot_meal", "laha_week", "laha_day", "overnight"):
            check_num("wages." + k, w[k], ow.get(k))
        check_num("wages.super_pct", w["super_pct"], ow.get("super_pct"), 0.8, 1.3)
        for k in ("cw3", "cw2", "cw1"):
            if abs(num(w[k + "_hour"]) * 36 - num(w[k + "_week"])) > 0.05:
                raise Gate(f"wages.{k}: weekly {w[k+'_week']} is not 36 x hourly {w[k+'_hour']}")
        if not (num(w["cw1_hour"]) < num(w["cw2_hour"]) < num(w["cw3_hour"])):
            raise Gate("wages: CW1 < CW2 < CW3 ordering broken")
        check_date("wages.rates_from", w["rates_from"], ow.get("rates_from"))
        check_date("wages.benefits_from", w["benefits_from"], ow.get("benefits_from"))
        out["wages"].update({k: w[k] for k in SCHEMA["properties"]["wages"]["required"]})
        out["wages"]["source_title"] = keep_title(w["source_title"], ow.get("source_title"))
    if "allowances" in changed:
        a, oa = new["allowances"], old["allowances"]
        for k in SCHEMA["properties"]["allowances"]["required"]:
            if k in ("source_title", "correct_at"):
                continue
            check_num("allowances." + k, a[k], oa.get(k))
        ms = [num(a[k]) for k in ("multistorey_1_15", "multistorey_16_30", "multistorey_31_45", "multistorey_46_60", "multistorey_61_plus")]
        if ms != sorted(ms):
            raise Gate("allowances: multi-storey bands not increasing")
        check_date("allowances.correct_at", a["correct_at"], oa.get("correct_at"))
        out["allowances"].update({k: a[k] for k in SCHEMA["properties"]["allowances"]["required"]})
        out["allowances"]["source_title"] = keep_title(a["source_title"], oa.get("source_title"))
    if "site_allowance" in changed:
        s, os_ = new["site_allowance"], old["site_allowance"]
        for k in ("threshold_m", "inner_cap_m", "inner_new", "inner_reno"):
            check_num("site_allowance." + k, s[k], os_.get(k))
        check_num("site_allowance.cpi_pct", s["cpi_pct"], None)
        if not (0 <= num(s["cpi_pct"]) <= 15):
            raise Gate("site_allowance.cpi_pct implausible")
        if len(s["bands"]) < 5:
            raise Gate("site_allowance: fewer than 5 value bands")
        rates = [num(b["rate"]) for b in s["bands"]]
        if rates != sorted(rates):
            raise Gate("site_allowance: band rates not increasing")
        for i, b in enumerate(s["bands"]):
            if num(b["lo_m"]) >= num(b["hi_m"]):
                raise Gate(f"site_allowance band {i}: lo >= hi")
            if i and abs(num(b["lo_m"]) - num(s["bands"][i-1]["hi_m"])) > 0.001:
                raise Gate(f"site_allowance band {i}: not contiguous")
            if os_.get("bands") and i < len(os_["bands"]):
                check_num(f"site_allowance.bands[{i}].rate", b["rate"], os_["bands"][i]["rate"])
        if abs(num(s["bands"][0]["lo_m"]) - num(s["threshold_m"])) > 0.001:
            raise Gate("site_allowance: first band does not start at the threshold")
        for p in s["projects"]:
            check_num("site_allowance.projects." + p["name"], p["rate"], None)
        check_date("site_allowance.applies_from", s["applies_from"], os_.get("applies_from"))
        out["site_allowance"].update({k: s[k] for k in SCHEMA["properties"]["site_allowance"]["required"]})
        out["site_allowance"]["source_title"] = keep_title(s["source_title"], os_.get("source_title"))
    if "rdo_ics" in changed:
        years = new["rdo_years"]
        if not any(int(y) >= date.today().year for y in years):
            raise Gate("rdo: the calendar file parsed to no events for this year or later")
        for y, v in years.items():
            if int(y) < date.today().year:
                continue
            if len(v["rdo"]) < 20 or len(v["rdo"]) > 30:
                raise Gate(f"rdo {y}: {len(v['rdo'])} RDO events, expected 20 to 30")
            if len(v["public_holidays"]) < 8:
                raise Gate(f"rdo {y}: only {len(v['public_holidays'])} public holidays found")
            out["rdo"]["years"][y] = v
        # never drop a year we already have
        for y in old["rdo"]["years"]:
            out["rdo"]["years"].setdefault(y, old["rdo"]["years"][y])
    out["as_at"] = date.today().isoformat()
    return out


# ---------------------------------------------------------------- git + issues

def sh(*cmd, check=True):
    log("$", " ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT, check=check, text=True, capture_output=True)


def open_issue(title, body):
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo or not os.environ.get("GH_TOKEN"):
        log("ISSUE (no GH_TOKEN, printing instead):", title, "\n", body)
        return
    sh("gh", "issue", "create", "-R", repo, "-t", title, "-b", body, "-l", "cfmeu-figures", check=False)


def diff_summary(old, new):
    lines = []
    def walk(a, b, path):
        if isinstance(a, dict) and isinstance(b, dict):
            for k in sorted(set(a) | set(b)):
                walk(a.get(k), b.get(k), f"{path}.{k}" if path else k)
        elif a != b:
            lines.append(f"- `{path}`: `{a}` -> `{b}`")
    walk(old, new, "")
    return "\n".join(lines) or "(no figure changed; only the check date moved)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--offline")
    args = ap.parse_args()

    old = load(FIG, None)
    if old is None:
        sys.exit("data/cfmeu-figures.json is missing")
    manifest = load(SRC, {})

    links = find_links(args.offline)
    blobs, changed, newman = {}, [], {}
    for key, url in links.items():
        data = open(url, "rb").read() if args.offline else fetch(url)
        h = hashlib.sha256(data).hexdigest()
        blobs[key] = data
        newman[key] = {"url": url, "sha256": h, "checked": date.today().isoformat()}
        if args.force or manifest.get(key, {}).get("sha256") != h:
            changed.append(key)
    log("changed:", changed or "nothing")
    if not changed:
        if not args.dry_run:
            json.dump(newman, io.open(SRC, "w", encoding="utf-8"), indent=2)
        return 0

    try:
        new = {}
        pdf_keys = [k for k in changed if k != "rdo_ics"]
        if pdf_keys:
            texts = {k: pdf_text(blobs[k]) for k in ("wages", "allowances", "site_allowance")}
            for k, t in texts.items():
                if len(t.strip()) < 400:
                    raise Gate(f"{k}: PDF has no text layer ({len(t)} chars)")
            new = extract(texts)
            log("extracted", json.dumps(new)[:400], "...")
        if "rdo_ics" in changed:
            new["rdo_years"] = parse_ics(blobs["rdo_ics"])
        merged = validate(new, old, changed)
    except Gate as g:
        open_issue("CFMEU figures: sheet changed but a sanity gate failed",
                   f"Changed sources: {', '.join(changed)}\n\nGate: **{g}**\n\nLinks:\n" + "\n".join(f"- {k}: {v}" for k, v in links.items()) +
                   "\n\nNothing was published. Fix data/cfmeu-figures.json by hand or re-run with the gate reviewed.")
        log("GATE FAILED:", g)
        return 2 if args.dry_run else 0
    except Exception as e:  # network, API, parse
        open_issue("CFMEU figures: update job errored", f"Changed sources: {', '.join(changed)}\n\nError: `{type(e).__name__}: {e}`\n\nNothing was published.")
        log("ERROR:", repr(e))
        return 1

    summary = diff_summary({k: old[k] for k in ("wages", "allowances", "site_allowance")}, {k: merged[k] for k in ("wages", "allowances", "site_allowance")})
    log("changes:\n" + summary)
    if args.dry_run:
        return 0

    json.dump(merged, io.open(FIG, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(newman, io.open(SRC, "w", encoding="utf-8"), indent=2)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "cfmeu", "build_guides.py")], cwd=ROOT, text=True, capture_output=True)
    if r.returncode != 0:
        open_issue("CFMEU figures: page build failed after extraction", r.stdout + "\n" + r.stderr)
        return 1
    sh("git", "config", "user.name", "paykicker-figures-bot")
    sh("git", "config", "user.email", "operations@paykicker.com.au")
    sh("git", "add", "data", "public")
    msg = f"CFMEU figures: update from union sheets ({', '.join(changed)})\n\n{summary}\n\nAutomated by scripts/cfmeu/watch.py; gates passed."
    sh("git", "commit", "-m", msg)
    sh("git", "push")
    open_issue("CFMEU figures updated and published", f"Changed sources: {', '.join(changed)}\n\n{summary}\n\nPublished to main automatically; Cloudflare Pages deploys it. Check the guides and the landing page.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
