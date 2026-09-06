# Contributing to SGAEIA

Thank you for contributing to the Secure Governed Autonomous Edge Intelligence Architecture. Contributions are welcome when they preserve the project's security invariants, SDD traceability, and vendor-neutral contracts.

## Before proposing a change

1. Read `README.md`, `MASTER-SPEC.md`, `GOVERNANCE.md`, and `SECURITY.md`.
2. Search existing issues and ADRs.
3. Describe the problem independently of the preferred product or framework.
4. Identify affected requirements, trust boundaries, risks, controls, tests, and evidence.

## Development setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/validate_specs.py
python -m pytest -q
python scripts/run_adapter_conformance.py
```

## Pull requests

Pull requests SHOULD be small enough to review and MUST accurately state their assurance level. A new adapter is not production-certified merely because it satisfies the local contract harness.

Changes that alter a normative invariant, public contract, trust boundary, conformance semantics, or failure/revocation behavior SHOULD include an ADR.

## SDD traceability

When behavior changes, update the relevant chain:

`Requirement -> Threat/Risk -> Control -> Policy/Implementation -> Test -> Evidence`.

A new security requirement without a verification strategy is incomplete. A control without evidence is not continuously verifiable.

## Security and safety

Do not submit real secrets, exploit details against active systems, customer data, proprietary datasets, or unsafe cyber-physical instructions. Report vulnerabilities privately according to `SECURITY.md`.

## Style

- Prefer explicit normative language (`MUST`, `SHOULD`, `MAY`) in normative specifications.
- Keep reference integrations replaceable through Integration Port Specifications.
- Distinguish simulation, local harness evidence, representative-environment evidence, and production evidence.
- Add tests for failure paths, not only happy paths.

## Licensing

By contributing, you agree that your contribution may be distributed under the repository's Apache License 2.0 unless explicitly agreed otherwise before merge.
