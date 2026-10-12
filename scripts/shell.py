#!/usr/bin/env python3
"""Stamp the one site nav and the one site footer into every page that carries the shell markers.

    python scripts/shell.py            stamp every page under public/ that has the markers
    python scripts/shell.py --check    report pages whose nav or footer has drifted (exit 1 if any)
    python scripts/shell.py FILE ...   stamp only these files

A page opts in by carrying, once each:

    <!-- shell:nav --><!-- /shell:nav -->          (right after <body>)
    <!-- shell:footer --><!-- /shell:footer -->    (right before the closing scripts)

Everything between a pair is replaced by the template in scripts/shell/nav.html or footer.html.
Per page, the stamp fills in:
  {{demo}}             "#contact" when the page carries the demo form (id="demoForm"), else "/#contact"
  aria-current="page"  on the nav and footer links whose href is this page's own path

Files are read and written as BYTES and keep their own line endings (Windows text mode would
rewrite them). Pages without markers (the legacy set-out pages) are left alone and listed by --check.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
TPL = pathlib.Path(__file__).resolve().parent / "shell"
BLOCKS = ("nav", "footer")


def page_path(f: pathlib.Path) -> str:
    rel = f.relative_to(PUBLIC).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel[: -len(".html")]


def render(name: str, page: bytes, path: str, eol: bytes) -> bytes:
    t = (TPL / f"{name}.html").read_bytes().replace(b"\r\n", b"\n").rstrip(b"\n")
    demo = b"#contact" if b'id="demoForm"' in page else b"/#contact"
    t = t.replace(b"{{demo}}", demo)
    href = f'href="{path}"'.encode()
    t = t.replace(href + b">", href + b' aria-current="page">')
    return t.replace(b"\n", eol)


def stamp(page: bytes, path: str):
    eol = b"\r\n" if b"\r\n" in page else b"\n"
    out = page
    for name in BLOCKS:
        start, end = f"<!-- shell:{name} -->".encode(), f"<!-- /shell:{name} -->".encode()
        if out.count(start) != 1 or out.count(end) != 1:
            return None
        a = out.index(start) + len(start)
        b = out.index(end)
        if b < a:
            return None
        out = out[:a] + eol + render(name, out, path, eol) + eol + out[b:]
    return out


def main(argv):
    check = "--check" in argv
    files = [pathlib.Path(a).resolve() for a in argv if not a.startswith("--")]
    if not files:
        files = sorted(PUBLIC.rglob("*.html"))
    drift, legacy, stamped = [], [], 0
    for f in files:
        page = f.read_bytes()
        if b"<!-- shell:nav -->" not in page:
            legacy.append(f)
            continue
        new = stamp(page, page_path(f))
        if new is None:
            print(f"BROKEN markers: {f.relative_to(ROOT)}")
            drift.append(f)
            continue
        if new != page:
            if check:
                drift.append(f)
                print(f"DRIFT: {f.relative_to(ROOT)}")
            else:
                f.write_bytes(new)
                stamped += 1
                print(f"stamped: {f.relative_to(ROOT)}")
    if check:
        print(f"{len(files) - len(legacy) - len(drift)} in step, {len(drift)} drifted, {len(legacy)} without the shell (legacy)")
        for f in legacy:
            print(f"  legacy: {f.relative_to(ROOT)}")
        return 1 if drift else 0
    print(f"{stamped} stamped")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
