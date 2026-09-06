# Agent Trust Zones

| Zone | Name | Assumption |
|---|---|---|
| ATZ-0 | External/Unknown | nenhuma confiança |
| ATZ-1 | Untrusted Inputs | conteúdo hostil esperado |
| ATZ-2 | Sandboxed Agents | autoridade mínima |
| ATZ-3 | Enterprise Agents | confiança condicionada |
| ATZ-4 | Privileged Agents | step-up e controles reforçados |
| ATZ-5 | Cyber-Physical Critical | criticidade máxima, nunca confiança implícita |

## Transition rule
`AuthN ∧ AuthZ ∧ Policy ∧ Risk ∧ Context ∧ Trust => ALLOW`, caso contrário `DENY`.

## Offline rule
`Offline => authority <= cached_safe_authority`.
