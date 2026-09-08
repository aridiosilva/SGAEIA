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
| INV-011 | raciocínio ou explicação do modelo não autoriza ação |
| INV-012 | monitor de ação crítica deve ser válido e independente |
| INV-013 | autonomia efetiva jamais excede assurance de monitoramento, contenção e recuperação |
| INV-014 | agente não altera controles protegidos por autorização operacional comum |
| INV-015 | agente não aprova sozinho mudança que afete suas próprias capacidades ou controles |
| INV-016 | autoridade coletiva não emerge da agregação de privilégios individualmente insuficientes |
| INV-017 | limites de tempo, ferramentas, rede e delegação são fail-closed |
| INV-018 | divergência entre ação proposta e efeito observado impede execução crítica |
