#!/usr/bin/env python3
"""Stamp a content hash onto the CSS links in every page.

Browsers cache assets/site.css hard. Without a version on the URL, a returning
visitor gets yesterday's stylesheet against today's HTML, which breaks the
layout in ways that look like a bug in the site.

Run this whenever assets/site.css or assets/fonts.css changes, before committing.

    python3 bump-assets.py
"""
import hashlib
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
ASSETS = ["assets/site.css", "assets/fonts.css"]


def short_hash(path):
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


def main():
    versions = {a: short_hash(a) for a in ASSETS}
    changed = []
    for page in sorted(ROOT.glob("*.html")):
        text = original = page.read_text()
        for asset, version in versions.items():
            text = re.sub(
                rf'href="{re.escape(asset)}(\?v=[a-f0-9]+)?"',
                f'href="{asset}?v={version}"',
                text,
            )
        if text != original:
            page.write_text(text)
            changed.append(page.name)

    for asset, version in versions.items():
        print(f"{asset}  ->  ?v={version}")
    print(f"{len(changed)} page(s) updated")


if __name__ == "__main__":
    main()
