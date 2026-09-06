## Summary

Describe the problem and the change.

## SDD impact

- [ ] Requirements/specifications updated if behavior changed.
- [ ] Threat/risk model updated if trust boundaries, authority, inputs, outputs, tools, or dependencies changed.
- [ ] Controls and traceability mappings updated where applicable.
- [ ] Tests added or updated.
- [ ] Evidence contract considered.
- [ ] ADR added/updated for a material architectural decision.

## Security invariants

- [ ] No silent authority increase.
- [ ] Fail-secure behavior is preserved.
- [ ] Revocation and kill-switch semantics remain bounded.
- [ ] Sensitive actions remain policy-enforced outside model reasoning.
- [ ] Logging/evidence does not expose secrets or unnecessary sensitive data.

## Validation

- [ ] `python scripts/validate_specs.py`
- [ ] `python -m pytest -q`
- [ ] `python scripts/run_adapter_conformance.py` when integration ports/adapters are affected.
- [ ] BOM/evidence artifacts regenerated when required.

## Conformance claim

State the highest conformance level actually demonstrated by evidence. Do not describe local harness success as production certification.
