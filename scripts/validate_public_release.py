from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_VERSION = "0.3.4"
CANDIDATE_PROJECT_VERSION = "0.4.0rc1"
CANDIDATE_DISPLAY_VERSION = "0.4.0-rc.1"

REQUIRED = [
    "LICENSE", "NOTICE", "README.md", "README.pt.md", "MASTER-SPEC.md",
    "SECURITY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "GOVERNANCE.md",
    "ROADMAP.md", "CHANGELOG.md", "SUPPORT.md", "CITATION.cff",
    "PROJECT-MANIFEST.md", "docs/github-public-release.md",
    ".github/dependabot.yml", ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/security-ci.yml", ".github/workflows/codeql.yml",
    ".github/workflows/release-validation.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml", ".github/CODEOWNERS",
    "RELEASE-NOTES-v0.3.2.md",
]

def fail(msg: str) -> None:
    print(f"RELEASE/CANDIDATE VALIDATION FAILED: {msg}")
    sys.exit(1)

for rel in REQUIRED:
    path = ROOT / rel
    if not path.is_file() or path.stat().st_size == 0:
        fail(f"missing or empty required file: {rel}")

pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
master = (ROOT / "MASTER-SPEC.md").read_text(encoding="utf-8")
readmes = [
    (ROOT / "README.md").read_text(encoding="utf-8"),
    (ROOT / "README.pt.md").read_text(encoding="utf-8"),
]
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
openapi = json.loads((ROOT / "specs/api/openapi.json").read_text(encoding="utf-8"))

match = re.search(r'version\s*=\s*"([^"]+)"', pyproject)
if not match:
    fail("cannot determine project version")
candidate_version = match.group(1)
if candidate_version != CANDIDATE_PROJECT_VERSION:
    fail(f"pyproject candidate must be {CANDIDATE_PROJECT_VERSION}")
if f"**Version:** {CANDIDATE_DISPLAY_VERSION}" not in master:
    fail("MASTER-SPEC does not identify the development candidate")
if openapi.get("info", {}).get("version") != CANDIDATE_DISPLAY_VERSION:
    fail("OpenAPI version does not identify the development candidate")
if CANDIDATE_DISPLAY_VERSION not in changelog:
    fail("CHANGELOG does not identify the development candidate")
for index, readme in enumerate(readmes, start=1):
    if PUBLIC_VERSION not in readme or CANDIDATE_DISPLAY_VERSION not in readme:
        fail(f"README {index} does not distinguish public and candidate versions")

citation_match = re.search(r'^version:\s*["\']?([^"\'\n]+)', citation, re.MULTILINE)
if not citation_match or citation_match.group(1).strip() != PUBLIC_VERSION:
    fail(f"CITATION.cff must remain pinned to public v{PUBLIC_VERSION}")

canonical = "https://github.com/aridiosilva/SGAEIA"
for rel in ["CITATION.cff", "docs/github-public-release.md", "SECURITY.md", "README.md"]:
    if canonical not in (ROOT / rel).read_text(encoding="utf-8"):
        fail(f"canonical repository URL missing from {rel}")

license_text = (ROOT / "LICENSE").read_text(encoding="utf-8", errors="replace")
if "Apache License" not in license_text or "Version 2.0" not in license_text:
    fail("LICENSE is not recognizable as Apache-2.0")

security = (ROOT / "SECURITY.md").read_text(encoding="utf-8").lower()
if "do not open a public github issue" not in security:
    fail("SECURITY.md lacks explicit private-disclosure warning")

ci = (ROOT / ".github/workflows/security-ci.yml").read_text(encoding="utf-8")
for command in ["scripts/validate_specs.py", "pytest", "run_adapter_conformance.py", "generate_agent_bom.py"]:
    if command not in ci:
        fail(f"security CI missing gate: {command}")

print(
    "RELEASE/CANDIDATE VALIDATION PASSED: "
    f"public v{PUBLIC_VERSION}; candidate v{CANDIDATE_DISPLAY_VERSION}"
)
