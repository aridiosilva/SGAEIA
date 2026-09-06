# SGAEIA v0.3.1 — GitHub Public Release

This release prepares SGAEIA for publication as a public open-source reference architecture.

## Highlights

- Apache-2.0 licensing and project NOTICE.
- Public governance, contribution, support, security-disclosure, roadmap, changelog, and citation metadata.
- GitHub Issue Forms and Pull Request template.
- Dependabot monitoring for Python dependencies and GitHub Actions.
- Multi-version Python CI with SDD validation, automated tests, adapter conformance, BOM generation, and evidence upload.
- CodeQL workflow and release-tag validation gate.
- Normative README and MASTER-SPEC sections for public repository governance.
- Explicit distinction between repository test evidence and production certification.

## Verified before packaging

- SDD specification validation: PASS.
- Integration Port validation: PASS.
- Automated tests: 31 PASS.
- Adapter conformance harness: 9 profiles PASS at the documented local harness scope.

## Before creating the GitHub repository

Review `docs/github-public-release.md`, choose the final repository URL/name, and then add that final URL to `CITATION.cff` if desired. Enable repository rulesets/branch protection, Dependabot alerts/security updates, secret scanning/push protection, and private vulnerability reporting when available.

## Assurance notice

This release is an open reference architecture and demonstrative implementation. It is not a certification of any product, organization, infrastructure, AI model, agent, Edge/MEC deployment, or cyber-physical system.
