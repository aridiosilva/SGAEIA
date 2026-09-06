# Agent Registry Specification

Todo agente de produção MUST possuir registro único, owner humano/organizacional, purpose, classe, autonomia, trust zone, identidade criptográfica, capabilities, ferramentas autorizadas, política de delegação, risco, controles, lifecycle e kill switch.

## Lifecycle
`REGISTERED → VALIDATED → AUTHORIZED → RUNNING → {PAUSED|QUARANTINED|REVOKED|TERMINATED}`.

Transição `UNKNOWN → RUNNING` é proibida.
