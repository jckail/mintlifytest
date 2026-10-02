#!/usr/bin/env python3
"""Check this content-only starter's local targets without compiling MDX."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []


def fail(source, message):
    errors.append(f"{source}: {message}")


def target_exists(source, target, site_page=False):
    target = target.strip().split()[0] if target.strip() else ""
    if not target:
        fail(source, "empty link target")
        return
    url = urlsplit(target)
    if url.scheme or target.startswith("//") or target.startswith("#"):
        return
    path = unquote(url.path)
    base = ROOT if path.startswith("/") else (ROOT / source).parent
    candidate = (base / path.lstrip("/")).resolve()
    if not candidate.is_relative_to(ROOT):
        fail(source, f"local target escapes repository: {target}")
        return
    if site_page and not candidate.suffix:
        candidate = candidate.with_suffix(".mdx")
    if not candidate.is_file():
        fail(source, f"missing local target: {target}")


try:
    config = json.loads((ROOT / "docs.json").read_text())
except (OSError, json.JSONDecodeError) as error:
    sys.exit(f"docs.json: {error}")

pages = []


def navigation(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "pages":
                for page in child:
                    if isinstance(page, str):
                        pages.append(page)
                        target_exists("docs.json", "/" + page, site_page=True)
                    else:
                        navigation(page)
            else:
                navigation(child)
    elif isinstance(value, list):
        for child in value:
            navigation(child)


navigation(config.get("navigation", {}))
if not pages:
    fail("docs.json", "no local navigation pages")
if len(pages) != len(set(pages)):
    fail("docs.json", "duplicate navigation page paths")
for asset in [config.get("favicon"), *config.get("logo", {}).values()]:
    if isinstance(asset, str):
        target_exists("docs.json", asset)

files = sorted(ROOT.rglob("*.mdx")) + [ROOT / "README.md"]
for file in files:
    relative = file.relative_to(ROOT)
    if any(part.startswith(".") or part in {"node_modules", "drafts"} for part in relative.parts) or file.name.endswith(".draft.mdx"):
        continue
    source = relative.as_posix()
    text = file.read_text()
    site_page = file.suffix == ".mdx"
    if site_page:
        frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
        for key in ["title", "description"]:
            if not frontmatter or not re.search(rf"^{key}:\s*\S", frontmatter.group(1), re.M):
                fail(source, f"missing {key} frontmatter")
    fence = False
    prose = []
    for line in text.splitlines():
        if line.startswith("```"):
            if not fence and not re.match(r"^```[A-Za-z][\w-]*", line):
                fail(source, "code fence requires a language")
            fence = not fence
        elif not fence:
            prose.append(line)
    if fence:
        fail(source, "unclosed code fence")
    content = "\n".join(prose)
    for label, target in re.findall(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)", content):
        if not label.strip():
            fail(source, "link requires a descriptive label")
        target_exists(source, target, site_page)
    for alt, target in re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content):
        if not alt.strip():
            fail(source, "image requires alt text")
        target_exists(source, target)
    for target in re.findall(r'\bhref="([^\"]*)"', content):
        target_exists(source, target, site_page)
    stack = []
    for closing, tag, attributes in re.findall(r"<(/?)([A-Z][\w]*)\b([^>]*)>", content):
        if closing:
            if not stack or stack.pop() != tag:
                fail(source, f"unbalanced component closing tag: {tag}")
        elif not attributes.rstrip().endswith("/"):
            stack.append(tag)
    if stack:
        fail(source, "unclosed components: " + ", ".join(stack))
    if re.search(r"npm install your-package|your-cli|support@yourcompany\.com", text):
        fail(source, "placeholder command/contact remains")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"Source checks passed: {len(pages)} navigation pages, local links/assets, frontmatter, fences and component tags.")
print("This is source validation, not MDX compilation, browser accessibility or hosted deployment verification.")
