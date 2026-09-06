# Implementation Guide

## Phase 1 — Inventory and governance
Establish owners, use cases, agent/model/tool inventories, risk appetite, L0–L4 and A0–A5 policies.

## Phase 2 — Identity and interposition
Introduce workload identity and ensure all sensitive tool/A2A calls are mediated by PEP/PDP.

## Phase 3 — Risk and delegation
Calibrate ARS and implement explicit delegation envelopes, capability scoping and toxic-combination controls.

## Phase 4 — Edge resilience
Define offline policy cache, expiry, attestation, safe degradation and sovereign-edge profiles.

## Phase 5 — Evidence and continuous GRC
Send policy decisions, traces and risk events to SIEM/GRC; automate control evidence and architecture-drift detection.

## Phase 6 — High assurance
For L3/L4: independent review, red team, formal invariants, safety analysis, chaos/security engineering and emergency drills.

## Integration Port Specifications

When moving from the reference implementation to production, select technologies by implementing the semantic contracts under `specs/integrations/`, not by replacing architectural requirements with product defaults. Run the IPS conformance tests and complete `replacement-qualification.md` for every critical adapter before production admission.

## Adapter Conformance Framework

Implement external technology through `src/sgaeia/integrations/` rather than importing vendor semantics directly into core authorization logic.

1. Select an Integration Port.
2. Create/update an `AdapterProfile`.
3. Implement the semantic adapter with an injected transport.
4. Run the shared contract/failure tests.
5. Generate `evidence/adapter-conformance.generated.json`.
6. For production, execute the Q2/Q3 live qualification procedure.
7. Select the approved adapter in a deployment profile.

A passing local harness proves IPS-C1 contract behavior only; it does not certify the upstream product or a production deployment.

