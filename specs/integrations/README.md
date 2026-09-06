# SGAEIA Integration Port Specifications (IPS)

**Status:** normative SDD specification.

This directory defines the replaceable integration boundary of SGAEIA. Technologies are adapters to **semantic ports**; the ports, not product names, are the architectural contract.

## Normative rule

A replacement is conformant only when it preserves all five contract dimensions:

```text
Functional Contract
AND Security Contract
AND Audit Contract
AND Failure Contract
AND Revocation Contract
```

A solution that provides the same happy-path function but weakens failure behavior, auditability or revocation is **not** an equivalent replacement.

## Contents

- `ports/*.port.yaml` — machine-readable semantic integration-port contracts.
- `openapi/*.openapi.yaml` — synchronous HTTP adapter contracts using OpenAPI 3.2.0.
- `asyncapi/*.asyncapi.yaml` — event contracts using AsyncAPI 3.1.0.
- `conformance-matrix.csv` — required artifacts and verification expectations per port.
- `replacement-qualification.md` — procedure to qualify a substitute implementation.
- `versioning-and-compatibility.md` — compatibility/version policy.
- `security-requirements.md` — cross-cutting requirements for every adapter.

## Design principle

```text
Security / Governance Semantics
            ↓
Integration Port Contract
            ↓
Adapter
            ↓
Replaceable Technology
```

Adapters MAY use SPIFFE/SPIRE, OPA/Rego, service meshes, OpenTelemetry, PostgreSQL, Kafka, Kubernetes or other technologies. Those technologies SHALL NOT become hidden sources of authority outside the contracts defined here.

## Conformance levels

- **IPS-C0 — Documented:** implementation is mapped to a port.
- **IPS-C1 — Functional:** required operations are implemented.
- **IPS-C2 — Secure:** security and failure semantics pass automated/independent tests.
- **IPS-C3 — Governed:** audit, evidence, revocation, traceability and lifecycle requirements are satisfied.

Production use of critical ports SHOULD require IPS-C3.
