# Formal Models

Este diretório contém modelos de referência para as invariantes centrais. Eles não substituem a modelagem completa de um deployment específico.

- `tla/SGAEIA.tla`: máquina de estados para lifecycle/autorização/revogação.
- `alloy/sgaeia.als`: relações entre agentes, capabilities e delegações.
- `tests/formal/test_invariants_state_space.py`: exploração finita executável no pipeline Python.

## Propriedades-alvo
1. agentes não registrados/revogados não podem executar;
2. L4+A5 não pode ser autorizado;
3. delegação não aumenta capabilities;
4. profundidade de delegação não excede o limite;
5. offline+critical não é autorizado no perfil de referência;
6. ação física só é admitida para agente L4 e sob controles adicionais.
