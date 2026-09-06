# SGAEIA Master SDD Specification

**Version:** 0.3.2  
**Author:** Aridio Silva — @aridiosilva  
**Date:** September 2026

## 1. System Mission

SGAEIA is a reference architecture for governed autonomous intelligence across Cloud, MEC, Edge and cyber-physical environments. Its principal invariant is:

`Distributed Intelligence ≠ Uncontrolled Distributed Authority`.

A production action is admissible only when identity, capability, context, risk and policy all permit it, with human approval where required.

## 2. Formal System Model

The system is represented as:

`S = (V, E, Z, P, I, C, R, T, L)`

where:
- `V` = entities (humans, agents, models, data, workloads, tools, nodes, external systems);
- `E` = communications/delegations/data flows;
- `Z` = trust zones;
- `P` = policy set;
- `I` = identities and attestations;
- `C` = capabilities;
- `R` = risk state;
- `T` = telemetry/evidence;
- `L` = lifecycle state.

Authorization is modeled as:

`Authorize(a,r,o,c) = Identity(a) ∧ Capability(a,o) ∧ Policy(a,r,o,c) ∧ Risk(a,r,o,c)<θ ∧ Trust(a)>τ`.

Execution is permitted iff `Authorize = true`.

## 3. Governed Agent Predicate

An agent is governed only if:

`Governed(A) = Identity ∧ Owner ∧ Purpose ∧ Capabilities ∧ Policy ∧ Risk ∧ Observability ∧ Auditability ∧ Revocability`.

## 4. Dynamic Autonomy

`A_effective = min(A_configured, A_risk, A_context, A_trust, A_policy)`.

Autonomy can only remain equal or decrease as trust degrades; failure or disconnection cannot silently increase authority.

## 5. Core Planes

1. Governance Plane — AI governance, GRC, risk appetite, compliance and policy administration.
2. Trust Plane — NHI, workload identity, PKI, attestation and secrets.
3. Agent Control Plane — registries, PDP, risk, delegation and kill switch.
4. Agentic Mesh — governed A2A/tool interactions.
5. Cyber-Physical Plane — sensors, actuators, OT and physical systems.
6. Observability/Evidence Plane — trace, decision provenance and continuous compliance.

## 6. Mandatory Architectural Rules

- Models may propose but never self-authorize sensitive actions.
- All sensitive tool calls pass through a PEP.
- Agents use non-human/workload identities, preferably short-lived.
- Delegation is explicit, bounded and non-authority-amplifying.
- Edge offline mode is fail-secure.
- L4 systems require independent deterministic/safety barriers.
- Critical actions are reconstructable through trace/evidence.
- Kill/revoke capability is independent of the controlled agent.
- Agent/model/tool changes trigger threat/risk reassessment.

## 7. Requirements and Traceability

Normative requirements are in `specs/requirements/`. The authoritative traceability matrix is `specs/traceability/requirements-controls-tests.csv`.

A requirement without a control or verification method is incomplete. A security control without evidence is not considered continuously verifiable.

## 8. Production Admission

An agent can be admitted only if:

`Spec ∧ Owner ∧ Identity ∧ ThreatModel ∧ RiskAssessment ∧ Controls ∧ Tests ∧ BOM ∧ KillSwitch ∧ Approval`.

## 9. Runtime Admission

Every critical action is evaluated again at runtime. Deployment-time approval does not grant perpetual operational authority.

## 10. Evidence Contract

For critical decisions, the evidence record MUST support reconstruction of:
- who/which workload acted;
- what intent and resource were involved;
- policy decision;
- risk score;
- relevant delegation chain;
- required human approval;
- outcome;
- trace/evidence identifier;
- integrity digest.

## 11. Security Assurance Strategy

Assurance combines:
- static SDD validation;
- unit/integration tests;
- invariant/property tests;
- adversarial tests;
- policy tests;
- supply-chain/BOM controls;
- runtime observability;
- continuous threat/risk updates;
- domain safety assurance for L4.

## 12. Conformance Levels (Reference)

- **C0 — Documented:** inventory/specs exist.
- **C1 — Enforced:** identity, PEP/PDP and capabilities are enforced.
- **C2 — Observable:** trace/evidence and anomaly detection are operational.
- **C3 — Continuous GRC:** policy/evidence/risk status continuously evaluated.
- **C4 — High Assurance:** formal invariants, attestation, red team, resilience and independent safety barriers for critical domains.

These are project-defined maturity levels, not external certifications.

## 13. Integration Port Specifications

SGAEIA SHALL expose replaceable technology dependencies through versioned **Integration Port Specifications (IPS)** under `specs/integrations/`.

