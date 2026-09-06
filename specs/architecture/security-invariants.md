# Security Invariants

| ID | Invariant |
|---|---|
| INV-001 | agente sem identidade válida não executa ação |
| INV-002 | agente desconhecido não recebe autorização |
| INV-003 | L4+A5 é proibido |
| INV-004 | delegação não aumenta autoridade |
| INV-005 | profundidade de delegação nunca supera limite |
| INV-006 | criação e aprovação de operação crítica não podem ser da mesma identidade |
| INV-007 | falha de attestation em agente crítico causa deny/quarantine |
| INV-008 | modo offline reduz ou mantém autoridade; jamais amplia |
| INV-009 | toda ação crítica deve produzir evidence_id e trace_id |
| INV-010 | kill switch deve ser independente do agente controlado |
