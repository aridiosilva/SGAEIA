# Agent Risk Method

## Dimensões
- autonomia;
- privilégio;
- sensibilidade dos dados;
- poder das tools;
- alcance de rede;
- delegação;
- impacto financeiro/físico;
- comportamento/anomalia.

Cada dimensão recebe 0–5. Pesos padrão somam 20 e o resultado é normalizado para 0–100.

## Faixas de referência
- 0–20: ALLOW
- 21–40: ALLOW + telemetry
- 41–60: RESTRICT / step-up
- 61–80: REQUIRE_APPROVAL
- 81–90: QUARANTINE
- 91–100: DENY/REVOKE

Thresholds são exemplos e devem ser calibrados ao risk appetite.
