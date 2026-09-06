# Integration Replacement Qualification Procedure

## Objective

Qualify a new adapter or technology without changing the SGAEIA governance and security semantics.

## Required dossier

1. Port(s) implemented and implementation version.
2. Functional mapping from every required operation to concrete endpoints/calls/events.
3. Security mapping for identity, authentication, authorization, integrity, confidentiality and isolation.
4. Failure-mode analysis, including dependency loss, stale cache, split-brain and network partition where applicable.
5. Revocation analysis with measured propagation time.
6. Audit/evidence mapping and sample evidence records.
7. Threat model and attack-path review introduced by the adapter.
8. Test results proving the five contract dimensions.
9. Rollback and emergency disable procedure.
10. Risk acceptance for any residual semantic gap.

## Decision rule

```text
Equivalent(adapter, port) =
  FunctionalPass
  AND SecurityPass
  AND AuditPass
  AND FailurePass
  AND RevocationPass
  AND NoInvariantViolation
```

If a semantic gap remains, the implementation SHALL be classified as a deviation, linked to a risk owner, compensating controls and expiry/review date. It MUST NOT be described as a transparent replacement.

## Mandatory negative tests

A candidate adapter SHALL demonstrate at least:

- unauthenticated request denied;
- unauthorized operation denied;
- stale/expired decision or identity rejected where required;
- dependency outage produces the documented safe state;
- revocation actually propagates within the port limit;
- audit/evidence remains attributable and correlated;
- emergency controls cannot be silently bypassed.
