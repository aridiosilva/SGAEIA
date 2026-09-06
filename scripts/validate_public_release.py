from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "LICENSE", "NOTICE", "README.md", "MASTER-SPEC.md", "SECURITY.md",
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "GOVERNANCE.md", "ROADMAP.md",
    "CHANGELOG.md", "SUPPORT.md", "CITATION.cff", "PROJECT-MANIFEST.md",
    "docs/github-public-release.md", ".github/dependabot.yml",
    ".github/PULL_REQUEST_TEMPLATE.md", ".github/workflows/security-ci.yml",
    ".github/workflows/codeql.yml", ".github/workflows/release-validation.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml", ".github/CODEOWNERS",
    "RELEASE-NOTES-v0.3.2.md",
]

def fail(msg: str) -> None:
    print(f"PUBLIC RELEASE VALIDATION FAILED: {msg}")
    sys.exit(1)

for rel in REQUIRED:
    p = ROOT / rel
    if not p.is_file() or p.stat().st_size == 0:
        fail(f"missing or empty required file: {rel}")

pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
master = (ROOT / "MASTER-SPEC.md").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")

m = re.search(r'version\s*=\s*"([^"]+)"', pyproject)
if not m:
    fail("cannot determine project version")
version = m.group(1)
if f"**Version:** {version}" not in master:
    fail("MASTER-SPEC version does not match pyproject")
if version not in readme:
    fail("README does not mention current release version")


# Canonical repository metadata for v0.3.2 public publication.
canonical = "https://github.com/aridiosilva/SGAEIA"
for rel in ["CITATION.cff", "docs/github-public-release.md", "SECURITY.md", "README.md"]:
    if canonical not in (ROOT / rel).read_text(encoding="utf-8"):
        fail(f"canonical repository URL missing from {rel}")
if 'version = "0.3.2"' not in pyproject:
    fail("public RC must be version 0.3.2")

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

print(f"PUBLIC RELEASE VALIDATION PASSED: v{version}")
