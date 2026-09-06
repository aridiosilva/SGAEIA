# ADR-001 — O modelo não é a autoridade de segurança

## Status
Accepted.

## Context
LLMs são probabilísticos e podem sofrer prompt injection, erro ou manipulação.

## Decision
Toda ação sensível passa por PDP/PEP determinístico/independente do modelo.

## Consequences
Mais latência e complexidade, porém menor blast radius e melhor auditabilidade.
