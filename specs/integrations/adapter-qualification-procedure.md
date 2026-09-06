# Adapter Qualification Procedure

## 1. Objective

Prove that a concrete implementation can replace another implementation behind the same SGAEIA Integration Port without violating security/governance invariants.

## 2. Stages

### Stage Q0 — Inventory
Record product, version, adapter version, owner, deployment topology, trust zone and data classifications.

### Stage Q1 — Contract harness / IPS-C1
Run deterministic functional and negative contract tests with injected transports. Verify evidence attribution and declared failure mode.

### Stage Q2 — Live security qualification / IPS-C2
Against a representative deployment, test authentication, authorization, malformed input, replay, timeout, partition, dependency loss, resource exhaustion and downgrade attempts.

### Stage Q3 — Governed qualification / IPS-C3
Measure revocation propagation, verify immutable/correlated evidence, validate rollback and emergency disable, map residual risks and obtain owner/GRC acceptance.

## 3. Mandatory failure tests

- dependency timeout;
- invalid/unverifiable identity;
- stale policy/configuration;
- network partition;
- duplicate/replayed event where applicable;
- evidence sink failure;
- revocation while in-flight;
- control-plane unavailability;
- version mismatch.

## 4. Decision

A product is not considered a transparent substitute merely because its API is compatible. Any gap in failure, audit or revocation semantics is an explicit architectural deviation and risk acceptance item.
