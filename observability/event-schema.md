# Agentic Security Event Schema

Campos mínimos para ações relevantes:
- timestamp
- trace_id
- evidence_id
- agent_id / workload identity
- model_id/version quando aplicável
- intent/operation/resource
- trust_zone
- policy decision
- risk score
- delegation chain
- tool call
- human approval reference
- outcome
- integrity digest

Conteúdo sensível de prompts deve ser tratado por classificação e minimização; hashes/referências podem ser preferíveis a logs integrais.
