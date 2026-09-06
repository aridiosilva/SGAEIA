# Método SDD

## Regra de precedência
Uma mudança deve iniciar na especificação apropriada. Código sem correspondência em uma spec aprovada é drift.

## Artefatos obrigatórios para novo agente
1. `agent manifest`;
2. owner e purpose;
3. classificação L0-L4;
4. autonomia A0-A5;
5. trust zone;
6. capabilities e denied capabilities;
7. delegation envelope;
8. threat model delta;
9. risk assessment;
10. control mapping;
11. testes;
12. kill-switch e observabilidade.

## Definition of Done
`Spec ∧ Identity ∧ ThreatModel ∧ Risk ∧ Controls ∧ Tests ∧ Evidence ∧ Approval`.

## Integration Port Specifications

Technology-facing dependencies are specified as stable semantic ports under `specs/integrations/`. A change of vendor/framework is therefore treated as a specification change or adapter qualification event, not as an implementation-only substitution.

The SDD chain is:

```text
Requirement -> ADR/Architecture -> Integration Port -> Adapter -> Conformance Test -> Evidence
```

For a replacement to be accepted it must preserve functional, security, audit, failure and revocation contracts and must not violate any system security invariant.

## Adapter changes as SDD changes

Changing a vendor, major/minor version, transport, mesh, identity system, policy engine, event bus, database or Edge orchestrator is an SDD-relevant change when it can alter port semantics, failure behavior, revocation, observability or threat surface.

The required chain is:

`Requirement -> IPS -> AdapterProfile -> Adapter Code -> Conformance Test -> Evidence -> Deployment Profile -> Runtime Evidence`.

