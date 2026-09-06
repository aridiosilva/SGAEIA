# Adapter Conformance Framework

This directory declares **concrete technology adapter profiles** for SGAEIA Integration Ports.

The stable architecture boundary is the `IntegrationPort`; the adapter profile binds a concrete implementation to that port without transferring architectural authority to the product.

## Assurance distinction

A profile with `verification: contract-harness` means that the repository contains executable client-side semantics and automated contract tests. It **does not** mean the named upstream product has been independently certified in a live environment.

Production qualification is progressive:

- **IPS-C1** — functional contract harness;
- **IPS-C2** — security/failure/adversarial tests against a live or representative environment;
- **IPS-C3** — governed production qualification including evidence, measured revocation, lifecycle, rollback and GRC acceptance.

## Reference profiles

- `ADP-SPIRE-IDENTITY` → `IP-IDENTITY`
- `ADP-OPA-PDP` → `IP-PDP`
- `ADP-ISTIO-MESH` → `IP-MESH`
- `ADP-OTEL-OBS` → `IP-OBS`
- `ADP-NATS-BUS` → `IP-BUS`
- `ADP-POSTGRES-STATE` → `IP-STATE`
- `ADP-K8S-EDGE` → `IP-EDGE`

Apache Kafka is explicitly represented as a substitute candidate for `IP-BUS`; K3s is represented as an Edge-oriented Kubernetes implementation candidate for `IP-EDGE`.

## Rule

```text
AdapterAccepted(port) =
    PortSemanticsPreserved
AND ContractTestsPassed
AND FailureSemanticsPassed
AND EvidenceAttributable
AND RevocationBoundVerifiedWhereRequired
AND ResidualRiskAccepted
```
