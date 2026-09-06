# GitHub Public Release Profile

## Objective

This profile prepares SGAEIA for publication as a public GitHub repository while preserving its SDD, security, governance, and assurance semantics. Public publication increases the project's supply-chain, disclosure, contribution, and reputation attack surfaces; repository governance is therefore treated as part of the architecture.

## Required repository files

A public release SHOULD include at least:

- `LICENSE` and `NOTICE`;
- `README.md`;
- `MASTER-SPEC.md`;
- `SECURITY.md`;
- `CONTRIBUTING.md`;
- `CODE_OF_CONDUCT.md`;
- `GOVERNANCE.md`;
- `ROADMAP.md`;
- `CHANGELOG.md`;
- `SUPPORT.md`;
- `CITATION.cff`;
- issue and pull-request templates;
- dependency update policy;
- CI/security workflows.

## Publication checklist

Before the first public push:

1. Run secret scanning locally and review repository history if a `.git` history already exists.
2. Verify that examples contain no real credentials, tokens, hostnames, customer data, or internal addresses.
3. Confirm ownership/copyright of every bundled artifact.
4. Confirm that third-party code, if any, is license-compatible and attributed.
5. Run SDD validation, tests, adapter conformance, and BOM generation.
6. Review generated evidence for sensitive data before committing or attaching it to a release.
7. Enable GitHub branch protection/rulesets for `main`.
8. Require pull requests and passing CI for protected branches.
9. Enable Dependabot alerts/security updates where available.
10. Enable secret scanning and push protection where available.
11. Enable private vulnerability reporting if the repository/account supports it.
12. Create the initial release from a reviewed tag, not from an unreviewed working tree.

## Recommended GitHub topics

`edge-ai`, `agentic-ai`, `multi-agent-systems`, `zero-trust`, `grc`, `security-by-design`, `spec-driven-development`, `owasp`, `mitre-atlas`, `nist`, `mec`, `ai-security`.

## Suggested repository description

> Open SDD reference architecture for secure, governed, zero-trust multi-agent Edge AI, with executable GRC, formal invariants, policy enforcement, evidence-as-code and replaceable integration ports.

## Assurance disclaimer

A public release is not a certification. Repository CI demonstrates only the scopes exercised by the included tests. Deployment-specific claims require deployment-specific evidence, risk acceptance, safety engineering where applicable, and independent review appropriate to the domain.

## Branch and release model

- `main`: protected integration branch.
- feature branches: short-lived change branches.
- release tag: `vMAJOR.MINOR.PATCH`.
- release notes: derived from `CHANGELOG.md` and material security/architecture changes.

## Security-sensitive contribution rule

A public pull request MUST NOT be the first disclosure channel for a vulnerability that could enable bypass of authorization, identity, revocation, kill switch, policy enforcement, evidence integrity, or a cyber-physical safety barrier. Use the private process in `SECURITY.md`.

## Canonical repository and first push — v0.3.2

Canonical repository: `https://github.com/aridiosilva/SGAEIA`

Create an **empty** GitHub repository named `SGAEIA` under `aridiosilva` (do not initialize it with another README, license, or .gitignore), then from the audited project root run:

```bash
git init
git branch -M main
git add .
git commit -m "Initial public release candidate: SGAEIA v0.3.2"
git remote add origin https://github.com/aridiosilva/SGAEIA.git
git push -u origin main
```

After the GitHub-hosted CI/CodeQL checks pass and the published repository has been reviewed, create the release tag:

```bash
git tag -a v0.3.2 -m "SGAEIA v0.3.2 — Public Research Preview"
git push origin v0.3.2
```

In GitHub Releases, use the tag `v0.3.2`, title the release **SGAEIA v0.3.2 — Public Research Preview**, and mark it **Pre-release** for the initial research publication.