For each production-critical port, conformance requires:

```text
FunctionalContract
AND SecurityContract
AND AuditContract
AND FailureContract
AND RevocationContract
AND SecurityInvariantsPreserved
```

### 13.1 Stable boundary

Product/framework choice is an adapter decision. Architectural authority resides in the port semantics and policies, not in the adapter implementation.

### 13.2 Machine-readable contracts

- synchronous HTTP reference contracts: OpenAPI 3.2.0;
- asynchronous event reference contracts: AsyncAPI 3.1.0;
- semantic port manifests: `IntegrationPort` YAML resources.

Transport-schema validity SHALL NOT be treated as proof of authorization, fail-safe, evidence or revocation conformance.

### 13.3 Failure invariant

For critical ports:

```text
DependencyFailure => AuthorityDoesNotIncrease
```

### 13.4 Replacement admission

A substitute adapter SHALL pass the qualification procedure in `specs/integrations/replacement-qualification.md` and be represented in the conformance matrix. Any semantic gap SHALL be treated as an explicit risk/deviation rather than transparent equivalence.

### 13.5 Evidence

Adapter evidence SHALL identify at minimum the port, concrete implementation/version, subject/workload, correlated trace and decision/result timestamp.

## 14. Adapter Conformance Framework

Concrete integrations SHALL be represented by versioned `AdapterProfile` resources and executable adapter contracts.

### 14.1 Binding invariant

```text
∀ Adapter A: ∃! IntegrationPort P : BoundTo(A,P)
```

A concrete adapter may not redefine the security semantics of its Integration Port.

### 14.2 Shared semantic harness

Two implementations of the same port SHALL be evaluated against the same port-level semantics even if vendor APIs differ.

```text
EquivalentAtPort(A1,A2,P,E) =
  Implements(A1,P)
  ∧ Implements(A2,P)
  ∧ Assurance(A1,E) >= Required(P,E)
  ∧ Assurance(A2,E) >= Required(P,E)
  ∧ SecurityInvariantsPreserved
```

### 14.3 Assurance truthfulness

Repository contract tests establish harness-level evidence only. `contract-harness` SHALL NOT be described as live-product certification. IPS-C2/C3 require representative/live environment tests as defined in `specs/integrations/adapter-qualification-procedure.md`.

### 14.4 Failure semantics

Critical adapter dependency failure SHALL preserve:

```text
DependencyFailure => AuthorityDoesNotIncrease
```

Reference patterns include fail-closed, read-only degradation, bounded buffer-and-retry and degrade-authority.

### 14.5 Runtime attribution

Every adapter evidence record SHALL identify the concrete `adapter_id`, `implementation_id`, `implementation_version`, `port_id`, subject, operation, trace and outcome.

### 14.6 Deployment profiles

A deployment profile selects one active adapter per required port for a deployment context. Selection SHALL NOT modify port semantics and SHALL satisfy the environment-specific minimum assurance level.

### 14.7 Reference adapters

The repository includes contract-level implementations for SPIFFE/SPIRE, OPA, Istio/Envoy, OpenTelemetry, NATS, Apache Kafka, PostgreSQL, Kubernetes and K3s. These implementations are testable integration boundaries, not upstream product certifications.

### 14.8 Admission

```text
AdapterAdmissible =
  ProfileValid
  ∧ PortConformance
  ∧ FailureTestsPassed
  ∧ EvidenceAttributable
  ∧ RevocationBoundVerifiedWhereRequired
  ∧ SupportedVersion
  ∧ ResidualRiskAccepted
```

## 15. GitHub Public Release Governance

Public repository governance is part of the SGAEIA assurance boundary because public contributions, dependencies, workflows, releases, vulnerability reports, and generated artifacts affect software supply-chain risk.

A public release MUST preserve the normative SDD chain and MUST NOT represent CI success as deployment certification. The repository SHOULD provide licensing, contribution governance, coordinated vulnerability reporting, dependency update automation, protected-branch CI, citation metadata, changelog/release discipline, and explicit assurance disclaimers.

The public-release profile is defined in `docs/github-public-release.md`. Repository-level controls include:

- reviewed pull requests for protected branches;
- SDD validation and automated tests before merge;
- adapter conformance where affected;
- dependency and GitHub Actions update monitoring;
- static code security analysis;
- secret-prevention practices;
- release validation for version tags;
- private handling of vulnerability details before coordinated disclosure.

The core invariant remains unchanged:

`PublicVisibility MUST NOT imply ReducedSecuritySemantics`.

Open-source replaceability and external contribution are accepted only through the same specification, failure, revocation, evidence, and conformance contracts used by the architecture itself.

