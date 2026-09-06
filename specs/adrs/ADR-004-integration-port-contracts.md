# ADR-004 — Integration Ports as Stable Architectural Boundaries

## Status
Accepted — September 2026.

## Context
SGAEIA must remain vendor-neutral while preserving security and governance behavior across substitutions such as SPIFFE/SPIRE, OPA/Rego, service mesh, telemetry, storage, messaging and Edge orchestrators.

## Decision
The architecture SHALL define stable **Integration Port Specifications (IPS)**. Product/framework integrations are adapters to those ports.

Every critical port SHALL define functional, security, audit, failure and revocation contracts. Where suitable, transport contracts SHALL be machine-readable using OpenAPI or AsyncAPI, but transport schema compatibility does not prove semantic equivalence.

## Consequences

Positive:
- reduces vendor lock-in;
- makes substitutions testable;
- keeps authority outside agent/model implementations;
- enables procurement and GRC comparison using the same requirements;
- supports parallel adapters per cloud/edge domain.

Trade-offs:
- adapters require explicit qualification;
- abstraction may expose lowest-common-denominator risks if contracts are underspecified;
- semantic versioning and conformance testing become governance obligations.

## Invariant

```text
ReplacementAllowed
=> FunctionalPass
AND SecurityPass
AND AuditPass
AND FailurePass
AND RevocationPass
AND NoSecurityInvariantViolation
```
