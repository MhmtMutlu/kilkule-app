#!/usr/bin/env python3
"""Copies the game's legal texts into src/ unchanged (the game repo's docs/legal is their only source).

    python3 tools/import_legal.py ../kilkule   →   python3 build.py

The privacy policy (six languages), the terms of use (Turkish, English) and the KVKK notice are copied byte for byte;
build.py renders them. The support and account deletion pages (src/support.*.md, src/delete.*.md) belong to this site
and are edited here.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = {f"privacy-policy.{l}.md": f"privacy.{l}.md" for l in ("tr", "en", "fr", "de", "it", "es")}
FILES |= {f"terms-of-use.{l}.md": f"terms.{l}.md" for l in ("tr", "en")}
FILES["kvkk-aydinlatma.tr.md"] = "kvkk.tr.md"

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 tools/import_legal.py <kilkule repo>")
    legal = pathlib.Path(sys.argv[1]) / "docs" / "legal"
    missing = [name for name in FILES if not (legal / name).is_file()]
    if missing:
        raise SystemExit(f"{legal}: missing {', '.join(missing)}")
    changed = []
    for name, target in FILES.items():
        data, out = (legal / name).read_bytes(), ROOT / "src" / target
        if not out.exists() or out.read_bytes() != data:
            out.write_bytes(data)
            changed.append(target)
    print("changed:", ", ".join(changed) if changed else "nothing")

if __name__ == "__main__":
    main()
