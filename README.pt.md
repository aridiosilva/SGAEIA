# Secure Governed Multi-Agent Edge AI — SDD Reference Project

**SGAEIA — Secure Governed Autonomous Edge Intelligence Architecture**  
**Aridio Silva — @aridiosilva — Setembro de 2026**

**Languages:** English | [Português](README.pt.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22557795.svg)](https://doi.org/10.5281/zenodo.22557795)

**Current public release:** `v0.3.4 — Citation and Zenodo Metadata Fix`  
**Research status:** `Public Research Preview`  
**Concept DOI:** `10.5281/zenodo.22557795`  
**Version DOI (v0.3.4):** `10.5281/zenodo.22557796`  
**License:** Apache-2.0

Projeto de referência **Spec-Driven Development (SDD)** para arquiteturas **Edge-AI multiagente** com **Zero Trust, GRC distribuído, Security-by-Design, Security-First, Shift Left/Right/Everywhere e autonomia governada**.

> **Status:** referência arquitetural e implementação mínima demonstrativa. Não é um produto pronto para produção e não substitui análise jurídica, safety engineering, threat modeling específico do domínio, validação regulatória, hardening operacional ou certificação independente.

---

## 1. Resumo executivo

Este repositório transforma uma arquitetura conceitual de Edge AI multiagente em um **Projeto SDD formal, versionável, testável e parcialmente executável**.

O problema tratado é simples de formular, mas complexo de resolver:

```text
Distributed Intelligence
        ≠
Uncontrolled Distributed Authority
```

Sistemas modernos podem combinar simultaneamente:

- agentes de IA locais e remotos;
- LLMs e outros modelos;
- Edge, Far Edge, MEC e Cloud;
- IoT/IIoT;
- OT/ICS;
- sensores e atuadores;
- RAG e bancos vetoriais;
- memória agentiva;
- APIs, ferramentas e MCP servers;
- serviços SaaS e terceiros;
- múltiplas organizações e trust domains.

Por isso, o objetivo desta arquitetura é permitir **inteligência distribuída** sem conceder **autoridade distribuída não governada**.

A tese central é:

```text
Intelligence != Trust
Trust        != Authority
Authority    != Unlimited Autonomy
Autonomy     => Governance + Evidence + Revocability
```

O modelo de IA pode propor uma ação. A arquitetura deve decidir se essa ação pode ser executada.

---

## 2. O que este projeto formaliza

O projeto define e implementa uma referência para:

- identidade não humana (**NHI**) de agentes e workloads;
- classificação de criticidade **L0–L4**;
- níveis de autonomia **A0–A5**;
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
- integração com **SBOM**;
- **Integration Port Specifications — IPS**;
- **Adapter Conformance Framework — ACF** com perfis concretos e assurance progressivo;
- catálogo de controles;
- risk register e threat register;
- testes de invariantes;
- testes adversariais;
- security gates no CI/CD;
- modelos formais em **TLA+** e **Alloy**;
- rastreabilidade SDD entre requisito, risco, controle, implementação, teste e evidência.

---

## 3. Hipótese arquitetural fundamental

A arquitetura assume desde o início:

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

Logo:

```text
System Safety != Agent Correctness
```

A segurança do sistema **não pode depender de o agente se comportar corretamente**.

Ela deve resultar de controles externos ao raciocínio do agente, que limitem o que ele pode fazer mesmo quando estiver errado, comprometido ou sob influência maliciosa.

Esse princípio orienta toda a implementação.

---

## 4. Princípios normativos

A arquitetura adota os seguintes princípios.

### P-01 — Zero Implicit Trust

Nenhum agente, workload, usuário, modelo, ferramenta, dispositivo ou serviço recebe confiança apenas por:

- localização;
- rede;
- organização;
- propriedade;
- origem declarada;
- relacionamento com um agente pai.

### P-02 — Every Agent Has an Identity

Todo agente deve possuir uma identidade verificável própria.

```text
Agent => Non-Human Identity
```

### P-03 — No Action Without Authorization

```text
Intent -> Authorization -> Execution
```

Nunca:

```text
Intent -> Execution -> Audit
```

### P-04 — Principle of Least Agency — PoLA

O agente deve possuir somente a autonomia necessária para sua finalidade.

Least Privilege é insuficiente quando o sistema também pode:

- planejar;
- delegar;
- executar ferramentas;
- iniciar novos fluxos;
- alcançar o mundo físico.

### P-05 — Delegation Cannot Increase Authority

Uma delegação não pode criar autoridade que o agente delegante não possua no contexto da operação.

```text
Capabilities(child) <= DelegatedCapabilities(parent)
```

### P-06 — Autonomy Must Be Revocable

Toda autonomia relevante deve poder ser:

- pausada;
- reduzida;
- revogada;
- isolada;
- encerrada.

```text
Autonomy => Revocability
```

### P-07 — Model Is Never the Security Authority

O LLM pode recomendar ou planejar uma ação. O LLM não é a autoridade que concede permissão para sua própria execução.

### P-08 — Policy Before Action

Toda ação relevante deve atravessar um **PEP** antes de alcançar recurso, ferramenta ou atuador.

### P-09 — Evidence by Default

Toda ação relevante deve produzir evidência verificável.

```text
Action -> Evidence
```

### P-10 — Assume Agent Compromise

O sistema deve permanecer limitado mesmo quando um agente válido for comprometido.

---

## 5. Invariantes de segurança

O projeto transforma princípios em propriedades verificáveis.

1. `AgentWithoutIdentity => DENY`
2. `UnknownAgent => DENY`
3. `L4 AND A5 => DENY`
4. `DelegationDepth > MaxDepth => DENY`
5. `ChildCapabilities ⊄ ParentDelegatedCapabilities => DENY`
6. `PaymentCreator == PaymentApprover => DENY`
7. `UntrustedInput -> PhysicalActuation` não pode existir sem mediação e autorização explícitas.
8. `AttestationFailed AND CriticalAgent => STOP/QUARANTINE`
9. `OfflineMode => ReducedAuthority`, nunca autoridade ampliada.
10. Toda ação crítica deve produzir evidence e decision provenance.
11. Um agente não pode elevar sozinho sua própria autonomia.
12. Um modelo não pode conceder autorização a si próprio.
13. Uma trust boundary não pode ser atravessada apenas por decisão semântica do LLM.
14. Credenciais críticas devem possuir validade limitada e ser revogáveis.
15. Ação crítica sem owner, policy ou traceability deve ser negada.

O objetivo não é apenas detectar comportamento ruim. É construir uma arquitetura onde determinadas classes de comportamento sejam **impossíveis ou fortemente limitadas por construção**.

---

## 6. Modelo formal geral

O sistema pode ser representado como:

```text
S = (V, E, Z, P, I, C, R, T, L)
```

onde:

- `V` = entidades;
- `E` = relações;
- `Z` = trust zones;
- `P` = políticas;
- `I` = identidades;
- `C` = capabilities;
- `R` = riscos;
- `T` = telemetria/evidência;
- `L` = estado de lifecycle.

As entidades podem ser decompostas em:

```text
V = H ∪ A ∪ M ∪ D ∪ W ∪ F ∪ N ∪ X
```

onde:

- `H` = humanos;
- `A` = agentes;
- `M` = modelos;
- `D` = dados;
- `W` = workloads;
- `F` = ferramentas;
- `N` = nós de infraestrutura;
- `X` = entidades externas.

A confiança é dinâmica:

```text
Trust = f(identity, context, device, attestation, behavior, history, policy, risk)
```

Ela não é uma propriedade permanente de uma entidade.

---

## 7. Modelo de autorização

A decisão de autorização pode ser representada como:

```text
Authorize(a, r, o, c, t) =
    IdentityValid(a)
    AND CapabilityValid(a, o)
    AND PolicyAllows(a, r, o, c)
    AND Risk(a, r, o, c) < MaxRisk
    AND Trust(a) > MinTrust
```

onde:

- `a` = agent/workload;
- `r` = recurso;
- `o` = operação;
- `c` = contexto;
- `t` = estado temporal.

Logo:

```text
Execute iff Authorize == true
```

---

## 8. Governed Autonomy

O projeto usa o conceito de **Governed Autonomy — Autonomia Governada**.

A pergunta não é apenas:

> O agente consegue executar esta ação?

A pergunta correta é:

> Este agente pode executar esta ação, neste recurso, neste contexto, neste momento, sob este risco, com estas evidências e com esta possibilidade de revogação?

A autonomia efetiva deve ser dinâmica:

```text
A_effective = min(
    A_configured,
    A_risk,
    A_context,
    A_trust,
    A_policy
)
```

Um agente configurado como `A4` pode ser rebaixado automaticamente para `A1` durante uma anomalia ou perda de confiança.

---

## 9. Classificação de agentes L0–L4

| Classe | Descrição | Exemplos | Autonomia normal máxima |
|---|---|---|---:|
| L0 | Informacional | sumarização, consulta pública | A4 |
| L1 | Operacional limitado | tarefas internas de baixo impacto | A3 |
| L2 | Corporativo privilegiado | dados sensíveis, ERP, workflows de negócio | A3 |
| L3 | Crítico | financeiro, administrativo, regulado | A2 |
| L4 | Cyber-physical / safety critical | OT, robôs, PLC, atuadores | A1/A2 |

A combinação:

```text
L4 + A5
```

é explicitamente proibida na referência.

---

## 10. Níveis de autonomia A0–A5

| Nível | Significado |
|---|---|
| A0 | Observe |
| A1 | Recommend |
| A2 | Act with approval |
| A3 | Bounded autonomous execution |
| A4 | Autonomous planning and execution |
| A5 | Autonomous orchestration/delegation |

Autonomia não é tratada como um booleano. Ela é uma variável de risco e governança.

---

## 11. Agent Trust Zones — ATZ

| Zona | Significado | Postura |
|---|---|---|
| ATZ-0 | External / Unknown | nenhuma confiança implícita |
| ATZ-1 | Untrusted Inputs | entrada não confiável |
| ATZ-2 | Sandboxed Agents | baixa autoridade |
| ATZ-3 | Enterprise Agents | confiança condicionada |
| ATZ-4 | Privileged Agents | controles reforçados |
| ATZ-5 | Cyber-Physical Critical | criticidade máxima, nunca confiança implícita |

ATZ-5 **não** significa “totalmente confiável”. Significa **máxima criticidade e máximo rigor de controle**.

Uma transição entre zonas deve satisfazer:

```text
AuthN AND AuthZ AND Policy AND Risk AND Context AND Trust == ALLOW
```

Caso contrário:

```text
DENY
```

A postura padrão é **Default Deny**.

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

## 14. Agent Runtime seguro

Cada runtime agentivo deve interpor controles entre raciocínio e execução:

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

O ponto essencial é que o agente **não possui acesso direto e irrestrito à ferramenta**.

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

Trust boundaries relevantes incluem:

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

Cada boundary deve possuir threat model próprio.

---

## 16. Identidade de agentes e workloads

Um dos erros arquiteturais mais perigosos é permitir que agentes operem genericamente com a credencial de um usuário, servidor ou aplicação.

Cada agente deve possuir registro próprio:

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

Exemplo conceitual de workload identity:

```text
spiffe://enterprise.ai/agents/finance/invoice-agent/production/instance-8834
```

O uso de SPIFFE/SPIRE no projeto é **referencial**, não obrigatório. Consulte a seção **Pontos de integração substituíveis**.

---

## 17. Agent Identity Record — AIR

Exemplo:

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

O Agent Registry deve permitir responder:

- Quem é este agente?
- Quem é seu owner?
- Qual sua finalidade?
- Que modelo utiliza?
- Em qual runtime executa?
- Que dados pode acessar?
- Que ferramentas pode usar?
- Pode delegar?
- Para quem?
- Qual sua autonomia?
- Qual seu risco?
- Quem pode interrompê-lo?

---

## 18. Capability Graph

O projeto não trata autorização apenas como papéis amplos.

```text
Agent.Invoice
    │
    ├── READ -> InvoiceDB
    ├── READ -> VendorDB
    ├── CALL -> OCR
    └── CALL -> ERP.Query
```

Formalmente:

```text
G_C = (A, C, E_C)
```

onde:

- `A` = agentes;
- `C` = capabilities;
- `E_C` = relações de concessão.

Capabilities devem poder ser específicas e temporárias:

```text
resource: invoice/89383
operation: read
duration: 60 seconds
delegate: false
```

---

## 19. Toxic Capability Combinations

O risco não decorre apenas de uma capability isolada.

Exemplo:

```text
SensitiveRead
+
ExternalWrite
+
CodeExecution
=
HighExfiltrationRisk
```

Outro exemplo:

```text
PaymentCreate + PaymentApprove = SegregationOfDutiesViolation
```

Logo, o Policy Engine deve avaliar **combinações de capacidades**, não apenas permissões individuais.

---

## 20. Delegation Graph

```text
G_D = (A, E_D)
```

Uma aresta:

```text
Agent-A -> Agent-B
```

significa que A pode delegar uma tarefa específica a B.

A delegação deve ser limitada por:

- profundidade;
- duração;
- capabilities;
- data scope;
- custo;
- runtime;
- onward delegation.

Exemplo:

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

O agente B **não herda automaticamente** todas as permissões de A.

---

## 21. Agent-to-Agent Security

Toda comunicação A2A relevante deve prever:

1. identidade mútua;
2. autenticação;
3. autorização;
4. confidencialidade;
5. integridade;
6. freshness;
7. anti-replay;
8. non-repudiation quando necessária;
9. schema validation;
10. intent validation;
11. correlation/trace ID;
12. policy evaluation.

---

## 22. Agent Intent Manifest

Antes de uma operação crítica, o agente deve declarar a intenção:

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

O PEP não autoriza somente “uma conexão”. Ele deve poder autorizar a **ação e o intent no contexto**.

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

### Regra principal

```text
Decision -> PolicyCheck -> Action
```

Não:

```text
Decision -> Action -> Audit
```

Auditoria posterior detecta dano. Security-by-Design deve impedir o dano antes da execução sempre que possível.

---

## 24. PDP hierárquico e distribuído

Edge AI não deve depender exclusivamente de um PDP em cloud.

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

Princípio:

```text
Global Governance
+
Local Decision
+
Central Evidence
```

---

## 25. Operação desconectada e Fail Secure

A perda de cloud ou conectividade não deve aumentar privilégios.

```text
OfflineMode => ReducedAuthority
```

Nunca:

```text
OfflineMode => UnlimitedAuthority
```

Exemplo de comportamento seguro:

```text
ALLOW cached low-risk operation
DENY unknown high-risk operation
DENY privilege escalation
DENY new external delegation
```

---

## 26. Sovereign Edge Mode

Ambientes críticos podem operar em **Sovereign Edge Mode**, mantendo localmente:

- identity verification;
- policy enforcement;
- modelos mínimos necessários;
- RAG mínimo necessário;
- logging;
- risk scoring;
- kill switch;
- safe operating mode.

O objetivo não é isolar permanentemente o Edge, mas preservar uma condição segura em degradação de conectividade.

---

## 27. Safe Degradation

Quando a confiança diminui, a autoridade deve diminuir.

```text
Normal           -> A3
Network degraded -> A2
Identity uncertain -> A1
Attestation failed -> A0 / STOP
```

Princípio:

```text
Trust down => Capability down
```

---

## 28. Agent Risk Score — ARS

O modelo conceitual usa:

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

A implementação de referência usa uma versão simplificada, auditável e normalizada entre 0 e 100.

Exemplo de resposta:

| ARS | Tratamento de referência |
|---:|---|
| 0–20 | allow |
| 21–40 | allow + telemetry |
| 41–60 | restrict / step-up |
| 61–80 | require human approval |
| 81–90 | quarantine |
| 91–100 | revoke / kill |

Esses thresholds **não são universais** e devem ser calibrados por domínio, impacto, segurança funcional, risco regulatório e apetite de risco.

---

## 29. Blast Radius

Para cada agente deve ser possível responder:

> Se este agente for comprometido agora, qual é o dano máximo possível?

Conceitualmente:

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

O blast radius deve ser reduzido usando:

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

Cada agente deve possuir um risk record.

| Campo | Exemplo |
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

O repositório inclui um exemplo em `specs/risks/risk-register.csv`.

---

## 31. Superfície de ataque ampliada

Em Edge-AI, a superfície pode ser representada como:

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

IA não substitui as superfícies anteriores. Ela **adiciona novas superfícies**.

---

## 32. Threat modeling integrado

O projeto combina:

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

STRIDE continua útil, mas não cobre sozinho:

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

## 33. Catálogo inicial de ameaças

O projeto considera, entre outras:

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

Os arquivos em `specs/threat-model/` contêm o detalhamento e crosswalks.

---

## 34. Attack Path Analysis

Uma rota de ataque pode surgir apenas pela composição:

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

Logo:

```text
Risk(System) != Sum(Risk(Component_i))
```

Existem riscos emergentes de relação, cadeia e comportamento coletivo.

---

## 35. RAG Security

Uma implementação de produção deve prever:

- source provenance;
- document signing quando aplicável;
- classification;
- ingestion validation;
- malware/content scanning;
- access control;
- tenant isolation;
- vector isolation;
- embedding integrity;
- retrieval authorization.

Princípio:

```text
CanRetrieve(Document) != CanDisclose(Document)
```

---

## 36. Agent Memory Security

Memória persistente deve ter metadados como:

```text
origin
timestamp
agent
classification
trust_score
expiry
integrity
```

Informação armazenada por um agente não deve tornar-se automaticamente “verdade confiável”.

---

## 37. Registries

### Agent Registry

Fonte de verdade para:

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

Deve registrar, conforme necessidade:

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

Ferramentas devem possuir:

- identidade;
- operações permitidas;
- risco;
- network scope;
- authentication requirements;
- logging requirements;
- policy requirements.

---

## 38. AI-BOM, Agent-BOM e SBOM

A composição completa pode ser representada como:

```text
SystemBOM = SBOM + AI-BOM + Agent-BOM
```

### AI-BOM

Pode incluir:

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

Registra especificamente:

- agents;
- roles;
- relationships;
- capabilities;
- delegations;
- tools;
- models;
- trust zones.

O repositório contém exemplos em `bom/`.

---

## 39. Supply Chain Security

Nenhum artefato crítico deveria alcançar produção sem mecanismos proporcionais de:

- signature verification;
- provenance;
- dependency scan;
- vulnerability scan;
- policy compliance;
- model validation;
- artifact attestation.

---

## 40. Edge Node Security

Conforme criticidade, Edge nodes devem considerar:

- Secure Boot;
- Measured Boot;
- TPM ou hardware root of trust;
- disk encryption;
- workload isolation;
- container sandbox;
- device identity;
- remote attestation;
- firmware signing;
- least privilege;
- secure update;
- tamper detection.

A trust decision sobre o node pode ser representada como:

```text
Trust(node) = Identity + IntegrityState + Attestation
```

---

## 41. Zero-Trust Agentic Mesh — ZTAM

O ZTAM estende o conceito de service mesh para interações agentivas.

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

Pode conter:

- Agent Proxy;
- Identity Proxy;
- Policy Proxy;
- Tool Proxy;
- A2A Gateway;
- Egress Gateway;
- Telemetry Sidecar;
- Evidence Collector.

A arquitetura é independente de vendor.

---

## 42. Egress Governance

Agentes não devem possuir Internet access irrestrito por padrão.

Todo egress relevante deve ser:

- identificado;
- autorizado;
- classificado;
- logado;
- rate-limited;
- policy-controlled.

---

## 43. Human-in-the-Loop baseado em risco

A arquitetura não exige aprovação humana para tudo.

```text
LOW RISK     -> autonomous
MEDIUM RISK  -> autonomous + monitoring
HIGH RISK    -> step-up / human approval
CRITICAL     -> multi-party authorization / deny
```

O objetivo é preservar automação sem abrir mão de accountability em ações irreversíveis ou de alto impacto.

---

## 44. Segregation of Duties — SoD

Nenhum agente crítico deve, sozinho, acumular todas as etapas incompatíveis de uma transação.

Exemplo:

```text
Agent A -> proposes payment
Agent B -> validates invoice
Policy Engine -> validates controls
Human C -> authorizes
Bank API -> executes
```

Em especial:

```text
create + approve + execute
```

não deve existir na mesma autoridade quando o domínio exigir SoD.

---

## 45. Observabilidade agentiva

Logs tradicionais são insuficientes.

Devem ser capturados, conforme criticidade:

- Agent ID;
- Session ID;
- Trace ID;
- Model;
- Model version;
- Intent;
- prompt hash ou referência segura;
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

## 46. Distributed Trace e Decision Provenance

Uma tarefa multiagente deve poder ser reconstruída:

```text
Human
  └── Agent-A
       ├── Agent-B
       │    └── Tool-X
       └── Agent-C
            └── Database
```

Para ações críticas, a provenance deve responder:

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

O objetivo é que controles produzam evidência automaticamente.

Exemplo:

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

Isso suporta **Continuous Compliance** em vez de auditoria puramente periódica.

---

## 48. Continuous GRC

A transformação buscada é:

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

Assim, GRC deixa de ser apenas documentação e passa a participar do runtime.

---

## 49. Governance Knowledge Graph

Conceitualmente:

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

Esse modelo permite rastreabilidade bidirecional:

- da norma até a evidência;
- da evidência até o requisito;
- do agente até riscos e controles;
- do controle até implementação e teste.

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

O projeto materializa esse conceito por meio de specs, catálogo de controles, testes e matriz de rastreabilidade.

---

## 51. GRC hierárquico e distribuído

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

Se a inteligência e a execução são distribuídas, segurança e governança também precisam ser distribuídas.

---

## 52. SDD — Spec-Driven Development

A precedência adotada é:

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

O código **não é a única fonte de verdade**.

Uma alteração de implementação que contrarie uma spec deve:

1. falhar no pipeline; ou
2. exigir alteração formal da spec;
3. exigir ADR quando arquitetural;
4. exigir nova análise de risco quando pertinente.

---

## 53. Rastreabilidade SDD

A cadeia usada pelo projeto é:

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

O arquivo:

```text
specs/traceability/requirements-controls-tests.csv
```

liga requisitos a controles, testes e evidências esperadas.

---

## 54. MASTER-SPEC

`MASTER-SPEC.md` define o contrato normativo superior do projeto.

Ele deve ser consultado antes de alterações arquiteturais significativas.

Artefatos mais específicos devem permanecer coerentes com ele, salvo quando um ADR documentar mudança deliberada de decisão.

---

## 55. Architecture Decision Records — ADR

Decisões importantes devem possuir ADR com, no mínimo:

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

O repositório inclui ADRs iniciais em `specs/adrs/`.

---

## 56. Security Control Catalog

Cada controle deve possuir:

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

Famílias sugeridas:

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

O caráter “formal” do projeto não se limita à documentação.

O repositório contém:

```text
formal/tla/SGAEIA.tla
formal/alloy/sgaeia.als
```

Esses modelos expressam propriedades como:

- agente sem identidade não executa;
- L4+A5 não é autorizado;
- delegação não aumenta autoridade;
- estados inválidos não devem alcançar RUNNING;
- operações críticas dependem de autorização.

Além disso, existe exploração de espaço de estados em Python em:

```text
tests/formal/test_invariants_state_space.py
```

### Importante

Os arquivos TLA+ e Alloy são **especificações formais fornecidas como base de model checking**, mas esta versão do repositório não pressupõe que os model checkers TLA+/Alloy estejam instalados no ambiente local.

As invariantes equivalentes são exercitadas também pela suíte Python.

---

## 58. Lifecycle Governance

Estados esperados:

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

Transições como:

```text
UNKNOWN -> RUNNING
```

devem ser proibidas.

Lifecycle completo:

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

## 59. Kill Switch e autonomia reversível

Todo agente de risco relevante deve suportar, conforme necessidade:

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

Arquitetura hierárquica:

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

Deve ser possível atuar sobre:

- uma execução;
- um agente;
- um grupo de agentes;
- um Edge node;
- uma região MEC;
- uma versão de modelo;
- uma ferramenta;
- todo o agent mesh.

---

## 60. Emergency Policy

Exemplo conceitual:

```text
IF systemic_attack == true
THEN
  external_agent_calls = DENY
  new_delegations      = DENY
  critical_actions     = HUMAN_ONLY
  edge_autonomy        = REDUCED
```

---

## 61. Security-by-Design, Security-First e Shift Everywhere

A segurança começa nos requisitos.

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

Mas sistemas agentivos mudam em runtime. Portanto:

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

O pipeline é desenhado para incorporar:

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

A implementação atual contém stubs e gates compatíveis com extensão corporativa.

---

## 63. Testes previstos

### Tradicionais

- SAST;
- DAST;
- SCA;
- IaC scanning;
- secret scanning;
- container scanning;
- API security testing.

### IA

- prompt injection;
- indirect prompt injection;
- jailbreak;
- RAG poisoning;
- model abuse;
- data leakage.

### Agentivos

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

Cenários recomendados:

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

O sistema deve degradar com segurança.

---

## 65. Definition of Done — DoD

Um agente só deve ser considerado production-ready quando:

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

Além disso, ações críticas devem possuir **Runtime Admission** via PDP/PEP.

---

## 67. Estrutura do repositório

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

A lista completa é mantida em `PROJECT-MANIFEST.md`.

---

## 68. Implementação de referência atual

A implementação Python demonstra capacidades mínimas para:

- registro e validação de agentes;
- cálculo de risco;
- decisão de política;
- validação de delegação;
- enforcement básico;
- geração de evidência;
- kill switch.

O endpoint:

```text
POST /v1/authorize
```

avalia uma ação proposta com base em:

- identidade;
- classificação;
- autonomia;
- capabilities;
- contexto;
- risco;
- estado do agente;
- regras críticas.

---

## 69. Como executar

### Requisitos básicos

- Python compatível com `pyproject.toml`;
- dependências instaladas;
- ambiente local de desenvolvimento.

### Testes

```bash
python -m pytest -q
```

### Validação das especificações

```bash
python scripts/validate_specs.py
```

### Gerar Agent-BOM

```bash
python scripts/generate_agent_bom.py
```

### API local

```bash
uvicorn sgaeia.api:app --app-dir src --host 0.0.0.0 --port 8080
```

### Health check

```bash
curl http://localhost:8080/health
```

---

## 70. Exemplo de fluxo de autorização

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

O agente **propõe**. A arquitetura **autoriza ou nega**.

---

# 71. Pontos de integração substituíveis

## 71.1 Princípio de neutralidade tecnológica

Este projeto foi desenhado para separar:

```text
Security / Governance Semantics
            │
            ▼
Reference Interface / Contract
            │
            ▼
Replaceable Technology
```

Ou seja, a segurança não deve depender de uma marca ou produto específico.

SPIFFE/SPIRE, OPA/Rego, OpenTelemetry, Envoy/Istio e outros componentes citados são **implementações de referência ou exemplos de integração**.

Eles podem ser substituídos desde que a nova solução preserve o **contrato semântico e as invariantes arquiteturais**.

---

## 71.2 Matriz de substituição

| Domínio | Referência no projeto | Pode ser substituído por | Contrato mínimo que deve permanecer |
|---|---|---|---|
| Workload / Agent Identity | SPIFFE/SPIRE | cloud workload identity, PKI própria, service identity platform, NHI platform | identidade única, verificável, rotacionável, curta duração quando possível, revogação, binding ao workload |
| PKI / Certificates | X.509/mTLS | enterprise CA, cloud CA, HSM-backed PKI | autenticação forte, integridade, rotação, revogação, trust domain explícito |
| Policy Engine | OPA/Rego | Cedar, Zanzibar-style engine, cloud IAM policy engine, custom PDP | decisão externalizada, deterministicamente auditável, default deny, versionamento de policy |
| PEP | middleware/API enforcement | Envoy filter, API gateway, service mesh, sidecar, library interceptors | nenhuma ação protegida bypassa enforcement |
| Service / Agent Mesh | Istio/Envoy/Linkerd model | Cilium service mesh, cloud mesh, custom proxy fabric | mTLS, identity propagation, policy hooks, telemetry, egress control |
| Observability | OpenTelemetry | vendor APM, cloud-native telemetry, custom event bus | trace ID, logs, metrics, correlation, exportabilidade, clock consistency adequada |
| Evidence Store | JSON/files em referência | WORM storage, object storage, immutable log, ledger, GRC evidence platform | integridade, retenção, provenance, access control, timestamp, queryability |
| SIEM/SOC | integração conceitual | qualquer SIEM/SOAR/SOC platform | ingestão de eventos, correlação, alerting, investigação, response hooks |
| GRC | especificações e evidence mapping | GRC platform, control monitoring platform, knowledge graph | requirement→control→evidence traceability e ownership |
| Risk Engine | Python reference | rules engine, Bayesian model, graph risk engine, ML-assisted risk engine | score explicável, limites, inputs versionados, policy-safe behavior |
| Registry | YAML/files + Python | PostgreSQL, service catalog, CMDB, graph DB, cloud registry | source of truth, owner, version, lifecycle, auditability |
| Agent Registry | manifests | dedicated agent registry/platform | identidade, owner, purpose, capabilities, autonomy, risk, lifecycle |
| Model Registry | manifests | MLflow, cloud model registry, enterprise AI catalog | model ID/version, provenance, approval, deployment status |
| Tool Registry | manifests | API catalog, service catalog, MCP registry | tool identity, operations, risk, authentication, scopes, audit |
| RAG / Vector Store | interface conceitual | pgvector, Milvus, Pinecone, Weaviate, Elasticsearch, cloud vector DB | tenant isolation, authZ, provenance, classification, retrieval policy |
| Secrets | environment/reference | Vault, KMS, cloud secret manager, HSM | encryption, least privilege, rotation, revocation, audit |
| Messaging / Event Bus | não acoplado | Kafka, NATS, Pulsar, RabbitMQ, cloud pub/sub | authenticated producers/consumers, integrity, partitioning, replay controls |
| State Store | in-memory/reference | PostgreSQL, Redis, distributed KV | consistency adequada, isolation, durability conforme criticidade |
| API Gateway | FastAPI direct/reference | Kong, Apigee, Envoy Gateway, cloud API gateway | AuthN/AuthZ hooks, rate limit, logging, schema validation |
| Container Runtime | Docker reference | containerd, CRI-O, microVM, unikernel | isolation, image provenance, runtime controls |
| Orchestrator | Kubernetes reference | K3s, OpenShift, Nomad, edge orchestrator, cloud container platform | lifecycle, identity binding, isolation, admission, policy integration |
| Edge Orchestration | Kubernetes manifests | K3s, KubeEdge, Akri, vendor edge stack, ETSI-aligned MEC platform | local policy enforcement, offline safety, telemetry buffering, node identity |
| Remote Attestation | conceptual hook | TPM attestation, confidential computing attestation, cloud attestation service | signed/measurable platform state, freshness, trust decision integration |
| SBOM | CycloneDX example | SPDX or equivalent | component inventory, version, dependency identity, machine readability |
| AI-BOM / Agent-BOM | project schemas | enterprise AI inventory format | models/agents/tools/dependencies and relationships |
| Formal Verification | TLA+ / Alloy | PlusCal, Coq, Isabelle, Lean, model checker, state-machine verifier | explicit invariants and mechanically checkable properties where required |
| CI/CD | GitHub Actions reference | GitLab CI, Jenkins, Azure DevOps, Tekton, Argo | mandatory gates, evidence, traceability, policy enforcement |
| IaC | Kubernetes YAML reference | Terraform, Pulumi, Helm, Crossplane | versioned infrastructure intent, policy testing, drift visibility |
| Supply-chain Attestation | conceptual | Sigstore, in-toto, SLSA tooling, enterprise signing | provenance, signatures/attestations, verification before admission |
| Incident Response | kill-switch reference | SOAR playbook, EDR response, mesh isolation, platform controller | revoke, isolate, disable, quarantine, trace, evidence preservation |

---

## 71.3 Regra para substituição de componentes

Uma tecnologia só deve substituir outra quando preservar, no mínimo:

```text
Functional Contract
AND Security Contract
AND Audit Contract
AND Failure Contract
AND Revocation Contract
```

### Functional Contract

A nova solução deve cumprir a função arquitetural prevista.

### Security Contract

Deve manter as invariantes de segurança relevantes.

### Audit Contract

Deve gerar evidência suficiente para investigação e compliance.

### Failure Contract

Deve possuir comportamento definido quando estiver indisponível ou degradada.

### Revocation Contract

Deve permitir revogar autoridade, credencial, sessão ou capability quando exigido.

---

## 71.4 Exemplo — substituição de SPIFFE/SPIRE

SPIFFE/SPIRE pode ser substituído.

A solução alternativa, porém, deve preservar:

- workload identity independente de usuário humano;
- identidade única;
- binding da identidade ao workload real;
- rotação de credenciais;
- revogação;
- autenticação mútua quando exigida;
- trust domain explícito;
- suporte a attestation ou mecanismo equivalente para agentes críticos.

Uma simples API key estática compartilhada por vários agentes **não é semanticamente equivalente**.

---

## 71.5 Exemplo — substituição de OPA/Rego

OPA/Rego é apenas a referência de Policy-as-Code.

A solução substituta deve oferecer:

- policy externalizada do agente;
- versionamento;
- decisão auditável;
- deterministicidade suficiente para compliance;
- default deny;
- possibilidade de testes automatizados;
- separação entre Policy Decision e Agent Reasoning;
- suporte a contexto, identidade e risco;
- tratamento explícito de falha.

O LLM não pode ser usado como substituto único do PDP para ações críticas.

---

## 71.6 Exemplo — substituição do service mesh

Istio/Envoy/Linkerd são exemplos.

Uma arquitetura sem service mesh ainda pode implementar o ZTAM, desde que consiga assegurar:

- mTLS ou proteção equivalente;
- identity propagation;
- policy enforcement;
- egress control;
- observabilidade distribuída;
- rate limiting;
- isolation;
- revocation.

---

## 71.7 Exemplo — substituição de OpenTelemetry

OpenTelemetry é uma referência de interoperabilidade.

A solução alternativa deve preservar:

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

Sem correlação distribuída, investigação de incidentes multiagente torna-se incompleta.

---

## 71.8 Exemplo — substituição do Risk Engine

O algoritmo ARS fornecido é deliberadamente simples.

Ele pode ser substituído por:

- scoring estatístico;
- risk graph;
- attack-path analysis;
- Bayesian network;
- rules engine;
- modelo híbrido;
- engine corporativo de risk analytics.

Porém a solução deve ser:

- explicável para decisões críticas;
- versionada;
- testável;
- limitada por policy;
- resistente a inputs ausentes ou manipulados;
- capaz de produzir evidence do motivo da decisão.

---

## 71.9 Exemplo — substituição de Kubernetes

Kubernetes é apenas uma implementação de deployment/orchestration de referência.

Pode ser substituído por outra plataforma, inclusive específica de Edge/MEC, desde que mantenha:

- workload identity;
- lifecycle management;
- isolation;
- network policy ou equivalente;
- admission controls;
- secret management;
- observabilidade;
- rollback;
- capacidade de executar kill/quarantine.

---

## 71.10 Exemplo — substituição de armazenamento de evidências

Evidence-as-Code não depende de JSON local.

Em produção, a organização pode usar:

- object storage imutável;
- WORM;
- SIEM;
- ledger;
- database auditável;
- data lake governado;
- plataforma GRC.

O requisito é preservar:

- integridade;
- origem;
- timestamps;
- retenção;
- controle de acesso;
- correlação;
- cadeia de custódia quando aplicável.

---

## 72. Contratos de integração recomendados

Ao trocar tecnologias, o projeto recomenda interfaces explícitas.

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

Esses contratos são mais importantes que a tecnologia concreta utilizada.

---

## 72A. Formal Integration Port Specification — IPS

Esta seção é **normativa** para a substituibilidade de integrações no SGAEIA.

A arquitetura não considera SPIFFE/SPIRE, OPA/Rego, OpenTelemetry, um service mesh, Kubernetes, Kafka, PostgreSQL ou qualquer produto específico como parte inseparável do núcleo. O elemento estável é a **semântica de segurança e governança da porta de integração**.

O modelo formal é:

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

### 72A.1 Estrutura do IPS

Cada porta em `specs/integrations/ports/*.port.yaml` declara obrigatoriamente:

```text
Functional Contract
Security Contract
Audit Contract
Failure Contract
Revocation Contract
```

Portanto:

```text
ConformantReplacement =
  FunctionalPass
  AND SecurityPass
  AND AuditPass
  AND FailurePass
  AND RevocationPass
  AND NoSecurityInvariantViolation
```

Compatibilidade de protocolo ou de JSON **não é suficiente** para equivalência arquitetural.

### 72A.2 Portas formalizadas

A versão atual formaliza, entre outras:

| Port | Responsabilidade |
|---|---|
| `IP-IDENTITY` | identidade/attestation/revogação de workloads e agentes |
| `IP-PDP` | decisão externa de policy |
| `IP-PEP` | enforcement antes da ação |
| `IP-RISK` | avaliação dinâmica de risco |
| `IP-REGISTRY` | inventário e lifecycle de entidades governadas |
| `IP-EVIDENCE` | evidência, sealing, correlação e exportação |
| `IP-KILL` | pause/quarantine/revoke/terminate |
| `IP-OBS` | telemetria e tracing agentivo |
| `IP-BUS` | eventos assíncronos de controle/governança |
| `IP-MESH` | comunicação Zero Trust agente-a-agente/serviço |
| `IP-STATE` | estado persistente governado |
| `IP-EDGE` | orquestração Edge/MEC com safe degradation |

### 72A.3 Contratos machine-readable

Contratos HTTP de referência ficam em:

```text
specs/integrations/openapi/
```

usando **OpenAPI 3.2.0**.

Contratos orientados a eventos ficam em:

```text
specs/integrations/asyncapi/
```

usando **AsyncAPI 3.1.0**.

Esses formatos descrevem transporte e interoperabilidade. A autoridade normativa continua sendo o contrato semântico da porta, porque um documento OpenAPI/AsyncAPI válido não prova, sozinho, fail-safe, revogabilidade ou evidência adequada.

### 72A.4 Qualificação de uma tecnologia substituta

Uma substituição deverá fornecer um dossier contendo:

1. versão da implementação e porta suportada;
2. mapeamento funcional de todas as operações;
3. análise AuthN/AuthZ, identidade, integridade e isolamento;
4. comportamento durante timeout, perda de dependência e partição;
5. tempo medido de propagação de revogação;
6. evidência produzida e sua correlação;
7. threat model das novas superfícies introduzidas;
8. testes positivos e negativos;
9. rollback/disable de emergência;
10. risco residual e owner para qualquer desvio.

A metodologia está especificada em:

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

`IPS-C3` acrescenta auditabilidade, evidência, revogação, rastreabilidade e lifecycle às propriedades funcionais e de segurança. Portas críticas destinadas à produção SHOULD atingir IPS-C3.

### 72A.6 Failure semantics são parte da API

Nesta arquitetura, falha não é apenas uma exceção técnica. Ela altera autoridade.

Exemplos:

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

Assim, dois produtos que executam a mesma chamada em operação normal podem **não** ser substitutos equivalentes se um deles falhar aberto.

### 72A.7 Revogação como requisito arquitetural

Para cada porta relevante, o projeto registra `maxPropagationSeconds`.

A qualificação deve demonstrar que:

```text
RevocationRequested(t0)
=> AuthorityUnavailable(t <= t0 + MaxPropagation)
```

O valor exato é específico por domínio, mas a propriedade de revogabilidade não é opcional.

### 72A.8 Integração com SDD e GRC

O IPS entra na cadeia SDD:

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

Dessa forma, a troca de um fornecedor deixa de ser apenas uma decisão operacional e passa a ser uma mudança arquitetural verificável, com evidência e impacto de risco explícitos.

### 72A.9 Arquivos normativos adicionados

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

O pipeline valida que cada porta contenha as cinco dimensões contratuais e que as especificações de transporte usem os baselines declarados.

---


## 72B. Adapter Conformance Framework — ACF

Esta seção é **normativa** para a implementação e qualificação dos adapters concretos que materializam as Integration Ports.

O IPS define **o que deve permanecer verdadeiro**. O Adapter Conformance Framework define **como uma tecnologia concreta demonstra que preserva essas propriedades**.

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

### 72B.1 Princípio: adapters implementam portas, não redefinem arquitetura

Um adapter concreto SHALL estar ligado a exatamente uma Integration Port no seu `AdapterProfile`.

A relação é:

```text
Adapter : Technology → IntegrationPortSemantics
```

Não:

```text
Technology → NewSecuritySemantics
```

Assim, SPIRE, OPA, Istio, NATS, Kafka, PostgreSQL, Kubernetes, K3s e OpenTelemetry são implementações substituíveis. Nenhuma delas se torna, por si só, autoridade normativa da arquitetura.

### 72B.2 Adapters executáveis de referência

A versão 0.3.0 inclui adapters no código em:

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

Os adapters usam **transport injection**. Portanto, podem operar sobre:

- HTTP/JSON facade;
- sidecar;
- Unix socket proxy;
- service gateway;
- implementação local;
- test double;
- bridge para gRPC ou APIs nativas.

O core SGAEIA não precisa importar um SDK de fornecedor para preservar a semântica arquitetural.

### 72B.3 Perfis concretos

Os manifests ficam em:

```text
specs/integrations/adapters/*.adapter.yaml
```

Cada perfil declara:

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

Exemplos atuais:

| Adapter | Porta | Implementação de referência | Target |
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

A coexistência de dois adapters para `IP-BUS` e dois para `IP-EDGE` é intencional e demonstra a propriedade de substituibilidade.

### 72B.4 Assurance progressivo: harness não é certificação de produto

A qualificação é explicitamente dividida em estágios:

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

Valida no repositório:

- binding adapter ↔ port;
- operações semânticas;
- outputs estruturados;
- fail-safe básico;
- evidência atribuível;
- revogação lógica;
- comportamento determinístico testável.

#### Q2 / IPS-C2

Exige ambiente representativo ou live e deve testar:

- autenticação real;
- autorização real;
- mTLS/identity binding;
- timeout;
- perda de dependência;
- partição de rede;
- replay;
- malformed input;
- resource exhaustion;
- downgrade/configuration drift;
- isolamento multi-tenant quando aplicável.

#### Q3 / IPS-C3

Acrescenta:

- medição de propagação de revogação;
- evidência operacional correlacionada;
- rollback;
- emergency disable;
- lifecycle/patch policy;
- architecture drift detection;
- residual-risk acceptance;
- GRC approval;
- observabilidade contínua.

Portanto:

```text
ContractHarnessPassed
!=
ProductCertifiedForProduction
```

### 72B.5 Contrato base no código

Todo adapter herda de `BaseIntegrationAdapter` e possui `AdapterMetadata`.

A evidência mínima inclui:

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

Isso permite provar não apenas que `IP-PDP` respondeu, mas **qual implementação e versão concreta respondeu**.

### 72B.6 Adapter Registry

`AdapterRegistry` resolve ports para implementações concretas.

Conceitualmente:

```text
IP-IDENTITY → ADP-SPIRE-IDENTITY
IP-PDP      → ADP-OPA-PDP
IP-MESH     → ADP-ISTIO-MESH
IP-BUS      → ADP-NATS-BUS OR ADP-KAFKA-BUS
IP-EDGE     → ADP-K8S-EDGE OR ADP-K3S-EDGE
```

Um deployment profile seleciona **uma implementação ativa por porta** no contexto daquele deployment.

### 72B.7 Transport Injection

O adapter separa:

```text
Semantic Contract
      ↓
Adapter Logic
      ↓
Transport Interface
      ↓
Vendor / Platform API
```

Isso permite substituir, por exemplo:

```text
HTTP facade → gRPC bridge
```

sem alterar o PDP contract, ou:

```text
NATS → Kafka
```

sem alterar o contrato `IP-BUS`.

O transport não decide política arquitetural; ele apenas materializa a integração.

### 72B.8 Failure semantics executáveis

Os adapters de referência codificam o comportamento esperado durante falhas.

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

### 72B.9 Revogação independente

Adapters críticos mantêm um caminho de revogação que não depende do agente controlado.

A propriedade continua:

```text
Autonomy ⇒ Revocability
```

E, para produção:

```text
MeasuredRevocationTime <= Port.maxPropagationSeconds
```

O harness demonstra a semântica; Q2/Q3 devem medir a propagação real da tecnologia implantada.

### 72B.10 Substituição NATS ↔ Kafka

NATS e Kafka têm APIs, modelos operacionais e características internas diferentes. A arquitetura não exige equivalência interna.

Exige equivalência na porta:

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

Logo:

```text
NATS ≈ Kafka
```

somente **no limite semântico da `IP-BUS`** e somente após ambos satisfazerem o nível de assurance requerido.

### 72B.11 Substituição Kubernetes ↔ K3s

Analogamente:

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

K3s pode ser apropriado ao Edge por seu perfil operacional, enquanto Kubernetes upstream ou distribuições empresariais podem ser adequados em outros tiers. A escolha não altera as invariantes.

### 72B.12 Deployment Profiles

Perfis em:

```text
specs/integrations/deployment-profiles/
```

selecionam adapters concretos para um contexto.

Exemplo Edge:

```text
Identity  = SPIRE
PDP       = OPA
Mesh      = Istio/Envoy
Telemetry = OpenTelemetry
Bus       = NATS
State     = PostgreSQL
Edge      = K3s
```

Exemplo enterprise/cloud:

```text
Identity  = SPIRE
PDP       = OPA
Mesh      = Istio/Envoy
Telemetry = OpenTelemetry
Bus       = Kafka
State     = PostgreSQL
Edge      = Kubernetes
```

Esses perfis são referências de composição e não endorsements de fornecedor.

### 72B.13 Reference baselines e version skew

`specs/integrations/reference-baselines.md` registra baselines observados em setembro de 2026.

Esses números servem para reprodutibilidade documental, não como regra `latest`.

Produção SHOULD definir:

```text
minimum supported version
maximum validated version
upgrade window
security patch SLA
compatibility matrix
rollback version
EOL policy
```

Um upgrade de tecnologia é uma mudança SDD quando pode alterar semântica, superfície de ataque, failure mode ou evidência.

### 72B.14 Conformance report como Evidence-as-Code

O comando:

```bash
python scripts/run_adapter_conformance.py
```

produz:

```text
evidence/adapter-conformance.generated.json
```

com:

- adapter;
- port;
- target level;
- checks;
- resultado;
- scope de assurance.

O relatório declara explicitamente que se trata de **offline contract harness / IPS-C1**, evitando confusão com certificação live.

### 72B.15 CI/CD gate

O pipeline agora executa:

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

Uma alteração de adapter que quebre port binding, failure semantics ou evidence attribution deve bloquear o pipeline.

### 72B.16 SDD traceability do ACF

O ACF acrescenta os requisitos `SR-020…SR-024` e controles `CTL-INT-005…CTL-INT-009`.

A cadeia passa a ser:

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

### 72B.17 Critério formal de admissão de adapter

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

onde:

- `A` = adapter;
- `P` = Integration Port;
- `E` = deployment environment.

### 72B.18 Critério de substituição segura

A tecnologia `A₂` somente pode substituir `A₁` quando:

```text
Implements(A₁,P)
AND Implements(A₂,P)
AND Assurance(A₂,E) >= RequiredAssurance(P,E)
AND SecurityInvariantsPreserved(A₂,E)
```

Logo, substituibilidade deixa de ser uma opinião arquitetural e passa a possuir **critério testável, evidência e decisão de risco**.

### 72B.19 Arquivos adicionados pelo Adapter Conformance Framework

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

O ACF transforma a propriedade **vendor-neutral** em uma característica arquitetural verificável e continuamente testável.

---


## 72C. GitHub Public Release Profile — v0.3.2

A publicação do SGAEIA como repositório público introduz uma nova superfície de governança e supply chain. Por isso, a preparação para GitHub é tratada como parte do SDD, e não apenas como empacotamento do código.

### 72C.1 Princípio

```text
PublicVisibility
       !=
ReducedSecuritySemantics
```

Abrir o repositório a contribuições externas não altera os invariantes de identidade, autorização, revogação, fail-secure, evidence-as-code e autonomia governada. Toda contribuição continua sujeita à cadeia:

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

### 72C.2 Arquivos públicos de governança

A release inclui:

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
- templates de Issues e Pull Requests;
- Dependabot;
- CI de validação SDD/testes/conformidade;
- CodeQL;
- gate de validação de releases por tag.

### 72C.3 Licenciamento

A licença padrão desta release é **Apache-2.0**. Ela foi escolhida para facilitar uso, modificação e redistribuição da referência, com concessão explícita de patente prevista pela licença e preservação das condições de copyright/licença. Antes da publicação, o mantenedor pode substituir a licença se houver uma decisão jurídica ou estratégica diferente.

A presença de nomes como SPIFFE/SPIRE, OPA, Istio, Envoy, OpenTelemetry, NATS, Kafka, PostgreSQL, Kubernetes ou K3s descreve pontos de integração de referência. Não implica certificação, endosso ou afiliação com os respectivos projetos.

### 72C.4 Public security disclosure

Vulnerabilidades não devem ser abertas inicialmente como Issues públicas. `SECURITY.md` define a divulgação coordenada e recomenda habilitar **GitHub Private Vulnerability Reporting** quando o repositório estiver publicado.

Falhas particularmente relevantes incluem bypass de:

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

### 72C.5 CI de repositório público

O workflow principal executa uma matriz de Python suportada e verifica:

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

CodeQL é executado separadamente para análise estática de segurança. Dependabot monitora dependências Python e GitHub Actions. A configuração usa `dependabot.yml` versão 2, conforme o formato atual documentado pelo GitHub.

### 72C.6 Assurance e não-certificação

É proibido inferir:

```text
GitHub CI PASS
      ⇒
Production Certified
```

O resultado correto é:

```text
GitHub CI PASS
      ⇒
Specified repository checks passed
```

IPS-C2/C3, ambientes L4, OT/ICS ou sistemas cyber-physical exigem evidência do ambiente real/representativo, além de avaliação independente conforme o domínio.

### 72C.7 Branch e release governance

Recomenda-se:

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

A política completa está em `docs/github-public-release.md`.

### 72C.8 Citação

`CITATION.cff` permite que GitHub e ferramentas acadêmicas apresentem metadados de citação do SGAEIA. A release registra:

```text
SGAEIA — Secure Governed Autonomous Edge Intelligence Architecture
Aridio Silva — @aridiosilva
Version 0.3.2
September 2026
Apache-2.0
```

### 72C.9 Tópicos sugeridos para o GitHub

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

A primeira publicação pública somente deve ser considerada pronta quando:

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

O checklist operacional detalhado encontra-se em `docs/github-public-release.md`.

## 73. Padrões de implantação suportáveis

A arquitetura pode ser adaptada para:

### Cloud-centric

Cloud concentra control plane; Edge executa operações locais de baixa latência.

### Hierarchical Edge/MEC

PDPs e controls são distribuídos entre Cloud, região, MEC e Edge.

### Sovereign Edge

Edge mantém capacidade mínima segura mesmo desconectado.

### OT / Cyber-Physical

Ações físicas exigem controles de safety, interlocks e possibilidade de emergency stop independentes do LLM.

### Multi-organization / Federated

Trust domains separados negociam identidade, capabilities e políticas sem presumir confiança implícita.

---

## 74. Arquitetura de integração de referência

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

A tecnologia concreta em cada bloco é substituível. A semântica de segurança não é.

---

## 75. Integração com frameworks

O projeto foi desenhado para permitir crosswalk com, conforme aplicabilidade:

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
- IEC 62443 em OT/ICS;
- SPIFFE/SPIRE ou workload identity equivalente.

Consulte `docs/references.md` e `specs/compliance/`.

---

## 76. Métricas GRC e de postura agentiva

KPIs/KRIs recomendados:

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

Uma organização pode derivar um **Agent Security Posture Score — ASPS**:

```text
ASPS = 100 - (
    RiskPenalty
  + ControlGap
  + BehaviorPenalty
  + CompliancePenalty
)
```

---

## 77. Responsabilidades organizacionais

### Board / Executive

Define:

- risk appetite;
- accountability;
- AI governance principles.

### AI Governance Board

Define:

- AI policy;
- autonomy levels;
- prohibited uses;
- approval criteria.

### CISO

Responsável por:

- security architecture;
- cyber threat model;
- incident response.

### CRO / GRC

Gerencia:

- risk;
- compliance;
- exceptions;
- residual risk acceptance workflow.

### Agent Owner

Responde pelo agente e seu propósito.

### Platform Engineering

Opera:

- identity;
- policy;
- agent mesh;
- registries;
- platform controls.

### SOC

Monitora:

- anomalias;
- attack paths;
- policy violations;
- incidents.

Nenhum agente produtivo deve possuir:

```text
Owner = NULL
```

---

## 78. Governed Agent — definição formal

Um agente é governado quando:

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

Se uma condição obrigatória não estiver satisfeita:

```text
Governed(A) = false
```

---

## 79. Secure Agentic System — definição formal

O sistema busca a propriedade:

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

Essa é uma meta arquitetural; níveis de assurance reais dependem da implementação e verificação de cada domínio.

---

## 80. Estado atual do repositório

Esta versão inclui:

- implementação Python mínima;
- FastAPI;
- Agent Registry;
- PDP/PEP de referência;
- Risk Engine;
- Delegation Controller;
- Kill Switch;
- Evidence Service;
- manifests YAML/JSON;
- schemas;
- OPA/Rego de referência;
- OpenAPI da API de controle e **OpenAPI 3.2.0** para Integration Ports HTTP;
- **AsyncAPI 3.1.0** para contratos de eventos;
- **12 Integration Port Specifications (IPS)** machine-readable;
- matriz de conformidade e procedimento de qualificação de tecnologias substitutas;
- **Adapter Conformance Framework (ACF)** com 9 perfis concretos de referência;
- adapters executáveis para SPIRE, OPA, Istio/Envoy, OpenTelemetry, NATS, Kafka, PostgreSQL, Kubernetes e K3s;
- deployment profiles `enterprise-cloud` e `edge-k3s`;
- relatório `Evidence-as-Code` de conformidade dos adapters;
- Docker;
- Kubernetes manifests;
- OpenTelemetry config;
- threat-model artifacts;
- risk/control catalogs;
- AI-BOM e Agent-BOM;
- formal models em TLA+ e Alloy;
- testes unitários, integração, segurança, adversariais, formais e de conformidade IPS em Python.

Estado verificado desta revisão:

```text
SPEC VALIDATION PASSED
INTEGRATION PORT VALIDATION PASSED
31 tests passed
```

---

## 81. Limitações atuais

Esta referência não deve ser interpretada como produto pronto para ambientes críticos.

Antes de produção, devem ser implementados e validados, conforme o caso:

1. trust domains reais e PKI/workload identity;
2. PDP/PEP corporativo;
3. inventário/discovery real de agentes, modelos e tools;
4. integração IAM/PAM/NHI;
5. SIEM/SOAR/GRC;
6. RAG provenance e data classification;
7. attestation de Edge nodes;
8. red team específico do caso de uso;
9. safety case para L4;
10. mapeamento regulatório de jurisdição/setor;
11. qualificação IPS-C2/C3 em ambientes reais para cada adapter selecionado;
12. medição real de revogação, failover, partição e version-skew dos produtos implantados;
12. BCP/DR;
13. testes de isolamento e desconexão;
14. assinatura/provenance de artefatos;
15. secrets management real;
16. data plane encryption;
17. service-mesh ou enforcement equivalente;
18. immutable evidence storage;
19. incident-response runbooks;
20. model supply-chain controls;
21. validação independente de security e safety.

---

## 82. Próxima evolução recomendada

A evolução natural desta versão é decompor a implementação mínima em serviços reais:

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

E integrar componentes de produção substituíveis para:

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

Uma etapa posterior pode transformar o repositório em um **Cyber Range Edge-AI Multiagente**, capaz de executar cenários controlados de:

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

O objetivo seria demonstrar não apenas a ameaça, mas a resposta automática de:

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

## 83. Referências

Consulte:

```text
docs/references.md
specs/compliance/
specs/threat-model/
```

Referências centrais incluem NIST, ISO/IEC, OWASP, MITRE, ETSI, SPIFFE e IEC conforme o domínio.

---

## 84. Licenciamento

Este repositório é fornecido como material de referência técnica.

A organização que o adotar deve:

- definir o licenciamento de sua implementação;
- revisar licenças das dependências;
- revisar requisitos dos padrões utilizados;
- realizar análise legal e regulatória aplicável.

---

## 85. Síntese da arquitetura

O objetivo desta arquitetura é estabelecer uma condição na qual:

> **nenhum agente confia implicitamente em outro agente; nenhuma ação crítica deriva exclusivamente da decisão probabilística de um modelo; toda identidade, capability e delegação é verificável; toda ação relevante é observável; toda autoridade possui limites; e toda autonomia relevante é reversível.**

A tese final é:

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

Inteligência pode ser distribuída.

**Autoridade deve permanecer explicitamente governada.**


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
