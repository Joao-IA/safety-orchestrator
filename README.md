# LLM Safety-Classifier Benchmark — Infra (Passo 1)

Infraestrutura de experimento para medir o **custo de capacidade do classificador
de segurança do Fable 5** vs. Opus 4.8 (fallback divulgado), em tarefas defensivas
de identificação de vulnerabilidades.

## Postura metodológica (importante)

O **disparo do classificador é a variável dependente**, não um obstáculo.
Portanto o código, por design:

- **não faz retry** quando o classificador bloqueia (`FLAGGED` é uma observação);
- **não reescreve prompts** para evitar o flag — isso destruiria a medição;
- registra, por chamada, o estado do classificador: `normal / fallback / flagged / error`.

Todos os prompts são **defensivos** (identificar/classificar CWE, causa-raiz, correção).
**Nunca** se pede geração de exploit funcional.

## Estrutura

```
configs/config.yaml     # um arquivo = um experimento reprodutível (seed, modelos, sample)
src/config.py           # carrega config + API key (.env)
src/models.py           # ClassifierState + CallResult (dado primário, serializável)
src/client.py           # 1 chamada -> classifica em normal/fallback/flagged/error
src/cache.py            # cache em disco por (item, modelo, prompt): idempotência
src/cost.py             # tokens/custo por execução
src/runner.py           # engine: cache + client + custo (consumida pelo passo 3)
scripts/smoke_test.py   # valida a infra SEM gastar API
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # e preencha ANTHROPIC_API_KEY
python -m scripts.smoke_test   # deve imprimir "SMOKE TEST OK"
```

## Pontos a ajustar ao seu endpoint

Toda parte específica do ambiente está isolada em `src/client.py`:
`_extract_flag_category`, `_is_safeguard_flag`, `_served_model`. Ajuste os campos
conforme o contrato real da sua API (o erro observado traz `Details: [cyber]` + Request ID).

## Próximo (Passo 3 — orquestrador)

Aqui entra a decisão de linguagem do Juliet (**C/C++** recomendado): o parser de
ingestão é a única parte específica de linguagem.

- ingestão do Juliet: parsear pares good/bad → `item_id`, código, CWE ID (ground truth);
  **good e bad como amostras separadas**;
- fatia complementar de CVE-corrigido/CTF para a métrica de trigger-rate realista;
- template de prompt defensivo; `runner.run_both_models(item_id, prompt)`;
- scoring contra ground truth + agregação das 3 métricas core.
