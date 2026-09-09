# Secure Governed Multi-Agent Edge AI — SDD Reference Project

**SGAEIA — Secure Governed Autonomous Edge Intelligence Architecture**  
**Aridio Silva — @aridiosilva — September 2026**

**Languages:** English | [Português](README.pt.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22557795.svg)](https://doi.org/10.5281/zenodo.22557795)

**Current public release:** `v0.3.4 — Citation and Zenodo Metadata Fix`  
**Research status:** `Public Research Preview`  
**Concept DOI:** `10.5281/zenodo.22557795`  
**Version DOI (v0.3.4):** `10.5281/zenodo.22557796`  
**License:** Apache-2.0

**Unreleased candidate on `main`:** `v0.4.0-rc.1 — Alien Cognition and Architectural Assurance` (merged from PR #13)  
The candidate is not a release or certification; `v0.3.4` remains the immutable public DOI baseline.

A **Spec-Driven Development (SDD)** reference project for **multi-agent Edge AI** architectures with **Zero Trust, distributed GRC, Security-by-Design, Security-First, Shift Left/Right/Everywhere, and governed autonomy**.

> **Status:** architectural reference and minimal demonstrative implementation. It is not a production-ready product and does not replace legal analysis, safety engineering, domain-specific threat modeling, regulatory validation, operational hardening, or independent certification.

---

## 1. Executive Summary

This repository transforms a conceptual multi-agent Edge AI architecture into a **formal, versionable, testable, and partially executable SDD Project**.

The problem addressed is simple to formulate, but complex to solve:

```text
Distributed Intelligence
        ≠
Uncontrolled Distributed Authority
```

Modern systems may simultaneously combine:

- local and remote AI agents;
- LLMs and other models;
- Edge, Far Edge, MEC, and Cloud;
- IoT/IIoT;
- OT/ICS;
- sensors and actuators;
- RAG and vector databases;
- agentic memory;
- APIs, tools, and MCP servers;
- SaaS and third-party services;
- multiple organizations and trust domains.

Therefore, the goal of this architecture is to enable **distributed intelligence** without granting **ungoverned distributed authority**.

The central thesis is:

```text
Intelligence != Trust
Trust        != Authority
Authority    != Unlimited Autonomy
Autonomy     => Governance + Evidence + Revocability
```

The AI model may propose an action. The architecture must decide whether that action may be executed.

---

## 2. What This Project Formalizes

The project defines and implements a reference for:

- non-human identity (**NHI**) for agents and workloads;
- **L0–L4** criticality classification;
- **A0–A5** autonomy levels;
- **Agent Trust Zones — ATZ-0…ATZ-5**;
- **Agent Registry**;
- **Model Registry**;
- **Tool Registry**;
- **Capability Graph**;
- **Delegation Graph**;
- **Delegation Envelope**;
- **Policy Administration Point — PAP**;
- **Policy Decision Point — PDP**;
- **Policy Enforcement Point — PEP**;
- **Risk Engine**;
- **Agent Risk Score — ARS**;
- **Kill Switch**;
- **Evidence-as-Code**;
- **Decision Provenance**;
- **Zero-Trust Agentic Mesh — ZTAM**;
- **Continuous Threat Modeling**;
- **Architecture Drift Detection**;
- **AI-BOM**;
- **Agent-BOM**;
- integration with **SBOM**;
- **Integration Port Specifications — IPS**;
- **Adapter Conformance Framework — ACF** with concrete profiles and progressive assurance;
- control catalog;
- risk register and threat register;
- invariant tests;
- adversarial tests;
- security gates in CI/CD;
- formal models in **TLA+** and **Alloy**;
- SDD traceability across requirement, risk, control, implementation, test, and evidence.

---

## 3. Fundamental Architectural Assumption

The architecture assumes from the outset:

```text
Agent may fail.
Agent may hallucinate.
Agent may be manipulated.
Agent may be compromised.
Agent may collaborate unexpectedly.
External tools may become hostile.
Data may be poisoned.
Models may be replaced or corrupted.
Edge connectivity may fail.
```

Therefore:

```text
System Safety != Agent Correctness
```

System security **cannot depend on the agent behaving correctly**.

It must result from controls external to the agent's reasoning that limit what it can do even when it is wrong, compromised, or under malicious influence.

This principle guides the entire implementation.

---

## 4. Normative Principles

The architecture adopts the following principles.

### P-01 — Zero Implicit Trust

No agent, workload, user, model, tool, device, or service receives trust solely because of:

- location;
- network;
- organization;
- ownership;
- declared origin;
- relationship with a parent agent.

### P-02 — Every Agent Has an Identity

Every agent must have its own verifiable identity.

```text
Agent => Non-Human Identity
```

### P-03 — No Action Without Authorization

```text
Intent -> Authorization -> Execution
```

Never:

```text
Intent -> Execution -> Audit
```

### P-04 — Principle of Least Agency — PoLA

An agent must have only the autonomy required for its purpose.

Least Privilege is insufficient when the system can also:

- plan;
- delegate;
- execute tools;
- initiate new workflows;
- reach the physical world.

### P-05 — Delegation Cannot Increase Authority

Delegation cannot create authority that the delegating agent does not possess in the context of the operation.

```text
Capabilities(child) <= DelegatedCapabilities(parent)
```

### P-06 — Autonomy Must Be Revocable

All relevant autonomy must be capable of being:

- paused;
- reduced;
- revoked;
- isolated;
- terminated.

```text
Autonomy => Revocability
```

### P-07 — Model Is Never the Security Authority

The LLM may recommend or plan an action. The LLM is not the authority that grants permission for its own execution.

### P-08 — Policy Before Action

Every relevant action must pass through a **PEP** before reaching a resource, tool, or actuator.

### P-09 — Evidence by Default

Every relevant action must produce verifiable evidence.

```text
Action -> Evidence
```

### P-10 — Assume Agent Compromise

The system must remain constrained even when a valid agent is compromised.

---

## 5. Security Invariants

The project transforms principles into verifiable properties.

1. `AgentWithoutIdentity => DENY`
2. `UnknownAgent => DENY`
3. `L4 AND A5 => DENY`
4. `DelegationDepth > MaxDepth => DENY`
5. `ChildCapabilities ⊄ ParentDelegatedCapabilities => DENY`
6. `PaymentCreator == PaymentApprover => DENY`
7. `UntrustedInput -> PhysicalActuation` cannot exist without explicit mediation and authorization.
8. `AttestationFailed AND CriticalAgent => STOP/QUARANTINE`
9. `OfflineMode => ReducedAuthority`, never increased authority.
10. Every critical action must produce evidence and decision provenance.
11. An agent cannot independently increase its own autonomy.
12. A model cannot grant authorization to itself.
13. A trust boundary cannot be crossed solely by an LLM semantic decision.
14. Critical credentials must have limited validity and be revocable.
15. A critical action without an owner, policy, or traceability must be denied.

The objective is not merely to detect bad behavior. It is to build an architecture in which certain classes of behavior are **impossible or strongly constrained by construction**.

---

## 6. General Formal Model

The system can be represented as:

```text
S = (V, E, Z, P, I, C, R, T, L)
```

where:

- `V` = entities;
- `E` = relationships;
- `Z` = trust zones;
- `P` = policies;
- `I` = identities;
- `C` = capabilities;
- `R` = risks;
- `T` = telemetry/evidence;
- `L` = lifecycle state.

Entities can be decomposed as:

```text
V = H ∪ A ∪ M ∪ D ∪ W ∪ F ∪ N ∪ X
```

where:

- `H` = humans;
- `A` = agents;
- `M` = models;
- `D` = data;
- `W` = workloads;
- `F` = tools;
- `N` = infrastructure nodes;
- `X` = external entities.

Trust is dynamic:

```text
Trust = f(identity, context, device, attestation, behavior, history, policy, risk)
```

It is not a permanent property of an entity.

---

## 7. Authorization Model

The authorization decision can be represented as:

```text
Authorize(a, r, o, c, t) =
    IdentityValid(a)
    AND CapabilityValid(a, o)
    AND PolicyAllows(a, r, o, c)
    AND Risk(a, r, o, c) < MaxRisk
    AND Trust(a) > MinTrust
```

where:

- `a` = agent/workload;
- `r` = resource;
- `o` = operation;
- `c` = context;
- `t` = temporal state.

Therefore:

```text
Execute iff Authorize == true
```

---

## 8. Governed Autonomy

The project uses the concept of **Governed Autonomy**.

The question is not merely:

> Can the agent execute this action?

The correct question is:

> May this agent execute this action, on this resource, in this context, at this time, under this risk, with this evidence, and with this possibility of revocation?

Effective autonomy must be dynamic:

```text
A_effective = min(
    A_configured,
    A_risk,
    A_context,
    A_trust,
    A_policy
)
```

An agent configured as `A4` may be automatically downgraded to `A1` during an anomaly or loss of trust.

---

## 9. Agent Classification L0–L4

| Class | Description | Examples | Normal maximum autonomy |
|---|---|---|---:|
| L0 | Informational | summarization, public queries | A4 |
| L1 | Limited operational | low-impact internal tasks | A3 |
| L2 | Privileged corporate | sensitive data, ERP, business workflows | A3 |
| L3 | Critical | financial, administrative, regulated | A2 |
| L4 | Cyber-physical / safety critical | OT, robots, PLCs, actuators | A1/A2 |

The combination:

```text
L4 + A5
```

is explicitly prohibited by the reference architecture.

---

## 10. Autonomy Levels A0–A5

| Level | Meaning |
|---|---|
| A0 | Observe |
| A1 | Recommend |
| A2 | Act with approval |
| A3 | Bounded autonomous execution |
| A4 | Autonomous planning and execution |
| A5 | Autonomous orchestration/delegation |

Autonomy is not treated as a Boolean. It is a risk and governance variable.

---

## 11. Agent Trust Zones — ATZ

| Zone | Meaning | Posture |
|---|---|---|
| ATZ-0 | External / Unknown | no implicit trust |
| ATZ-1 | Untrusted Inputs | untrusted input |
| ATZ-2 | Sandboxed Agents | low authority |
| ATZ-3 | Enterprise Agents | conditional trust |
| ATZ-4 | Privileged Agents | strengthened controls |
| ATZ-5 | Cyber-Physical Critical | maximum criticality, never implicit trust |

ATZ-5 **does not** mean “fully trusted.” It means **maximum criticality and maximum control rigor**.

A transition between zones must satisfy:

```text
AuthN AND AuthZ AND Policy AND Risk AND Context AND Trust == ALLOW
```

Otherwise:

```text
DENY
```

The default posture is **Default Deny**.

---

## 12. C4 — System Context

```text
                         ┌──────────────────┐
                         │ Human Operators  │
                         └────────┬─────────┘
                                  │
                                  ▼
                  ┌─────────────────────────────┐
                  │ Secure Governed Edge-AI     │
                  │ Multi-Agent Platform        │
                  └──────────────┬──────────────┘
                                 │
       ┌─────────────────────────┼────────────────────────┐
       │                         │                        │
       ▼                         ▼                        ▼
┌──────────────┐          ┌───────────────┐       ┌──────────────┐
│ Enterprise   │          │ External SaaS │       │ Physical /   │
│ Systems      │          │ APIs / Models │       │ OT Systems   │
└──────────────┘          └───────────────┘       └──────────────┘
```

---

## 13. C4 — Containers / Planes

```text
┌──────────────────────────────────────────────────────────────┐
│                     GOVERNANCE PLANE                         │
│ AI Governance │ GRC │ Risk │ Compliance │ Audit │ Policies │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                       TRUST PLANE                            │
│ Identity │ Attestation │ PKI │ NHI │ Secrets │ Trust      │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                    AGENT CONTROL PLANE                       │
│ Agent Registry │ Capability Registry │ Model/Tool Registry │
│ PDP │ Risk Engine │ Delegation Controller │ Kill Switch    │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                       AGENTIC MESH                           │
│ Cloud Agents ↔ MEC Agents ↔ Edge Agents ↔ Device Agents   │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                  CYBER-PHYSICAL PLANE                        │
│ Sensors │ Cameras │ PLC │ Robots │ Vehicles │ Actuators    │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                  OBSERVABILITY PLANE                         │
│ Logs │ Traces │ Decisions │ Actions │ Evidence │ SIEM/SOC  │
└──────────────────────────────────────────────────────────────┘
```

---

## 14. Secure Agent Runtime

Each agent runtime must interpose controls between reasoning and execution:

```text
Input Gateway
      │
      ▼
Prompt/Input Security
      │
      ▼
Context Builder
  ├── RAG
  ├── Memory
  └── External Data
      │
      ▼
Model Runtime
      │
      ▼
Agent Planner
      │
      ▼
Proposed Action
      │
      ▼
┌───────────────────────────────────┐
│ SECURITY INTERPOSITION            │
│ Identity Validation               │
│ Capability Check                  │
│ Risk Check                        │
│ Policy Check                      │
│ Delegation Check                  │
│ Human Approval Check              │
└─────────────────┬─────────────────┘
                  │
         ┌────────┴─────────┐
         │                  │
       ALLOW              DENY
         │                  │
         ▼                  ▼
      Tool/API          Security Log
         │
         ▼
      Evidence
```

The essential point is that the agent **does not have direct, unrestricted access to the tool**.

---

## 15. Data Flow Diagram — DFD

```text
                External/User Input
                        │
                        ▼
                 [DF1 Input Gateway]
                        │
                        ▼
               [DF2 Input Sanitizer]
                        │
                        ▼
                 [DF3 Agent Core]
                  /     │      \
                 /      │       \
                ▼       ▼        ▼
             Memory    RAG      Model
                │       │        │
                └───────┼────────┘
                        ▼
                 Proposed Action
                        │
                        ▼
                  [DF4 PEP]
                        │
              ┌─────────┴──────────┐
              ▼                    ▼
         Internal Tool        External Tool
              │                    │
              ▼                    ▼
             Data                 API
              │                    │
              └─────────┬──────────┘
                        ▼
                   Evidence Bus
                        │
                        ▼
                    SIEM / GRC
```

Relevant trust boundaries include:

```text
TB-01 Human -> Agent
TB-02 External Data -> Agent
TB-03 Agent -> Model
TB-04 Agent -> RAG
TB-05 Agent -> Memory
TB-06 Agent -> Agent
TB-07 Agent -> Tool
TB-08 Edge -> MEC
TB-09 MEC -> Cloud
TB-10 IT -> OT
TB-11 Enterprise -> Third Party
TB-12 Digital -> Physical
```

Each boundary must have its own threat model.

---

## 16. Agent and Workload Identity

One of the most dangerous architectural mistakes is allowing agents to operate generically using the credential of a user, server, or application.

Each agent must have its own record:

```text
AgentIdentity = {
    ID,
    Owner,
    Role,
    Model,
    Version,
    Capabilities,
    Permissions,
    Tools,
    DataScope,
    ExecutionEnvironment,
    RiskLevel,
    PolicySet
}
```

Conceptual workload identity example:

```text
spiffe://enterprise.ai/agents/finance/invoice-agent/production/instance-8834
```

The use of SPIFFE/SPIRE in this project is **referential**, not mandatory. See the **Replaceable Integration Points** section.

---

## 17. Agent Identity Record — AIR

Example:

```yaml
agent:
  id: invoice-agent-prod-01

  owner:
    organization: enterprise
    business_unit: finance

  purpose:
    - analyze_invoice
    - reconcile_vendor

  model:
    id: model-x
    version: 7

  execution:
    zone: ATZ-3
    node: edge-sp-04

  capabilities:
    allow:
      - invoices.read
      - vendors.read
      - erp.query

    deny:
      - payments.execute
      - external.network.write

  autonomy: A2

  delegation:
    allowed: true
    max_depth: 1

  risk_class: L2
  kill_switch: required

  audit:
    immutable: true
```

The Agent Registry must make it possible to answer:

- Who is this agent?
- Who is its owner?
- What is its purpose?
- Which model does it use?
- In which runtime does it execute?
- What data can it access?
- Which tools can it use?
- Can it delegate?
- To whom?
- What is its autonomy level?
- What is its risk?
- Who can stop it?

---

## 18. Capability Graph

The project does not treat authorization only as broad roles.

```text
Agent.Invoice
    │
    ├── READ -> InvoiceDB
    ├── READ -> VendorDB
    ├── CALL -> OCR
    └── CALL -> ERP.Query
```

Formally:

```text
G_C = (A, C, E_C)
```

where:

- `A` = agents;
- `C` = capabilities;
- `E_C` = grant relationships.

Capabilities should be specific and temporary where appropriate:

```text
resource: invoice/89383
operation: read
duration: 60 seconds
delegate: false
```

---

## 19. Toxic Capability Combinations

Risk does not arise only from an isolated capability.

Example:

```text
SensitiveRead
+
ExternalWrite
+
CodeExecution
=
HighExfiltrationRisk
```

Another example:

```text
PaymentCreate + PaymentApprove = SegregationOfDutiesViolation
```

Therefore, the Policy Engine must evaluate **capability combinations**, not only individual permissions.

---

## 20. Delegation Graph

```text
G_D = (A, E_D)
```

An edge:

```text
Agent-A -> Agent-B
```

means that A may delegate a specific task to B.

Delegation must be constrained by:

- depth;
- duration;
- capabilities;
- data scope;
- cost;
- runtime;
- onward delegation.

Example:

```yaml
delegation:
  parent: agent-A
  child: agent-B

  purpose:
    - validate_invoice

  capabilities:
    - invoice.read

  expires: 2026-09-05T23:45:00-03:00
  onward_delegation: false
  max_tokens: 15000
  max_cost: 2.00
```

Agent B **does not automatically inherit** all of A's permissions.

---

## 21. Agent-to-Agent Security

All relevant A2A communication must provide for:

1. mutual identity;
2. authentication;
3. authorization;
4. confidentiality;
5. integrity;
6. freshness;
7. anti-replay;
8. non-repudiation when required;
9. schema validation;
10. intent validation;
11. correlation/trace ID;
12. policy evaluation.

---

## 22. Agent Intent Manifest

Before a critical operation, the agent must declare its intent:

```json
{
  "agent": "invoice-agent-01",
  "intent": "approve_invoice_analysis",
  "resource": "invoice-88238",
  "planned_actions": [
    "read_invoice",
    "query_vendor",
    "compare_purchase_order"
  ],
  "external_calls": [],
  "delegation": false,
  "estimated_risk": 21
}
```

The PEP does not authorize merely “a connection.” It must be able to authorize the **action and the intent in context**.

---

## 23. Policy Architecture — PAP / PDP / PEP

```text
Policy Administration Point — PAP
              │
              ▼
Policy Decision Point — PDP
              │
    ┌─────────┼─────────┐
    │         │         │
 Identity    Risk     Context
    │         │         │
    └─────────┼─────────┘
              ▼
Policy Enforcement Point — PEP
              │
              ▼
            Action
```

### Primary Rule

```text
Decision -> PolicyCheck -> Action
```

Not:

```text
Decision -> Action -> Audit
```

Post-event auditing detects harm. Security-by-Design should prevent harm before execution whenever possible.

---

## 24. Hierarchical and Distributed PDP

Edge AI should not depend exclusively on a cloud PDP.

```text
Global PDP
    │
    ├── Regional PDP
    │       │
    │       └── MEC PDP
    │               │
    │               └── Edge PDP
    │
    └── Emergency Policy Cache
```

Principle:

```text
Global Governance
+
Local Decision
+
Central Evidence
```

---

## 25. Disconnected Operation and Fail Secure

Loss of cloud connectivity or network access must not increase privileges.

```text
OfflineMode => ReducedAuthority
```

Never:

```text
OfflineMode => UnlimitedAuthority
```

Example of safe behavior:

```text
ALLOW cached low-risk operation
DENY unknown high-risk operation
DENY privilege escalation
DENY new external delegation
```

---

## 26. Sovereign Edge Mode

Critical environments may operate in **Sovereign Edge Mode**, retaining locally:

- identity verification;
- policy enforcement;
- the minimum required models;
- the minimum required RAG;
- logging;
- risk scoring;
- kill switch;
- safe operating mode.

The objective is not to permanently isolate the Edge, but to preserve a safe condition during degraded connectivity.

---

## 27. Safe Degradation

When trust decreases, authority must decrease.

```text
Normal             -> A3
Network degraded   -> A2
Identity uncertain -> A1
Attestation failed -> A0 / STOP
```

Principle:

```text
Trust down => Capability down
```

---

## 28. Agent Risk Score — ARS

The conceptual model uses:

```text
ARS =
  wA*Autonomy
+ wP*Privilege
+ wD*DataSensitivity
+ wT*ToolPower
+ wN*NetworkReach
+ wG*Delegation
+ wI*Impact
+ wB*BehaviorAnomaly
```

The reference implementation uses a simplified, auditable version normalized between 0 and 100.

Example response:

| ARS | Reference treatment |
|---:|---|
| 0–20 | allow |
| 21–40 | allow + telemetry |
| 41–60 | restrict / step-up |
| 61–80 | require human approval |
| 81–90 | quarantine |
| 91–100 | revoke / kill |

These thresholds are **not universal** and must be calibrated by domain, impact, functional safety, regulatory risk, and risk appetite.

---

## 29. Blast Radius

For each agent, it should be possible to answer:

> If this agent is compromised now, what is the maximum possible damage?

Conceptually:

```text
BlastRadius(A) = f(
    Privileges,
    Reach,
    Data,
    Tools,
    Delegation,
    FinancialAuthority,
    PhysicalAuthority
)
```

Blast radius should be reduced using:

- microsegmentation;
- short-lived credentials;
- capability tokens;
- sandboxing;
- egress control;
- quotas;
- namespaces;
- policy scopes;
- delegation limits.

---

## 30. Agent Risk Register

Each agent must have a risk record.

| Field | Example |
|---|---|
| Agent ID | invoice-agent |
| Owner | Finance |
| Class | L2 |
| Autonomy | A3 |
| Data | confidential |
| External access | no |
| Delegation | yes |
| Risk owner | CFO/CISO |
| Inherent risk | 72 |
| Controls | 14 |
| Residual risk | 31 |
| Accepted by | Risk Committee |
| Review | quarterly |

The repository includes an example in `specs/risks/risk-register.csv`.

---

## 31. Expanded Attack Surface

In Edge AI, the surface can be represented as:

```text
AttackSurface =
  Network
+ Software
+ Identity
+ Data
+ Model
+ Agent
+ Tool
+ Memory
+ RAG
+ SupplyChain
+ Physical
```

AI does not replace previous attack surfaces. It **adds new surfaces**.

---

## 32. Integrated Threat Modeling

The project combines:

```text
ThreatModel =
    STRIDE
  + MITRE ATT&CK
  + MITRE ATLAS
  + OWASP GenAI
  + OWASP Agentic
  + Edge/MEC threats
  + OT/ICS threats
  + DomainSpecificThreats
```

STRIDE remains useful, but by itself it does not cover:

- goal hijacking;
- prompt injection;
- indirect prompt injection;
- memory poisoning;
- RAG poisoning;
- tool abuse;
- agent impersonation;
- delegation abuse;
- autonomy escalation;
- agent collusion;
- unsafe actuation.

---

## 33. Initial Threat Catalog

The project considers, among others:

- **T-001** Prompt Injection;
- **T-002** Indirect Prompt Injection;
- **T-003** Memory Poisoning;
- **T-004** RAG Poisoning;
- **T-005** Tool Abuse;
- **T-006** Agent Impersonation;
- **T-007** Delegation Escalation;
- **T-008** Agent Hijacking;
- **T-009** Data Exfiltration;
- **T-010** Model Supply Chain Attack;
- **T-011** Tool Supply Chain Attack;
- **T-012** Autonomous Lateral Movement;
- **T-013** Agent Collusion;
- **T-014** Sensor Manipulation;
- **T-015** Unsafe Actuation;
- **T-016** Identity Theft;
- **T-017** Excessive Agency;
- **T-018** Resource Exhaustion.

Files under `specs/threat-model/` contain detailed descriptions and crosswalks.

---

## 34. Attack Path Analysis

An attack path may emerge only through composition:

```text
Untrusted Document
        ↓
Indirect Prompt Injection
        ↓
Agent
        ↓
Tool Invocation
        ↓
Internal Database
        ↓
External API
```

Therefore:

```text
Risk(System) != Sum(Risk(Component_i))
```

Emergent risks arise from relationships, chains, and collective behavior.

---

## 35. RAG Security

A production implementation should provide for:

- source provenance;
- document signing when applicable;
- classification;
- ingestion validation;
- malware/content scanning;
- access control;
- tenant isolation;
- vector isolation;
- embedding integrity;
- retrieval authorization.

Principle:

```text
CanRetrieve(Document) != CanDisclose(Document)
```

---

## 36. Agent Memory Security

Persistent memory should include metadata such as:

```text
origin
timestamp
agent
classification
trust_score
expiry
integrity
```

Information stored by an agent must not automatically become “trusted truth.”

---

## 37. Registries

### Agent Registry

Source of truth for:

- identity;
- owner;
- purpose;
- class;
- autonomy;
- model;
- tools;
- data access;
- network access;
- delegation;
- risk;
- controls;
- lifecycle.

### Model Registry

Should record, as required:

- model ID;
- version;
- provider;
- provenance;
- checksum/digest;
- deployment zone;
- known risks;
- security tests;
- approval status.

### Tool Registry

Tools should have:

- identity;
- allowed operations;
- risk;
- network scope;
- authentication requirements;
- logging requirements;
- policy requirements.

---

## 38. AI-BOM, Agent-BOM, and SBOM

The complete composition can be represented as:

```text
SystemBOM = SBOM + AI-BOM + Agent-BOM
```

### AI-BOM

May include:

- models;
- prompts;
- system prompts;
- datasets;
- embeddings;
- vector databases;
- tools;
- APIs;
- MCP servers;
- frameworks;
- containers;
- firmware;
- edge hardware.

### Agent-BOM

Specifically records:

- agents;
- roles;
- relationships;
- capabilities;
- delegations;
- tools;
- models;
- trust zones.

The repository contains examples under `bom/`.

---

## 39. Supply Chain Security

No critical artifact should reach production without proportional mechanisms for:

- signature verification;
- provenance;
- dependency scan;
- vulnerability scan;
- policy compliance;
- model validation;
- artifact attestation.

---

## 40. Edge Node Security

According to criticality, Edge nodes should consider:

- Secure Boot;
- Measured Boot;
- TPM or hardware root of trust;
- disk encryption;
- workload isolation;
- container sandbox;
- device identity;
- remote attestation;
- firmware signing;
- least privilege;
- secure update;
- tamper detection.

The trust decision for a node can be represented as:

```text
Trust(node) = Identity + IntegrityState + Attestation
```

---

## 41. Zero-Trust Agentic Mesh — ZTAM

ZTAM extends the service-mesh concept to agentic interactions.

```text
Agent A
   ↓
Agent Proxy
   ↓
Identity + Policy + Risk
   ↓
Encrypted Mesh
   ↓
Agent Proxy
   ↓
Agent B
```

It may contain:

- Agent Proxy;
- Identity Proxy;
- Policy Proxy;
- Tool Proxy;
- A2A Gateway;
- Egress Gateway;
- Telemetry Sidecar;
- Evidence Collector.

The architecture is vendor-neutral.

---

## 42. Egress Governance

Agents should not have unrestricted Internet access by default.

All relevant egress must be:

- identified;
- authorized;
- classified;
- logged;
- rate-limited;
- policy-controlled.

---

## 43. Risk-Based Human-in-the-Loop

The architecture does not require human approval for everything.

```text
LOW RISK     -> autonomous
MEDIUM RISK  -> autonomous + monitoring
HIGH RISK    -> step-up / human approval
CRITICAL     -> multi-party authorization / deny
```

The goal is to preserve automation without sacrificing accountability for irreversible or high-impact actions.

---

## 44. Segregation of Duties — SoD

No critical agent should independently accumulate all incompatible stages of a transaction.

Example:

```text
Agent A -> proposes payment
Agent B -> validates invoice
Policy Engine -> validates controls
Human C -> authorizes
Bank API -> executes
```

In particular:

```text
create + approve + execute
```

must not exist under the same authority when the domain requires SoD.

---

## 45. Agentic Observability

Traditional logs are insufficient.

Depending on criticality, capture:

- Agent ID;
- Session ID;
- Trace ID;
- Model;
- Model version;
- Intent;
- prompt hash or secure reference;
- context sources;
- RAG sources;
- memory references;
- plan;
- tool calls;
- delegations;
- policy decisions;
- risk score;
- human approvals;
- actions;
- outputs;
- errors;
- costs;
- latency.

---

## 46. Distributed Trace and Decision Provenance

A multi-agent task must be reconstructable:

```text
Human
  └── Agent-A
       ├── Agent-B
       │    └── Tool-X
       └── Agent-C
            └── Database
```

For critical actions, provenance must answer:

```text
who
what
why
when
model
policy
data sources
approvals
risk
result
```

---

## 47. Evidence-as-Code

The objective is for controls to produce evidence automatically.

Example:

```yaml
evidence:
  control: CTL-IAM-002

  requirement:
    agent_identity_required: true

  observation:
    identity_verified: true

  agent:
    invoice-agent-01

  timestamp:
    2026-09-05T22:00:00-03:00
```

This supports **Continuous Compliance** instead of purely periodic auditing.

---

## 48. Continuous GRC

The intended transformation is:

```text
Regulation
    ↓
Requirement
    ↓
Risk
    ↓
Control
    ↓
Machine-readable Policy
    ↓
Runtime Enforcement
    ↓
Telemetry
    ↓
Evidence
    ↓
Compliance Status
```

Thus, GRC ceases to be only documentation and becomes part of runtime operation.

---

## 49. Governance Knowledge Graph

Conceptually:

```text
Regulation
    ↓
Requirement
    ↓
Risk
    ↓
Control
    ↓
Policy
    ↓
Agent
    ↓
Capability
    ↓
Tool
    ↓
Data
    ↓
Evidence
```

This model enables bidirectional traceability:

- from regulation to evidence;
- from evidence to requirement;
- from agent to risks and controls;
- from control to implementation and test.

---

## 50. Security Digital Thread

```text
Business Requirement
        ↓
Regulatory Requirement
        ↓
Risk
        ↓
Threat
        ↓
Security Requirement
        ↓
Architecture Decision
        ↓
Control
        ↓
Code
        ↓
Test
        ↓
Deployment
        ↓
Runtime Evidence
```

The project materializes this concept through specifications, the control catalog, tests, and the traceability matrix.

---

## 51. Hierarchical and Distributed GRC

```text
Enterprise GRC
     │
     ▼
Global Policies
     │
     ▼
Regional Governance
     │
     ▼
MEC Governance
     │
     ▼
Edge Governance
     │
     ▼
Agent Enforcement
```

If intelligence and execution are distributed, security and governance must also be distributed.

---

## 52. SDD — Spec-Driven Development

The adopted precedence is:

```text
Business / Regulatory Requirement
        ↓
MASTER-SPEC
        ↓
Security Invariants
        ↓
Architecture / C4 / DFD / Trust Zones
        ↓
Threat & Risk Specifications
        ↓
Control Specifications
        ↓
Policy Specifications
        ↓
Agent / Model / Tool Manifests
        ↓
Implementation
        ↓
Tests
        ↓
Runtime Evidence
```

Code is **not the only source of truth**.

An implementation change that contradicts a specification must:

1. fail in the pipeline; or
2. require a formal specification change;
3. require an ADR when architectural;
4. require a new risk analysis when applicable.

---

## 53. SDD Traceability

The chain used by the project is:

```text
Requirement
    ↓
Threat / Risk
    ↓
Control
    ↓
Policy
    ↓
Implementation
    ↓
Test
    ↓
Evidence
```

The file:

```text
specs/traceability/requirements-controls-tests.csv
```

links requirements to controls, tests, and expected evidence.

---

## 54. MASTER-SPEC

`MASTER-SPEC.md` defines the project's highest-level normative contract.

It should be consulted before significant architectural changes.

More specific artifacts must remain consistent with it unless an ADR documents a deliberate change in decision.

---

## 55. Architecture Decision Records — ADR

Important decisions should have an ADR containing, at minimum:

```text
Title
Context
Decision
Alternatives
Security impact
Risk impact
Compliance mapping
Rollback strategy
```

The repository includes initial ADRs under `specs/adrs/`.

---

## 56. Security Control Catalog

Each control should contain:

```yaml
control:
  id: CTL-AGENT-001
  name: Agent cryptographic identity
  requirement: All agents SHALL possess workload identity
  threats:
    - impersonation
    - spoofing
  frameworks:
    - NIST-ZTA
    - STRIDE
  verification: automated
  evidence: identity-attestation-log
```

Suggested families:

```text
AGT — Agent
IAM — Identity
MOD — Model
RAG — Retrieval
MEM — Memory
TOL — Tool
DAT — Data
NET — Network
EDG — Edge
MEC — MEC
PHY — Physical
GOV — Governance
RSK — Risk
MON — Monitoring
IR  — Incident Response
SUP — Supply Chain
BCP — Resilience
```

---

## 57. Formal Methods

The “formal” character of the project is not limited to documentation.

The repository contains:

```text
formal/tla/SGAEIA.tla
formal/alloy/sgaeia.als
```

These models express properties such as:

- an agent without identity does not execute;
- L4+A5 is not authorized;
- delegation does not increase authority;
- invalid states must not reach RUNNING;
- critical operations depend on authorization.

In addition, Python state-space exploration exists in:

```text
tests/formal/test_invariants_state_space.py
```

### Important

The TLA+ and Alloy files are **formal specifications provided as a basis for model checking**, but this repository version does not assume that the TLA+/Alloy model checkers are installed in the local environment.

Equivalent invariants are also exercised by the Python test suite.

---

## 58. Lifecycle Governance

Expected states:

```text
REGISTERED
    │
    ▼
VALIDATED
    │
    ▼
AUTHORIZED
    │
    ▼
RUNNING
    │
 ┌──┼───────────────┐
 │  │               │
 ▼  ▼               ▼
PAUSED QUARANTINED REVOKED
 │                  │
 ▼                  ▼
RUNNING           TERMINATED
```

Transitions such as:

```text
UNKNOWN -> RUNNING
```

must be prohibited.

Complete lifecycle:

```text
Design
-> Register
-> Validate
-> Approve
-> Deploy
-> Monitor
-> Review
-> Retire
```

---

## 59. Kill Switch and Reversible Autonomy

Every agent with relevant risk must support, as required:

```text
pause
disable
isolate
revoke_credentials
revoke_tools
disconnect_network
rollback
terminate
```

Hierarchical architecture:

```text
SOC / GRC
   │
   ▼
Emergency Control Plane
   │
   ├── revoke identity
   ├── disable agent
   ├── revoke tools
   ├── remove network
   ├── quarantine node
   └── stop actuation
```

It must be possible to act on:

- a single execution;
- an agent;
- a group of agents;
- an Edge node;
- a MEC region;
- a model version;
- a tool;
- the entire agent mesh.

---

## 60. Emergency Policy

Conceptual example:

```text
IF systemic_attack == true
THEN
  external_agent_calls = DENY
  new_delegations      = DENY
  critical_actions     = HUMAN_ONLY
  edge_autonomy        = REDUCED
```

---

## 61. Security-by-Design, Security-First, and Shift Everywhere

Security starts with requirements.

```text
Requirements
    ↓
Threat Modeling
    ↓
Architecture
    ↓
Development
    ↓
Testing
    ↓
Deployment
```

But agentic systems change at runtime. Therefore:

```text
Shift Left
+
Shift Right
+
Runtime Governance
=
Shift Everywhere
```

---

## 62. Security Gates

The pipeline is designed to incorporate:

```text
SPEC
 ↓
Architecture Validation
 ↓
Threat Modeling Gate
 ↓
Security Requirements Gate
 ↓
Code
 ↓
SAST
 ↓
SCA
 ↓
SBOM / AI-BOM / Agent-BOM
 ↓
Policy Tests
 ↓
Agent Security Tests
 ↓
Integration
 ↓
Adversarial Tests
 ↓
Deployment
 ↓
Runtime Validation
 ↓
Continuous Monitoring
```

The current implementation contains stubs and gates compatible with enterprise extension.

---

## 63. Planned Tests

### Traditional

- SAST;
- DAST;
- SCA;
- IaC scanning;
- secret scanning;
- container scanning;
- API security testing.

### AI

- prompt injection;
- indirect prompt injection;
- jailbreak;
- RAG poisoning;
- model abuse;
- data leakage.

### Agentic

- tool abuse;
- delegation abuse;
- identity spoofing;
- capability escalation;
- excessive agency;
- agent loops;
- collusion scenarios.

### Edge

- offline operation;
- node compromise;
- attestation failure;
- policy cache expiry;
- network partition;
- physical tampering.

### Cyber-physical

- unsafe action;
- sensor spoofing;
- actuator abuse;
- fail-safe;
- emergency stop.

---

## 64. Chaos Security Engineering

Recommended scenarios:

```text
PDP unavailable
Identity provider unavailable
Cloud disconnected
Model unavailable
Tool returns malicious data
Agent compromised
MEC unavailable
Clock manipulation
Certificate expiry
RAG poisoned
```

The system must degrade safely.

---

## 65. Definition of Done — DoD

An agent should be considered production-ready only when:

```text
DoD =
  Specification
  AND Identity
  AND ThreatModel
  AND RiskAssessment
  AND Controls
  AND Tests
  AND Evidence
  AND Approval
```

---

## 66. Production Admission Controller

```text
Agent Artifact
     ↓
Admission Controller
     │
     ├── Spec exists?
     ├── Owner exists?
     ├── Risk accepted?
     ├── AI-BOM valid?
     ├── Signature valid?
     ├── Threat model?
     ├── Tests passed?
     ├── Policy compliant?
     └── Kill-switch available?
             │
        YES ─┴─ NO
         │      │
      Deploy   Reject
```

In addition, critical actions must have **Runtime Admission** via PDP/PEP.

---

## 67. Repository Structure

```text
SGAEIA/
├── MASTER-SPEC.md
├── README.md
├── SECURITY.md
├── CONTRIBUTING.md
├── PROJECT-MANIFEST.md
├── pyproject.toml
├── Makefile
├── .github/workflows/security-ci.yml
├── docs/
├── specs/
│   ├── acceptance/
│   ├── adrs/
│   ├── agents/
│   ├── api/
│   ├── architecture/
│   ├── compliance/
│   ├── controls/
│   ├── models/
│   ├── requirements/
│   ├── risks/
│   ├── threat-model/
│   ├── tools/
│   └── traceability/
├── schemas/
├── policies/rego/
├── src/sgaeia/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── security/
│   ├── adversarial/
│   └── formal/
├── formal/
│   ├── tla/
│   └── alloy/
├── deploy/
│   ├── docker/
│   └── k8s/
├── observability/
├── bom/
├── examples/
└── scripts/
```

The complete list is maintained in `PROJECT-MANIFEST.md`.

---

## 68. Current Reference Implementation

The Python implementation demonstrates minimal capabilities for:

- agent registration and validation;
- risk calculation;
- policy decision;
- delegation validation;
- basic enforcement;
- evidence generation;
- kill switch.

The endpoint:

```text
POST /v1/authorize
```

evaluates a proposed action based on:

- identity;
- classification;
- autonomy;
- capabilities;
- context;
- risk;
- agent state;
- critical rules.

---

## 69. How to Run

### Basic Requirements

- Python compatible with `pyproject.toml`;
- installed dependencies;
- local development environment.

### Tests

```bash
python -m pytest -q
```

### Specification Validation

```bash
python scripts/validate_specs.py
```

### Generate Agent-BOM

```bash
python scripts/generate_agent_bom.py
```

### Local API

```bash
uvicorn sgaeia.api:app --app-dir src --host 0.0.0.0 --port 8080
```

### Health Check

```bash
curl http://localhost:8080/health
```

---

## 70. Authorization Flow Example

```text
Agent Intent
    ↓
Identity Validation
    ↓
Capability Validation
    ↓
Delegation Validation
    ↓
Risk Evaluation
    ↓
Policy Decision — PDP
    ↓
Policy Enforcement — PEP
    ↓
Human Approval — when required
    ↓
Execution
    ↓
Telemetry + Evidence + Trace
```

The agent **proposes**. The architecture **authorizes or denies**.

---

# 71. Replaceable Integration Points

## 71.1 Technology-Neutrality Principle

This project was designed to separate:

```text
Security / Governance Semantics
            │
            ▼
Reference Interface / Contract
            │
            ▼
Replaceable Technology
```

In other words, security should not depend on a specific brand or product.

SPIFFE/SPIRE, OPA/Rego, OpenTelemetry, Envoy/Istio, and other cited components are **reference implementations or integration examples**.

They may be replaced as long as the new solution preserves the **semantic contract and architectural invariants**.

---

## 71.2 Replacement Matrix

| Domain | Project reference | May be replaced by | Minimum contract that must remain |
|---|---|---|---|
| Workload / Agent Identity | SPIFFE/SPIRE | cloud workload identity, custom PKI, service identity platform, NHI platform | unique and verifiable identity, rotation, short lifetime where possible, revocation, workload binding |
| PKI / Certificates | X.509/mTLS | enterprise CA, cloud CA, HSM-backed PKI | strong authentication, integrity, rotation, revocation, explicit trust domain |
| Policy Engine | OPA/Rego | Cedar, Zanzibar-style engine, cloud IAM policy engine, custom PDP | externalized decision, deterministically auditable behavior, default deny, policy versioning |
| PEP | middleware/API enforcement | Envoy filter, API gateway, service mesh, sidecar, library interceptors | no protected action bypasses enforcement |
| Service / Agent Mesh | Istio/Envoy/Linkerd model | Cilium service mesh, cloud mesh, custom proxy fabric | mTLS, identity propagation, policy hooks, telemetry, egress control |
| Observability | OpenTelemetry | vendor APM, cloud-native telemetry, custom event bus | trace ID, logs, metrics, correlation, exportability, adequate clock consistency |
| Evidence Store | reference JSON/files | WORM storage, object storage, immutable log, ledger, GRC evidence platform | integrity, retention, provenance, access control, timestamp, queryability |
| SIEM/SOC | conceptual integration | any SIEM/SOAR/SOC platform | event ingestion, correlation, alerting, investigation, response hooks |
| GRC | specifications and evidence mapping | GRC platform, control-monitoring platform, knowledge graph | requirement→control→evidence traceability and ownership |
| Risk Engine | Python reference | rules engine, Bayesian model, graph risk engine, ML-assisted risk engine | explainable score, bounds, versioned inputs, policy-safe behavior |
| Registry | YAML/files + Python | PostgreSQL, service catalog, CMDB, graph DB, cloud registry | source of truth, owner, version, lifecycle, auditability |
| Agent Registry | manifests | dedicated agent registry/platform | identity, owner, purpose, capabilities, autonomy, risk, lifecycle |
| Model Registry | manifests | MLflow, cloud model registry, enterprise AI catalog | model ID/version, provenance, approval, deployment status |
| Tool Registry | manifests | API catalog, service catalog, MCP registry | tool identity, operations, risk, authentication, scopes, audit |
| RAG / Vector Store | conceptual interface | pgvector, Milvus, Pinecone, Weaviate, Elasticsearch, cloud vector DB | tenant isolation, AuthZ, provenance, classification, retrieval policy |
| Secrets | environment/reference | Vault, KMS, cloud secret manager, HSM | encryption, least privilege, rotation, revocation, audit |
| Messaging / Event Bus | decoupled | Kafka, NATS, Pulsar, RabbitMQ, cloud pub/sub | authenticated producers/consumers, integrity, partitioning, replay controls |
| State Store | in-memory/reference | PostgreSQL, Redis, distributed KV | adequate consistency, isolation, durability according to criticality |
| API Gateway | FastAPI direct/reference | Kong, Apigee, Envoy Gateway, cloud API gateway | AuthN/AuthZ hooks, rate limiting, logging, schema validation |
| Container Runtime | Docker reference | containerd, CRI-O, microVM, unikernel | isolation, image provenance, runtime controls |
| Orchestrator | Kubernetes reference | K3s, OpenShift, Nomad, edge orchestrator, cloud container platform | lifecycle, identity binding, isolation, admission, policy integration |
| Edge Orchestration | Kubernetes manifests | K3s, KubeEdge, Akri, vendor edge stack, ETSI-aligned MEC platform | local policy enforcement, offline safety, telemetry buffering, node identity |
| Remote Attestation | conceptual hook | TPM attestation, confidential computing attestation, cloud attestation service | signed/measurable platform state, freshness, trust-decision integration |
| SBOM | CycloneDX example | SPDX or equivalent | component inventory, version, dependency identity, machine readability |
| AI-BOM / Agent-BOM | project schemas | enterprise AI inventory format | models/agents/tools/dependencies and relationships |
| Formal Verification | TLA+ / Alloy | PlusCal, Coq, Isabelle, Lean, model checker, state-machine verifier | explicit invariants and mechanically checkable properties where required |
| CI/CD | GitHub Actions reference | GitLab CI, Jenkins, Azure DevOps, Tekton, Argo | mandatory gates, evidence, traceability, policy enforcement |
| IaC | Kubernetes YAML reference | Terraform, Pulumi, Helm, Crossplane | versioned infrastructure intent, policy testing, drift visibility |
| Supply-chain Attestation | conceptual | Sigstore, in-toto, SLSA tooling, enterprise signing | provenance, signatures/attestations, verification before admission |
| Incident Response | kill-switch reference | SOAR playbook, EDR response, mesh isolation, platform controller | revoke, isolate, disable, quarantine, trace, evidence preservation |

---

## 71.3 Rule for Component Replacement

A technology should replace another only when it preserves, at minimum:

```text
Functional Contract
AND Security Contract
AND Audit Contract
AND Failure Contract
AND Revocation Contract
```

### Functional Contract

The new solution must fulfill the intended architectural function.

### Security Contract

It must preserve the relevant security invariants.

### Audit Contract

It must generate sufficient evidence for investigation and compliance.

### Failure Contract

It must have defined behavior when unavailable or degraded.

### Revocation Contract

It must allow authority, credentials, sessions, or capabilities to be revoked when required.

---

## 71.4 Example — Replacing SPIFFE/SPIRE

SPIFFE/SPIRE may be replaced.

The alternative solution, however, must preserve:

- workload identity independent of a human user;
- unique identity;
- identity binding to the actual workload;
- credential rotation;
- revocation;
- mutual authentication when required;
- an explicit trust domain;
- attestation support or an equivalent mechanism for critical agents.

A simple static API key shared by multiple agents is **not semantically equivalent**.

---

## 71.5 Example — Replacing OPA/Rego

OPA/Rego is only the Policy-as-Code reference.

A replacement solution must provide:

- policy externalized from the agent;
- versioning;
- auditable decisions;
- sufficient determinism for compliance;
- default deny;
- support for automated tests;
- separation between Policy Decision and Agent Reasoning;
- support for context, identity, and risk;
- explicit failure handling.

The LLM cannot be used as the sole replacement for the PDP for critical actions.

---

## 71.6 Example — Replacing the Service Mesh

Istio/Envoy/Linkerd are examples.

An architecture without a service mesh may still implement ZTAM, provided it can ensure:

- mTLS or equivalent protection;
- identity propagation;
- policy enforcement;
- egress control;
- distributed observability;
- rate limiting;
- isolation;
- revocation.

---

## 71.7 Example — Replacing OpenTelemetry

OpenTelemetry is an interoperability reference.

The alternative solution must preserve:

```text
Trace-ID
Agent-ID
Intent
Policy Decision
Risk Score
Tool Call
Delegation
Action Result
Timestamp
Evidence Link
```

Without distributed correlation, multi-agent incident investigation becomes incomplete.

---

## 71.8 Example — Replacing the Risk Engine

The provided ARS algorithm is deliberately simple.

It may be replaced by:

- statistical scoring;
- risk graph;
- attack-path analysis;
- Bayesian network;
- rules engine;
- hybrid model;
- enterprise risk analytics engine.

However, the solution must be:

- explainable for critical decisions;
- versioned;
- testable;
- bounded by policy;
- resilient to missing or manipulated inputs;
- able to produce evidence explaining the decision.

---

## 71.9 Example — Replacing Kubernetes

Kubernetes is only a reference deployment/orchestration implementation.

It may be replaced by another platform, including one specific to Edge/MEC, provided it preserves:

- workload identity;
- lifecycle management;
- isolation;
- network policy or equivalent;
- admission controls;
- secret management;
- observability;
- rollback;
- the ability to execute kill/quarantine actions.

---

## 71.10 Example — Replacing Evidence Storage

Evidence-as-Code does not depend on local JSON files.

In production, an organization may use:

- immutable object storage;
- WORM;
- SIEM;
- ledger;
- auditable database;
- governed data lake;
- GRC platform.

The requirement is to preserve:

- integrity;
- origin;
- timestamps;
- retention;
- access control;
- correlation;
- chain of custody when applicable.

---

## 72. Recommended Integration Contracts

When replacing technologies, the project recommends explicit interfaces.

### Identity Provider Contract

```text
verify_identity(subject)
issue_identity(workload)
revoke_identity(subject)
attest(subject)
get_trust_domain(subject)
```

### Policy Decision Contract

```text
evaluate(identity, capability, resource, context, risk) -> decision
```

### Policy Enforcement Contract

```text
enforce(decision, action)
```

### Risk Contract

```text
score(agent, intent, context, behavior) -> score + factors
```

### Registry Contract

```text
register(entity)
get(entity_id)
version(entity_id)
revoke(entity_id)
list_relationships(entity_id)
```

### Evidence Contract

```text
record(event)
seal(event)
query(trace_id)
export(control_id)
```

### Kill-Switch Contract

```text
pause(scope)
quarantine(scope)
revoke(scope)
terminate(scope)
```

These contracts are more important than the concrete technology used.

---

## 72A. Formal Integration Port Specification — IPS

This section is **normative** for integration replaceability in SGAEIA.

The architecture does not treat SPIFFE/SPIRE, OPA/Rego, OpenTelemetry, a service mesh, Kubernetes, Kafka, PostgreSQL, or any specific product as an inseparable part of the core. The stable element is the **security and governance semantics of the integration port**.

The formal model is:

```text
Security / Governance Semantics
            ↓
Integration Port Specification (IPS)
            ↓
Transport Contract (OpenAPI / AsyncAPI / local interface)
            ↓
Adapter
            ↓
Replaceable Technology
```

### 72A.1 IPS Structure

Each port in `specs/integrations/ports/*.port.yaml` SHALL declare:

```text
Functional Contract
Security Contract
Audit Contract
Failure Contract
Revocation Contract
```

Therefore:

```text
ConformantReplacement =
  FunctionalPass
  AND SecurityPass
  AND AuditPass
  AND FailurePass
  AND RevocationPass
  AND NoSecurityInvariantViolation
```

Protocol or JSON compatibility **is not sufficient** for architectural equivalence.

### 72A.2 Formalized Ports

The current version formalizes, among others:

| Port | Responsibility |
|---|---|
| `IP-IDENTITY` | workload/agent identity, attestation, and revocation |
| `IP-PDP` | external policy decision |
| `IP-PEP` | enforcement before action |
| `IP-RISK` | dynamic risk evaluation |
| `IP-REGISTRY` | inventory and lifecycle of governed entities |
| `IP-EVIDENCE` | evidence, sealing, correlation, and export |
| `IP-KILL` | pause/quarantine/revoke/terminate |
| `IP-OBS` | agentic telemetry and tracing |
| `IP-BUS` | asynchronous control/governance events |
| `IP-MESH` | Zero Trust agent-to-agent/service communication |
| `IP-STATE` | governed persistent state |
| `IP-EDGE` | Edge/MEC orchestration with safe degradation |

### 72A.3 Machine-Readable Contracts

Reference HTTP contracts are located in:

```text
specs/integrations/openapi/
```

using **OpenAPI 3.2.0**.

Event-driven contracts are located in:

```text
specs/integrations/asyncapi/
```

using **AsyncAPI 3.1.0**.

These formats describe transport and interoperability. The semantic contract of the port remains the normative authority because a valid OpenAPI/AsyncAPI document alone does not prove fail-safe behavior, revocability, or adequate evidence.

### 72A.4 Qualification of a Replacement Technology

A replacement SHALL provide a dossier containing:

1. implementation version and supported port;
2. functional mapping of all operations;
3. AuthN/AuthZ, identity, integrity, and isolation analysis;
4. behavior during timeout, dependency loss, and partition;
5. measured revocation propagation time;
6. produced evidence and its correlation;
7. threat model for newly introduced surfaces;
8. positive and negative tests;
9. emergency rollback/disable;
10. residual risk and owner for any deviation.

The methodology is specified in:

```text
specs/integrations/replacement-qualification.md
```

### 72A.5 Conformance Levels

```text
IPS-C0  Documented
IPS-C1  Functional
IPS-C2  Secure
IPS-C3  Governed
```

`IPS-C3` adds auditability, evidence, revocation, traceability, and lifecycle to functional and security properties. Critical ports intended for production SHOULD reach IPS-C3.

### 72A.6 Failure Semantics Are Part of the API

In this architecture, failure is not merely a technical exception. It changes authority.

Examples:

```text
PDP unavailable + critical action
=> DENY

Identity unverifiable + privileged action
=> DENY

Cloud disconnected + Edge critical workload
=> reduce/preserve authority; never increase authority

Evidence backend unavailable
=> buffer critical evidence; never silently discard it
```

Thus, two products that execute the same call during normal operation may **not** be equivalent substitutes if one fails open.

### 72A.7 Revocation as an Architectural Requirement

For each relevant port, the project records `maxPropagationSeconds`.

Qualification must demonstrate that:

```text
RevocationRequested(t0)
=> AuthorityUnavailable(t <= t0 + MaxPropagation)
```

The exact value is domain-specific, but the property of revocability is not optional.

### 72A.8 Integration with SDD and GRC

IPS enters the SDD chain:

```text
Requirement
    ↓
Architecture / ADR
    ↓
Integration Port
    ↓
Adapter
    ↓
Conformance Test
    ↓
Runtime Evidence
    ↓
GRC / Audit
```

In this way, changing a vendor is no longer merely an operational decision; it becomes a verifiable architectural change with explicit evidence and risk impact.

### 72A.9 Added Normative Files

```text
specs/integrations/README.md
specs/integrations/ports/*.port.yaml
specs/integrations/openapi/*.openapi.yaml
specs/integrations/asyncapi/*.asyncapi.yaml
specs/integrations/conformance-matrix.csv
specs/integrations/replacement-qualification.md
specs/integrations/versioning-and-compatibility.md
specs/integrations/security-requirements.md
schemas/integration-port.schema.json
specs/adrs/ADR-004-integration-port-contracts.md
tests/specification/test_integration_port_contracts.py
```

The pipeline validates that every port contains the five contractual dimensions and that transport specifications use the declared baselines.

---

## 72B. Adapter Conformance Framework — ACF

This section is **normative** for implementing and qualifying the concrete adapters that materialize Integration Ports.

IPS defines **what must remain true**. The Adapter Conformance Framework defines **how a concrete technology demonstrates that it preserves those properties**.

```text
Integration Port Specification
          │
          ▼
   Adapter Profile
          │
          ▼
Executable Adapter Contract
          │
          ▼
Shared Conformance Harness
          │
   ┌──────┼───────────┐
   ▼      ▼           ▼
Failure  Evidence   Revocation
Tests    Tests      Tests
   │      │           │
   └──────┼───────────┘
          ▼
Conformance Evidence
          │
          ▼
Deployment Admission / GRC
```

### 72B.1 Principle: Adapters Implement Ports; They Do Not Redefine the Architecture

A concrete adapter SHALL be bound to exactly one Integration Port in its `AdapterProfile`.

The relationship is:

```text
Adapter : Technology → IntegrationPortSemantics
```

Not:

```text
Technology → NewSecuritySemantics
```

Thus, SPIRE, OPA, Istio, NATS, Kafka, PostgreSQL, Kubernetes, K3s, and OpenTelemetry are replaceable implementations. None of them, by itself, becomes the normative authority of the architecture.

### 72B.2 Executable Reference Adapters

Version 0.3.0 includes code adapters under:

```text
src/sgaeia/integrations/
├── contracts.py
├── registry.py
├── transports.py
├── conformance.py
└── adapters/
    ├── identity_spire.py
    ├── pdp_opa.py
    ├── mesh_istio.py
    ├── observability_otel.py
    ├── bus_nats.py
    ├── bus_kafka.py
    ├── state_postgres.py
    ├── edge_kubernetes.py
    └── edge_k3s.py
```

Adapters use **transport injection**. Therefore, they may operate over:

- HTTP/JSON facade;
- sidecar;
- Unix socket proxy;
- service gateway;
- local implementation;
- test double;
- bridge to gRPC or native APIs.

The SGAEIA core does not need to import a vendor SDK to preserve architectural semantics.

### 72B.3 Concrete Profiles

Manifests are located in:

```text
specs/integrations/adapters/*.adapter.yaml
```

Each profile declares:

```text
adapter id
port id
adapter version
concrete implementation
reference baseline
assurance target
verification scope
failure mode
evidence outputs
alternative implementations
qualification notes
```

Current examples:

| Adapter | Port | Reference implementation | Target |
|---|---|---|---|
| `ADP-SPIRE-IDENTITY` | `IP-IDENTITY` | SPIFFE/SPIRE | IPS-C3 |
| `ADP-OPA-PDP` | `IP-PDP` | Open Policy Agent | IPS-C3 |
| `ADP-ISTIO-MESH` | `IP-MESH` | Istio/Envoy | IPS-C3 |
| `ADP-OTEL-OBS` | `IP-OBS` | OpenTelemetry Collector | IPS-C2 |
| `ADP-NATS-BUS` | `IP-BUS` | NATS/JetStream | IPS-C2 |
| `ADP-KAFKA-BUS` | `IP-BUS` | Apache Kafka | IPS-C2 |
| `ADP-POSTGRES-STATE` | `IP-STATE` | PostgreSQL | IPS-C2 |
| `ADP-K8S-EDGE` | `IP-EDGE` | Kubernetes | IPS-C3 |
| `ADP-K3S-EDGE` | `IP-EDGE` | K3s | IPS-C3 |

The coexistence of two adapters for `IP-BUS` and two for `IP-EDGE` is intentional and demonstrates replaceability.

### 72B.4 Progressive Assurance: the Harness Is Not Product Certification

Qualification is explicitly divided into stages:

```text
Q0 Inventory
      ↓
Q1 Contract Harness / IPS-C1
      ↓
Q2 Live Security Qualification / IPS-C2
      ↓
Q3 Governed Production Qualification / IPS-C3
```

#### Q1 / IPS-C1

Validates in the repository:

- adapter ↔ port binding;
- semantic operations;
- structured outputs;
- basic fail-safe behavior;
- attributable evidence;
- logical revocation;
- testable deterministic behavior.

#### Q2 / IPS-C2

Requires a representative or live environment and should test:

- real authentication;
- real authorization;
- mTLS/identity binding;
- timeout;
- dependency loss;
- network partition;
- replay;
- malformed input;
- resource exhaustion;
- downgrade/configuration drift;
- multi-tenant isolation when applicable.

#### Q3 / IPS-C3

Adds:

- revocation propagation measurement;
- correlated operational evidence;
- rollback;
- emergency disable;
- lifecycle/patch policy;
- architecture drift detection;
- residual-risk acceptance;
- GRC approval;
- continuous observability.

Therefore:

```text
ContractHarnessPassed
!=
ProductCertifiedForProduction
```

### 72B.5 Base Contract in Code

Every adapter inherits from `BaseIntegrationAdapter` and has `AdapterMetadata`.

Minimum evidence includes:

```text
trace_id
port_id
subject_id
decision_or_result
timestamp
implementation_id
implementation_version
adapter_id
operation
digest
```

This makes it possible to prove not only that `IP-PDP` responded, but **which concrete implementation and version responded**.

### 72B.6 Adapter Registry

`AdapterRegistry` resolves ports to concrete implementations.

Conceptually:

```text
IP-IDENTITY → ADP-SPIRE-IDENTITY
IP-PDP      → ADP-OPA-PDP
IP-MESH     → ADP-ISTIO-MESH
IP-BUS      → ADP-NATS-BUS OR ADP-KAFKA-BUS
IP-EDGE     → ADP-K8S-EDGE OR ADP-K3S-EDGE
```

A deployment profile selects **one active implementation per port** within that deployment context.

### 72B.7 Transport Injection

The adapter separates:

```text
Semantic Contract
      ↓
Adapter Logic
      ↓
Transport Interface
      ↓
Vendor / Platform API
```

This makes it possible to replace, for example:

```text
HTTP facade → gRPC bridge
```

without changing the PDP contract, or:

```text
NATS → Kafka
```

without changing the `IP-BUS` contract.

Transport does not decide architectural policy; it only materializes the integration.

### 72B.8 Executable Failure Semantics

Reference adapters encode the expected behavior during failures.

#### Identity

```text
SPIRE/identity dependency unavailable
→ identity unverifiable
→ privileged authorization DENY
```

#### PDP

```text
OPA/PDP unavailable
→ critical decision DENY
```

#### Mesh

```text
mTLS absent OR mesh policy unavailable
→ egress DENY
```

#### Observability

```text
collector unavailable
→ bounded buffer-and-retry
→ never silently discard critical evidence
```

#### Event Bus

```text
NATS/Kafka unavailable
→ bounded buffer-and-retry
→ no implicit conversion into unauthorized synchronous action
```

#### State

```text
state backend unavailable
→ write disabled / read-only degraded posture
```

#### Edge

```text
control plane unavailable OR attestation missing for critical workload
→ admission DENY
→ authority does not increase
```

### 72B.9 Independent Revocation

Critical adapters maintain a revocation path that does not depend on the controlled agent.

The property remains:

```text
Autonomy ⇒ Revocability
```

And, for production:

```text
MeasuredRevocationTime <= Port.maxPropagationSeconds
```

The harness demonstrates semantics; Q2/Q3 must measure real propagation for the deployed technology.

### 72B.10 NATS ↔ Kafka Replacement

NATS and Kafka have different APIs, operational models, and internal characteristics. The architecture does not require internal equivalence.

It requires equivalence at the port:

```text
IP-BUS =
  AuthorizedPublish
  + PublisherIdentity
  + ReplayProtectionPolicy
  + DurabilityPolicy
  + Correlation
  + FailureSemantics
  + Evidence
  + Revocation
```

Therefore:

```text
NATS ≈ Kafka
```

only **within the semantic boundary of `IP-BUS`** and only after both satisfy the required assurance level.

### 72B.11 Kubernetes ↔ K3s Replacement

Similarly:

```text
IP-EDGE =
  Admission
  + WorkloadIdentity
  + AttestationContext
  + PolicyEnforcement
  + Quarantine
  + OfflineSafeDegradation
  + Evidence
```

K3s may be appropriate for Edge due to its operational profile, while upstream Kubernetes or enterprise distributions may be suitable in other tiers. The choice does not change the invariants.

### 72B.12 Deployment Profiles

Profiles under:

```text
specs/integrations/deployment-profiles/
```

select concrete adapters for a context.

Edge example:

```text
Identity  = SPIRE
PDP       = OPA
Mesh      = Istio/Envoy
Telemetry = OpenTelemetry
Bus       = NATS
State     = PostgreSQL
Edge      = K3s
```

Enterprise/cloud example:

```text
Identity  = SPIRE
PDP       = OPA
Mesh      = Istio/Envoy
Telemetry = OpenTelemetry
Bus       = Kafka
State     = PostgreSQL
Edge      = Kubernetes
```

These profiles are composition references, not vendor endorsements.

### 72B.13 Reference Baselines and Version Skew

`specs/integrations/reference-baselines.md` records baselines observed in September 2026.

These numbers support documentary reproducibility; they are not a `latest` rule.

Production SHOULD define:

```text
minimum supported version
maximum validated version
upgrade window
security patch SLA
compatibility matrix
rollback version
EOL policy
```

A technology upgrade is an SDD change when it can alter semantics, attack surface, failure mode, or evidence.

### 72B.14 Conformance Report as Evidence-as-Code

The command:

```bash
python scripts/run_adapter_conformance.py
```

produces:

```text
evidence/adapter-conformance.generated.json
```

with:

- adapter;
- port;
- target level;
- checks;
- result;
- assurance scope.

The report explicitly states that this is an **offline contract harness / IPS-C1**, avoiding confusion with live certification.

### 72B.15 CI/CD Gate

The pipeline now executes:

```text
Validate SDD Specs
      ↓
Validate Integration Ports
      ↓
Validate Adapter Profiles
      ↓
Run Unit / Security / Adversarial Tests
      ↓
Run Adapter Conformance Harness
      ↓
Generate BOM / Evidence
```

An adapter change that breaks port binding, failure semantics, or evidence attribution must block the pipeline.

### 72B.16 SDD Traceability of the ACF

The ACF adds requirements `SR-020…SR-024` and controls `CTL-INT-005…CTL-INT-009`.

The chain becomes:

```text
Security Requirement
      ↓
Integration Port
      ↓
Adapter Profile
      ↓
Concrete Adapter Code
      ↓
Contract / Failure Test
      ↓
Conformance Report
      ↓
Deployment Profile
      ↓
Runtime Evidence
      ↓
GRC Decision
```

### 72B.17 Formal Adapter Admission Criterion

```text
AdapterAdmissible(A,P,E) =
    BoundTo(A,P)
AND FunctionalConformance(A,P)
AND SecurityConformance(A,P,E)
AND FailureConformance(A,P,E)
AND EvidenceConformance(A,P,E)
AND RevocationConformance(A,P,E)
AND VersionSupported(A,E)
AND ResidualRiskAccepted(A,E)
```

where:

- `A` = adapter;
- `P` = Integration Port;
- `E` = deployment environment.

### 72B.18 Safe Replacement Criterion

Technology `A₂` may replace `A₁` only when:

```text
Implements(A₁,P)
AND Implements(A₂,P)
AND Assurance(A₂,E) >= RequiredAssurance(P,E)
AND SecurityInvariantsPreserved(A₂,E)
```

Thus, replaceability ceases to be an architectural opinion and gains a **testable criterion, evidence, and a risk decision**.

### 72B.19 Files Added by the Adapter Conformance Framework

```text
src/sgaeia/integrations/
specs/integrations/adapters/
specs/integrations/deployment-profiles/
specs/integrations/adapter-conformance-matrix.csv
specs/integrations/adapter-qualification-procedure.md
specs/integrations/reference-baselines.md
schemas/adapter-profile.schema.json
tests/integration/test_adapter_conformance_framework.py
tests/specification/test_adapter_profiles.py
scripts/run_adapter_conformance.py
evidence/adapter-conformance.generated.json
examples/adapter_stack.py
```

The ACF turns the **vendor-neutral** property into a verifiable and continuously testable architectural characteristic.

---

## 72C. GitHub Public Release Profile — v0.3.2

Publishing SGAEIA as a public repository introduces a new governance and supply-chain surface. For this reason, GitHub publication readiness is treated as part of SDD, not merely as code packaging.

### 72C.1 Principle

```text
PublicVisibility
       !=
ReducedSecuritySemantics
```

Opening the repository to external contributions does not change the identity, authorization, revocation, fail-secure, Evidence-as-Code, and governed-autonomy invariants. Every contribution remains subject to the chain:

```text
Requirement
    ↓
Threat / Risk
    ↓
Control
    ↓
Specification / Policy / Implementation
    ↓
Test
    ↓
Evidence
    ↓
Review / Release
```

### 72C.2 Public Governance Files

The release includes:

- `LICENSE` — Apache License 2.0;
- `NOTICE`;
- `CODE_OF_CONDUCT.md`;
- `CONTRIBUTING.md`;
- `SECURITY.md`;
- `GOVERNANCE.md`;
- `ROADMAP.md`;
- `CHANGELOG.md`;
- `SUPPORT.md`;
- `CITATION.cff`;
- `docs/github-public-release.md`;
- Issue and Pull Request templates;
- Dependabot;
- CI for SDD validation/tests/conformance;
- CodeQL;
- release-validation gate by tag.

### 72C.3 Licensing

The default license for this release is **Apache-2.0**. It was chosen to facilitate use, modification, and redistribution of the reference, with the explicit patent grant provided by the license and preservation of copyright/license conditions. Before publication, the maintainer may replace the license if a different legal or strategic decision is made.

The presence of names such as SPIFFE/SPIRE, OPA, Istio, Envoy, OpenTelemetry, NATS, Kafka, PostgreSQL, Kubernetes, or K3s describes reference integration points. It does not imply certification, endorsement, or affiliation with the respective projects.

### 72C.4 Public Security Disclosure

Vulnerabilities should not initially be opened as public Issues. `SECURITY.md` defines coordinated disclosure and recommends enabling **GitHub Private Vulnerability Reporting** when the repository is public.

Particularly relevant failures include bypass of:

```text
Identity
Authorization
PDP / PEP
Capability bounds
Delegation bounds
Revocation
Kill Switch
Evidence integrity
Adapter semantics
Edge fail-secure behavior
Cyber-physical safety barriers
```

### 72C.5 Public Repository CI

The primary workflow runs a supported Python matrix and verifies:

```text
SDD specification validation
        +
Automated tests
        +
Adapter conformance
        +
Agent-BOM generation
        +
Basic secret-pattern rejection
        +
Generated assurance evidence
```

CodeQL runs separately for static security analysis. Dependabot monitors Python and GitHub Actions dependencies. The configuration uses `dependabot.yml` version 2, according to the current format documented by GitHub.

### 72C.6 Assurance and Non-Certification

It is prohibited to infer:

```text
GitHub CI PASS
      ⇒
Production Certified
```

The correct result is:

```text
GitHub CI PASS
      ⇒
Specified repository checks passed
```

IPS-C2/C3, L4 environments, OT/ICS, or cyber-physical systems require evidence from the real/representative environment, in addition to independent assessment appropriate to the domain.

### 72C.7 Branch and Release Governance

Recommended:

```text
main
  └── protected by GitHub ruleset
       ├── pull request required
       ├── CI required
       ├── review required
       └── force-push disabled

release
  └── signed/reviewed tag vMAJOR.MINOR.PATCH
```

The complete policy is in `docs/github-public-release.md`.

### 72C.8 Citation

`CITATION.cff` allows GitHub and academic tools to present SGAEIA citation metadata. The release records:

```text
SGAEIA — Secure Governed Autonomous Edge Intelligence Architecture
Aridio Silva — @aridiosilva
Version 0.3.2
September 2026
Apache-2.0
```

### 72C.9 Suggested GitHub Topics

```text
edge-ai
agentic-ai
multi-agent-systems
zero-trust
grc
security-by-design
spec-driven-development
owasp
mitre-atlas
nist
mec
ai-security
```

### 72C.10 Definition of Ready for Public Release

The first public publication should be considered ready only when:

```text
NoKnownSecrets
AND LicensePresent
AND GovernancePresent
AND SecurityDisclosureDefined
AND SpecsValid
AND TestsPass
AND ConformanceHarnessPasses
AND BOMGenerated
AND CIConfigured
AND ReleaseTagReviewed
```

The detailed operational checklist is available in `docs/github-public-release.md`.

## 73. Supported Deployment Patterns

The architecture may be adapted for:

### Cloud-Centric

Cloud concentrates the control plane; Edge executes low-latency local operations.

### Hierarchical Edge/MEC

PDPs and controls are distributed across Cloud, region, MEC, and Edge.

### Sovereign Edge

Edge retains a minimum safe capability even when disconnected.

### OT / Cyber-Physical

Physical actions require safety controls, interlocks, and an emergency-stop capability independent of the LLM.

### Multi-Organization / Federated

Separate trust domains negotiate identity, capabilities, and policies without assuming implicit trust.

---

## 74. Reference Integration Architecture

```text
Enterprise Governance
        │
        ▼
Policy / Risk / GRC
        │
        ▼
Identity & Trust Fabric
        │
        ▼
Agent Control Plane
        │
        ▼
Zero-Trust Agentic Mesh
        │
 ┌──────┼─────────┐
 ▼      ▼         ▼
Cloud   MEC      Edge
Agents  Agents   Agents
                  │
                  ▼
              OT / IoT
                  │
                  ▼
Observability / Evidence
                  │
                  ▼
SOC / GRC / Audit
```

The concrete technology in each block is replaceable. The security semantics are not.

---

## 75. Framework Integration

The project was designed to support crosswalks, as applicable, with:

- NIST SP 800-207 / SP 800-207A — Zero Trust;
- NIST Cybersecurity Framework 2.0;
- NIST AI RMF;
- NIST AI 600-1 — Generative AI Profile;
- NIST SP 800-218 / 800-218A — SSDF;
- ISO/IEC 42001:2023;
- ISO/IEC 23894:2023;
- ISO/IEC 27001;
- MITRE ATT&CK;
- MITRE ATLAS;
- OWASP GenAI Security Project;
- OWASP Agentic Security Initiative;
- OWASP Agent Control Standard;
- OWASP ASVS;
- ETSI MEC;
- IEC 62443 for OT/ICS;
- SPIFFE/SPIRE or equivalent workload identity.

See `docs/references.md` and `specs/compliance/`.

---

## 76. GRC and Agentic-Posture Metrics

Recommended KPIs/KRIs:

```text
% agents inventoried
% agents with owner
% agents with risk assessment
% agents with cryptographic identity
% agents with kill-switch
% agents with valid threat model
% agents exceeding autonomy policy
mean delegation depth
mean blast radius
policy deny rate
agent anomaly rate
mean time to revoke
mean time to quarantine
% actions with provenance
% controls continuously evidenced
```

An organization may derive an **Agent Security Posture Score — ASPS**:

```text
ASPS = 100 - (
    RiskPenalty
  + ControlGap
  + BehaviorPenalty
  + CompliancePenalty
)
```

---

## 77. Organizational Responsibilities

### Board / Executive

Defines:

- risk appetite;
- accountability;
- AI governance principles.

### AI Governance Board

Defines:

- AI policy;
- autonomy levels;
- prohibited uses;
- approval criteria.

### CISO

Responsible for:

- security architecture;
- cyber threat model;
- incident response.

### CRO / GRC

Manages:

- risk;
- compliance;
- exceptions;
- residual-risk acceptance workflow.

### Agent Owner

Accountable for the agent and its purpose.

### Platform Engineering

Operates:

- identity;
- policy;
- agent mesh;
- registries;
- platform controls.

### SOC

Monitors:

- anomalies;
- attack paths;
- policy violations;
- incidents.

No production agent should have:

```text
Owner = NULL
```

---

## 78. Governed Agent — Formal Definition

An agent is governed when:

```text
Governed(A) =
    Identity(A)
AND Owner(A)
AND Purpose(A)
AND Capabilities(A)
AND Policy(A)
AND Risk(A)
AND Observability(A)
AND Auditability(A)
AND Revocability(A)
```

If a mandatory condition is not satisfied:

```text
Governed(A) = false
```

---

## 79. Secure Agentic System — Formal Definition

The system seeks the property:

```text
for every Agent A:
    Governed(A)

for every Interaction E:
    Authorized(E)

for every CriticalAction:
    PolicyChecked
    AND RiskChecked
    AND Auditable
```

This is an architectural objective; real assurance levels depend on the implementation and verification performed in each domain.

---

## 80. Current Repository State

This version includes:

- minimal Python implementation;
- FastAPI;
- Agent Registry;
- reference PDP/PEP;
- Risk Engine;
- Delegation Controller;
- Kill Switch;
- Evidence Service;
- YAML/JSON manifests;
- schemas;
- reference OPA/Rego;
- OpenAPI for the control API and **OpenAPI 3.2.0** for HTTP Integration Ports;
- **AsyncAPI 3.1.0** for event contracts;
- **12 machine-readable Integration Port Specifications (IPS)**;
- conformance matrix and replacement-technology qualification procedure;
- **Adapter Conformance Framework (ACF)** with 9 concrete reference profiles;
- executable adapters for SPIRE, OPA, Istio/Envoy, OpenTelemetry, NATS, Kafka, PostgreSQL, Kubernetes, and K3s;
- `enterprise-cloud` and `edge-k3s` deployment profiles;
- adapter-conformance `Evidence-as-Code` report;
- Docker;
- Kubernetes manifests;
- OpenTelemetry configuration;
- threat-model artifacts;
- risk/control catalogs;
- AI-BOM and Agent-BOM;
- formal models in TLA+ and Alloy;
- Python unit, integration, security, adversarial, formal, and IPS conformance tests.

Verified state of this revision:

```text
SPEC VALIDATION PASSED
INTEGRATION PORT VALIDATION PASSED
31 tests passed
```

---

## 81. Current Limitations

This reference must not be interpreted as a production-ready product for critical environments.

Before production, the following must be implemented and validated as applicable:

1. real trust domains and PKI/workload identity;
2. enterprise PDP/PEP;
3. real inventory/discovery of agents, models, and tools;
4. IAM/PAM/NHI integration;
5. SIEM/SOAR/GRC;
6. RAG provenance and data classification;
7. Edge-node attestation;
8. use-case-specific red teaming;
9. safety case for L4;
10. jurisdiction/sector regulatory mapping;
11. IPS-C2/C3 qualification in real environments for each selected adapter;
12. real measurement of revocation, failover, partition, and version skew for deployed products;
12. BCP/DR;
13. isolation and disconnection tests;
14. artifact signing/provenance;
15. real secrets management;
16. data-plane encryption;
17. service mesh or equivalent enforcement;
18. immutable evidence storage;
19. incident-response runbooks;
20. model supply-chain controls;
21. independent security and safety validation.

---

## 82. Recommended Next Evolution

The natural evolution of this version is to decompose the minimal implementation into real services:

```text
Agent Registry Service
Identity Service / Workload Identity Adapter
Policy Decision Service
Policy Enforcement Middleware
Risk Engine Service
Delegation Service
Evidence Service
Kill-Switch Service
Governance API
A2A Gateway
Tool Gateway
Observability Pipeline
```

And integrate replaceable production components for:

```text
Workload Identity
mTLS / Trust Fabric
Policy-as-Code
Service / Agent Mesh
Persistent Registry
Message Bus
Evidence Store
SIEM / SOAR
GRC
Remote Attestation
SBOM / AI-BOM / Agent-BOM provenance
```

A later stage may transform the repository into a **Multi-Agent Edge AI Cyber Range**, capable of executing controlled scenarios involving:

- prompt injection;
- memory poisoning;
- RAG poisoning;
- agent impersonation;
- delegation escalation;
- tool abuse;
- lateral movement;
- malicious MCP/tool server;
- sensor spoofing;
- unsafe actuation;
- Edge disconnection;
- PDP failure;
- compromised agent.

The objective would be to demonstrate not only the threat, but the automated response:

```text
Detect
-> Evaluate Risk
-> Enforce Policy
-> Restrict
-> Quarantine
-> Revoke
-> Preserve Evidence
```

---

## 83. References

See:

```text
docs/references.md
specs/compliance/
specs/threat-model/
```

Core references include NIST, ISO/IEC, OWASP, MITRE, ETSI, SPIFFE, and IEC as applicable to the domain.

---

## 84. Licensing

This repository is provided as technical reference material.

An organization adopting it should:

- define the licensing of its implementation;
- review dependency licenses;
- review requirements of the standards used;
- perform applicable legal and regulatory analysis.

---

## 85. Architecture Summary

The objective of this architecture is to establish a condition in which:

> **no agent implicitly trusts another agent; no critical action derives exclusively from a model's probabilistic decision; every identity, capability, and delegation is verifiable; every relevant action is observable; every authority has limits; and all relevant autonomy is reversible.**

The final thesis is:

```text
Distributed Intelligence
+
Zero Trust
+
Governed Autonomy
+
Continuous GRC
+
Security-by-Design
+
Evidence-by-Default
=
Secure Governed Edge-AI Architecture
```

Intelligence may be distributed.

**Authority must remain explicitly governed.**


# 72D. Academic Publication and arXiv Technical Paper Series

SGAEIA is accompanied by an English-language academic publication track under `paper/arxiv-series/`. The publication narrative intentionally begins with the evolution **Cloud Computing -> Edge Computing -> Edge AI -> Agentic Edge AI -> Distributed Autonomous Agency**. This conceptual progression is not treated as unrelated background: it establishes the architectural necessity for SGAEIA.

The initial series contains four manuscripts:

1. **Reference Architecture** — the canonical paper presenting the complete SGAEIA scope.
2. **Governed Autonomy and Security** — identity, capability, delegation, Zero Trust, continuous GRC, revocation, fail-secure Edge operation, and formal invariants.
3. **Integration Port Specifications and Adapter Conformance** — security-preserving technology substitution and semantic conformance.
4. **Cyber-Range Evaluation Protocol** — a pre-results, reproducible methodology for future empirical evaluation.

The manuscripts distinguish four evidence levels:

```text
Designed Property
    -> Formally Specified Property
    -> Locally Tested Property
    -> Representative / Live Experimental Evidence
```

No manuscript may present local contract tests as production certification, claim completed TLA+/Alloy model checking unless those model checkers have actually been executed, or report cyber-range results before the experiments are performed.

Canonical public repository: `https://github.com/aridiosilva/SGAEIA`.

## 72E. First Public Research Preview — v0.3.2

Version `v0.3.2` established the first public SGAEIA research
preview at:

https://github.com/aridiosilva/SGAEIA

The public repository was validated through GitHub-hosted
security CI and CodeQL before the versioned release was published.

The `main` branch is governed through GitHub branch protection/rulesets,
and dependency maintenance is supported by Dependabot.

The release remains a research reference artifact and does not
constitute production certification.

## Research Artifact Archival and Persistent Identification

SGAEIA uses GitHub as the canonical living source repository and
Zenodo for persistent archival, versioned citation, and long-term
identification of selected research releases.

### Canonical Source Repository

https://github.com/aridiosilva/SGAEIA

### Persistent Identifiers

SGAEIA is archived in Zenodo and has persistent Digital Object
Identifiers (DOIs) for both the evolving research artifact and
individual archived releases.

**SGAEIA — All Versions / Concept DOI**

DOI: `10.5281/zenodo.22557795`

https://doi.org/10.5281/zenodo.22557795

The Concept DOI identifies SGAEIA across releases and resolves to the
latest archived version. It SHOULD be used when referring to the SGAEIA
project as an evolving research artifact.

**SGAEIA v0.3.4 — Version DOI**

DOI: `10.5281/zenodo.22557796`

https://doi.org/10.5281/zenodo.22557796

The version DOI identifies the immutable Zenodo archive of SGAEIA
version `v0.3.4`. It SHOULD be used when reproducibility requires
citation of the exact software artifact used in research, evaluation,
or experimentation.

### Research Artifact Metadata

Research artifact metadata is maintained through:

- `CITATION.cff` — standardized software citation metadata;
- `.zenodo.json` — Zenodo archival metadata;
- ORCID — persistent creator identification;
- GitHub Releases — versioned source releases;
- Zenodo — immutable archival records and persistent DOI assignment.

### Creator

Aridio Silva  
GitHub: `@aridiosilva`  
ORCID: https://orcid.org/0009-0008-2411-6995

### Citation Policy

When citing SGAEIA generally, use the Concept DOI:

`10.5281/zenodo.22557795`

When citing the exact `v0.3.4` research artifact, use the version-specific DOI:

`10.5281/zenodo.22557796`

Future SGAEIA releases archived by Zenodo may receive their own
version-specific DOI while remaining associated with the SGAEIA
Concept DOI.
