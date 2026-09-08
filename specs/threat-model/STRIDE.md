# STRIDE aplicado ao sistema agentivo

| STRIDE | Manifestação |
|---|---|
| Spoofing | agent/workload impersonation |
| Tampering | prompt, memory, RAG, model or policy tampering |
| Repudiation | ações sem provenance/trace |
| Information Disclosure | exfiltração por tool/RAG/A2A |
| Denial of Service | loops, token/GPU/API exhaustion |
| Elevation of Privilege | capability/delegation escalation |

STRIDE deve ser complementado por ameaças semânticas de IA: goal hijacking, indirect prompt injection, memory/RAG poisoning, tool abuse, collusion e autonomy escalation.

## RC2 — Alien cognition and collective agency extensions

| STRIDE | Threat | Required response |
|---|---|---|
| Spoofing | Agent impersonates an independent monitor or approver | workload identity, signed decision provenance, independence check |
| Tampering | Agent changes policy, monitor, evidence, identity or kill-switch state | protected-control path, separation of duties, tamper-evident evidence |
| Repudiation | Delegated agent denies participation in a multi-agent action | attributable delegation chain and correlated trace |
| Information Disclosure | Agents combine partial access to reconstruct protected information | collective authorization and aggregate data-flow evaluation |
| Denial of Service | Coordinated agents exhaust runtime, tools, network or evidence capacity | enforceable budgets, quarantine and safe degradation |
| Elevation of Privilege | Agents aggregate individually allowed capabilities into a prohibited operation | graph-level privilege aggregation detection |

Cross-cutting threats include deceptive explanation, monitor probing, sandbagging,
self-affecting change, distributed policy evasion and cumulative low-risk actions.
