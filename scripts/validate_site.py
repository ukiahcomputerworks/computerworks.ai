from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ROUTES = {
    "index.html",
    "business-it-infrastructure.md",
    "clientele.md",
    "automation.md",
    "workflow-rescue.md",
    "workflow-rescue-legacy-redirect.md",
    "certifications.md",
    "contact.md",
    "awards.md",
    "local.md",
    "tips.md",
    "sitemap.md",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


missing = sorted(name for name in EXPECTED_ROUTES if not (ROOT / name).is_file())
if missing:
    fail(f"missing retained routes: {', '.join(missing)}")

config = (ROOT / "_config.yml").read_text(encoding="utf-8")
header = (ROOT / "_includes" / "header.html").read_text(encoding="utf-8")
footer = (ROOT / "_includes" / "footer.html").read_text(encoding="utf-8")
contact = (ROOT / "contact.md").read_text(encoding="utf-8")
cname = (ROOT / "CNAME").read_text(encoding="utf-8").strip()

checks = {
    "site title": "title: ComputerWorks.AI" in config,
    "canonical URL": 'url: "https://www.computerworks.ai"' in config,
    "custom domain": cname == "www.computerworks.ai",
    "new logo reference": "/images/computerworks-ai-modern-v1.png" in header,
    "new logo file": (ROOT / "images" / "computerworks-ai-modern-v1.png").is_file(),
    "footer brand": "ComputerWorks.AI" in footer,
    "Wufoo account preserved": "'userName':'computerworksofukiah'" in contact,
    "Wufoo form preserved": "'formHash':'z9cbgzd0wxkahu'" in contact,
}
for name, passed in checks.items():
    if not passed:
        fail(name)

text_extensions = {".html", ".md", ".yml", ".yaml", ".css", ".js"}
old_brand = re.compile(r"Computer\s*Works\s+of\s+Ukiah", re.IGNORECASE)
violations = []
for path in ROOT.rglob("*"):
    if ".git" in path.parts or ".trash" in path.parts or path.suffix.lower() not in text_extensions:
        continue
    if old_brand.search(path.read_text(encoding="utf-8")):
        violations.append(str(path.relative_to(ROOT)))
if violations:
    fail(f"old visible brand remains in: {', '.join(sorted(violations))}")

print(f"PASS: {len(EXPECTED_ROUTES)} retained routes and all ComputerWorks.AI source gates")
sys.exit(0)
