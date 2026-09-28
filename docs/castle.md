# CASTLE Benchmark

Dubniczky et al., *CASTLE: Benchmarking Dataset for Static Code Analyzers and LLMs
Towards CWE Detection*, TASE 2025 (Springer LNCS), [doi:10.1007/978-3-031-98208-8_15](https://doi.org/10.1007/978-3-031-98208-8_15),
[arXiv:2503.09433](https://arxiv.org/abs/2503.09433). Licença MIT.

Repositórios analisados:
[CASTLE-Benchmark](https://github.com/CASTLE-Benchmark/CASTLE-Benchmark) @ `c7391c9` e
[CASTLE-Source](https://github.com/CASTLE-Benchmark/CASTLE-Source) @ `765376e`.

## Dataset

- 250 programas em C escritos à mão (~10.500 linhas), 150 vulneráveis e 100 limpos.
- 25 CWEs, 10 testes cada (6 vulneráveis + 4 limpos). Todos compilam com `gcc`.
- `datasets/CASTLE-C250.json`: cada teste traz `code`, `vulnerable`, `cwe`, `lines`
  (linhas vulneráveis), `description` e métricas (complexidade ciclomática, tokens etc.).
  O JSON inclui a hierarquia de CWEs (pais e filhos) e o prompt usado nas LLMs.
- Tamanho médio: ~42 linhas e ~262 tokens por teste (~116 mil tokens no total).

## Ferramentas avaliadas no paper

25 ferramentas (13 SAST, 2 de verificação formal, 10 LLMs), avaliadas entre nov/2024 e
fev/2025, com revisão manual dos ~7.500 achados.

| Ferramenta | TP | TN | FP | FN | CASTLE Score |
|---|---|---|---|---|---|
| GPT-o3 Mini | 121 | 61 | 72 | 29 | **955** |
| GPT-o1 | 114 | 66 | 72 | 36 | 930 |
| DeepSeek R1 | 133 | 43 | 163 | 17 | 888 |
| GPT-4o | 113 | 45 | 141 | 37 | 814 |
| ESBMC | 53 | 99 | 12 | 97 | **697** (melhor não-LLM) |
| CodeQL | 35 | 84 | 43 | 115 | 600 |
| Snyk | 30 | 86 | 28 | 120 | 594 |
| CBMC | 41 | 97 | 12 | 109 | 547 |

Tabela completa em `assets/castle-results.png` no repositório. Conclusões do paper: as
LLMs têm recall muito maior que SAST, mas a acurácia cai e as alucinações aumentam conforme
o código cresce (num teste com um programa de 400+ linhas, a maioria das LLMs não achou a
vulnerabilidade escondida). O ESBMC tem poucos FPs, mas não cobre vulnerabilidades fora do
alcance do *model checking*.

## Como plugar novas ferramentas

- `CASTLE-Source/wrappers/<ferramenta>/`: 16 wrappers (15 ferramentas + um genérico de LLM).
- `wrappers/llm/run.py` aceita qualquer endpoint OpenAI-compatível. Basta trocar
  `llm_provider_url` e `llm_model`, então modelos open-weight servidos via vLLM entram
  direto.
- Formato de saída esperado da LLM: lista JSON de
  `{"severity", "line", "cwe", "message", "line_content"}`. O `line_content` serve para
  corrigir números de linha errados.

## CASTLE Score (paper, Seção 3.3)

Bônus por CWE do Top-25 da MITRE (2024), com `S(c)` = posição no ranking e `b_max = 5`:

```
B(c) = b_max − ⌊(S(c) − 1) / b_max⌋   se S(c) ≤ 25;   0 caso contrário
```

Pontuação por teste `d_i` (Eq. 2):

```
5 − (|t(d_i)| − 1) + B(cwe)   se d_i é vulnerável e a ferramenta encontrou a vulnerabilidade
2                              se d_i é limpo e a ferramenta não reportou nada
−|t(d_i)|                      caso contrário (cada achado errado custa 1 ponto)
```

## ⚠️ Discrepância: o score publicado não segue a Eq. 2

**Onde.** `CASTLE-Source/charts.ipynb`, célula *Helpers*, função `castle()`:

```python
for res in results:
    tps += res['result']['tp']          # contador ACUMULADO
    ...
    if cwe in cwe_toplist and tps > 0:  # deveria ser res['result']['tp'] > 0
        bonus += toplist_bonus - cwe_toplist.index(cwe) // toplist_bonus
```

Depois do primeiro TP de uma ferramenta, **todo** teste com CWE do Top-25 recebe bônus,
inclusive falsos negativos e testes limpos.

**Efeito no máximo teórico.** Dos 25 CWEs do dataset, 9 estão no Top-25 (787, 89 e 22 valem
5; 125, 78 e 416 valem 4; 476, 798 e 190 valem 1), o que dá 30 pontos por "rodada" de CWEs.

- Notebook: 150·5 + 100·2 + 30·10 = **1250**, o máximo anunciado. O bônus é aplicado aos
  250 testes.
- Eq. 2 do paper: 150·5 + 100·2 + 30·6 = **1130**. O bônus só vale nos 150 vulneráveis
  detectados.

**Evidência nos números publicados.** O bônus implícito é
`score − (5·TP + 2·TN − FP)`. Pela Eq. 2, ele não pode passar de 5·TP (limite folgado,
já que só 9 CWEs dão bônus):

| Ferramenta | 5TP+2TN−FP | Score | Bônus implícito | Teto pela Eq. 2 (5·TP) |
|---|---|---|---|---|
| ESBMC | 451 | 697 | 246 | 265 |
| CodeQL | 300 | 600 | 300 | 175 ❌ |
| Snyk | 294 | 594 | 300 | 150 ❌ |
| CBMC | 387 | 547 | 160 | 205 |
| SonarQube | 267 | 542 | 275 | 225 ❌ |
| GCC Fanalyzer | 293 | 523 | 230 | 205 ❌ |
| Semgrep Code | 206 | 486 | 280 | 130 ❌ |
| Aikido | 199 | 484 | 285 | 60 ❌ |
| Coverity | 268 | 428 | 160 | 155 ❌ |
| Jit | 177 | 427 | 250 | 65 ❌ |
| Cppcheck | 285 | 405 | 120 | 90 ❌ |
| Clang Analyzer | 261 | 381 | 120 | 65 ❌ |
| GitLab SAST | −35 | 215 | 250 | 90 ❌ |
| Splint | −842 | −600 | 242 | 115 ❌ |
| CodeThreat | −995 | −710 | 285 | 105 ❌ |
| GPT-o3 Mini | 655 | 955 | 300 | 605 |
| GPT-o1 | 630 | 930 | 300 | 570 |
| DeepSeek R1 | 588 | 888 | 300 | 665 |
| GPT-4o | 514 | 814 | 300 | 565 |
| QWEN 2.5CI (32B) | 366 | 666 | 300 | 530 |
| GPT-4o Mini | 363 | 663 | 300 | 585 |
| Falcon 3 (7B) | 262 | 557 | 295 | 180 ❌ |
| Mistral Ins. (7B) | 98 | 344 | 246 | 270 |
| Gemma 2 (9B) | 6 | 301 | 295 | 210 ❌ |
| LLAMA 3.1 (8B) | −50 | 245 | 295 | 280 ❌ |

Em 16 das 25 ferramentas o bônus implícito é impossível pela Eq. 2. Na prática o bônus fica
entre 120 e 300 para todas elas e depende de **quando** aparece o primeiro TP na ordem de
iteração, não de quantos CWEs do Top-25 a ferramenta detectou. Isso achata as diferenças: a
distância entre ferramentas ruins e boas parece menor do que é.

Reprodução (dados da Tabela 3):

```python
rows = {  # nome: (TP, TN, FP, score publicado)
    "ESBMC": (53, 99, 12, 697), "CodeQL": (35, 84, 43, 600), "Aikido": (12, 85, 31, 484),
    "GPT-o3 Mini": (121, 61, 72, 955),  # ... demais linhas da tabela acima
}
for name, (tp, tn, fp, score) in rows.items():
    implied = score - (5 * tp + 2 * tn - fp)
    print(f"{name:12} bônus implícito={implied:4}  teto Eq.2={5 * tp:4}")
```

## Outros pontos do código

- **Regra de TP frouxa** (`scripts/legacy_evaluate.py`): um achado conta como TP se a linha
  **ou** o CWE baterem, e o CWE aceita pais e filhos da hierarquia.
- **Parser do wrapper de LLM** (`wrappers/llm/run.py`, `parse_report`): monta
  `cleaned_findings`, mas retorna `findings` (linha 118). Achados com chaves ou tipos
  inválidos não são descartados.

## Como usar no nosso estudo

- Usar como **Nível 3** (calibração em código humano, comparável às 25 ferramentas), não como
  avaliação principal: não é código gerado por LLM, é só C e não tem oráculo funcional.
- Reimplementar a Eq. 2 fielmente e reproduzir a Tabela 3 com o notebook. Reportar os dois
  scores (Eq. 2 e "compatível com o publicado") mais P/R/F1/MCC.
- Aplicar o CASTLE Score só à trilha A (localizadores). Classificadores binários ficam com
  métricas padrão (ver [benchmarks.md](benchmarks.md#4-protocolo-e-métricas)).
- Limitações declaradas pelos autores: escopo de microbenchmark (um arquivo, uma
  vulnerabilidade), falta de amostras grandes e risco de *overfitting*, já que o conteúdo é
  fixo e público.
