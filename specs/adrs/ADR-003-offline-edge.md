# ADR-003 — Edge offline opera com autoridade reduzida

## Status
Accepted.

## Decision
Cache local de políticas seguras com expiry. Operações críticas desconhecidas são negadas durante partition.

## Consequences
Disponibilidade funcional pode degradar; segurança não é relaxada automaticamente.
