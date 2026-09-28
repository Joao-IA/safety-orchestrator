# Benchmarks

## 1. Requisitos

O que o benchmark precisa oferecer para avaliar um fiscal de código gerado por LLM:

| # | Requisito | Por quê |
|---|---|---|
| R1 | **Código gerado por LLM** | O fiscal vai ver a distribuição de código que LLMs produzem, não código humano |
| R2 | **Rótulo independente das ferramentas avaliadas** (oráculo dinâmico: testes/exploits) | Rótulo vindo de SAST/ESBMC/ICD favorece a própria ferramenta (circularidade) |
| R3 | **Amostras seguras e inseguras** | Falso positivo bloqueia o usuário; a taxa de FP é métrica central para um plugin |
| R4 | Localização (CWE + linha/função) | Necessária para avaliar explicação e correção (desejável) |
| R5 | Múltiplas linguagens | LLMs geram majoritariamente Python/JS/Go além de C |
| R6 | Oráculo funcional + de segurança | Permite avaliar o loop gerar → fiscalizar → corrigir → re-verificar sem regressão |
| R7 | Revisado por pares, público, licença utilizável | Aceitação pelos revisores e reprodutibilidade |
| R8 | Contaminação controlável | Modelos treinados após a publicação podem ter visto os dados |

## 2. Candidatos avaliados

Legenda: ✅ atende · ⚠️ parcial · ❌ não atende

| Benchmark | Venue | R1 | R2 | R3 | R4 | R5 | R6 | Uso no estudo |
|---|---|---|---|---|---|---|---|---|
| **CWEval** | LLM4Code @ ICSE 2025 | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | **Nível 1 e 2** |
| **BaxBench** | ICML 2025 | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | **Nível 1 e 2** |
| **SeCodePLT** | NeurIPS 2025 D&B | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | ✅ | **Nível 1 e 3** |
| **SusVibes** | ICML 2026 | ✅ | ✅ | ✅ | ❌ | ⚠️ | ✅ | **Nível 2** |
| **SecRepoBench** | LLM4Code 2026 | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | Nível 2 (opcional, C/C++) |
| **CASTLE** | TASE 2025 | ❌ | ⚠️ | ✅ | ✅ | ❌ | ❌ | **Nível 3** |
| **PrimeVul** | ICSE 2025 | ❌ | ⚠️ | ✅ | ⚠️ | ❌ | ❌ | Nível 3 (classificadores) |
| FormAI / FormAI-v2 | PROMISE 2023 / preprint | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | Só com ressalva (rótulo = ESBMC) |
| CyberSecEval | preprint (Meta) | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | Só com ressalva (rótulo = ICD) |
| Juliet (NIST SARD) | — | ❌ | ✅ | ✅ | ✅ | ⚠️ | ❌ | Não recomendado (contaminação) |
| **AutoPenBench** | EMNLP 2025 Industry | ❌ | — | ❌ | ❌ | — | ❌ | **Fora do escopo** |
| CyberGym | ICLR 2026 | ❌ | ✅ | ❌ | ❌ | ⚠️ | ❌ | Contexto |
| ExploitGym | preprint (2026) | ❌ | ✅ | ❌ | ❌ | ⚠️ | ❌ | Contexto |

### Notas por candidato

**CWEval** — 119 tarefas, 31 CWEs, em C, Go, JavaScript e Python. Cada tarefa tem oráculo
de funcionalidade e de segurança executados em Docker (métricas `func@k` e `func-sec@k`).
Gera respostas de qualquer endpoint OpenAI-compatível. Apache-2.0.
[paper](https://arxiv.org/abs/2501.08200) · [código](https://github.com/Co1lin/CWEval)

**BaxBench** — 392 tarefas (28 cenários × 14 frameworks, 6 linguagens) de *backends*.
Funcionalidade validada por testes e segurança validada executando *exploits* ponta a ponta.
Mesmo o melhor modelo avaliado (o1) chega a 62% de corretude, e cerca de metade dos
programas corretos é explorável.
[paper](https://arxiv.org/abs/2502.11844) · [site](https://baxbench.com/)

**SeCodePLT** — splits de *secure coding*, *vulnerability detection* e *patch generation*
para C/C++, Python e Java (~1.240 amostras por split). No split de detecção em C, o código
vem do ARVO (vulnerabilidades reais do OSS-Fuzz), com par vulnerável/corrigido e imagem
Docker com PoC. Ou seja, é código humano com rótulo dinâmico. O split de *secure coding*
serve para gerar código com LLMs e rotular por execução. Licença do dataset: verificar.
[paper](https://arxiv.org/abs/2410.11096) · [código](https://github.com/ucsb-mlsec/SeCodePLT) · [dados](https://huggingface.co/datasets/UCSB-SURFI/SeCodePLT)

**SusVibes** — 186 tarefas de *feature request* em repositórios reais (Python), com
~175 linhas editadas sobre ~236 mil linhas de contexto. SWE-Agent + Claude 4 Sonnet
acerta a funcionalidade em 57% dos casos, mas só 11,8% das soluções são seguras. Já traz
estratégias como `feedback-driven` e `sec-test`, que são baselines naturais para o plugin.
Exige ~300 GB de disco e máquina x86_64.
[paper](https://arxiv.org/abs/2512.03262) · [código](https://github.com/LeiLiLab/susvibes)

**SecRepoBench** — 318 tarefas de completação em 27 repositórios C/C++, cobrindo 15 CWEs.
[código](https://github.com/ai-sec-lab/SecRepoBench)

**CASTLE** — 250 microbenchmarks em C escritos à mão, 25 CWEs, rótulo de linha e CWE.
Útil para comparar com 25 ferramentas já publicadas. Análise completa, incluindo o
problema do score, em [castle.md](castle.md).

**FormAI / FormAI-v2** — C gerado por LLM (265 mil programas na v2, 42 CWEs), mas o rótulo
vem do ESBMC. Avaliar ESBMC ou ferramentas derivadas nele é circular, e os limites do
*model checking* geram falsos negativos no próprio rótulo.

**CyberSecEval** — o rótulo vem do *Insecure Code Detector* (estático), a mesma base do
CodeShield. Avaliar o CodeShield nele é circular.

**Juliet** — é o dataset previsto no plano atual da branch (`README.md`, Passo 3). É
sintético, com pares good/bad bem definidos, mas é antigo e quase certamente está nos dados
de treino dos modelos. Serve no máximo como sanidade, não como avaliação principal.

**AutoPenBench** — 33 tarefas (22 *in-vitro*: controle de acesso, web, rede, criptografia;
11 CVEs reais como Log4Shell, Heartbleed e Spring4Shell). O agente recebe uma estação Kali
e precisa invadir máquinas vulneráveis em Docker até capturar uma flag, com *milestones*
de progresso. É um benchmark de **pentest ofensivo *black-box***: não há código-fonte para
o agente analisar, não há código gerado por LLM e não mede detecção. **Não serve** para o
nosso requisito. Revisado por pares (EMNLP 2025 Industry Track), MIT.
[paper](https://aclanthology.org/2025.emnlp-industry.114/) · [código](https://github.com/lucagioacchini/auto-pen-bench)

**CyberGym / ExploitGym** — medem reprodução de vulnerabilidades e geração de *exploits*
por agentes. São relevantes como contexto de capacidade ofensiva, não como avaliação de
detector.

## 3. Composição proposta

Nenhum benchmark cobre R1–R8 sozinho. A proposta é avaliar em três níveis.

### Nível 1 — Detector em código gerado por LLM (principal)

1. Gerar código com *K* LLMs geradoras nas tarefas do CWEval, BaxBench e SeCodePLT
   (*secure coding*).
2. Rotular cada amostra pelo oráculo do próprio benchmark (testes e *exploits*). O rótulo
   não depende de nenhuma ferramenta avaliada (R2).
3. Rodar todos os detectores sobre as amostras rotuladas.

O conjunto resultante ("código gerado por LLM com rótulo por *outcome*") é em si uma
contribuição do artigo.

### Nível 2 — Plugin no loop de geração

Gerador + fiscal em loop (gerar → fiscalizar → corrigir → re-verificar) nas tarefas do
CWEval, BaxBench e SusVibes, comparando com o gerador sozinho e com as estratégias já
embutidas no SusVibes.

### Nível 3 — Calibração em código humano

CASTLE (comparável às 25 ferramentas publicadas), SeCodePLT *vulnerability detection* e
PrimeVul (pares vulnerável/corrigido).

## 4. Protocolo e métricas

### Duas trilhas de detectores

| Trilha | Quem | Métricas |
|---|---|---|
| **A — localizadores** | SAST, verificação formal, LLMs, agentes, LLMxCPG… (reportam CWE + linha) | P, R, F1, MCC, FPR, acerto de CWE, acerto de linha; CASTLE Score no Nível 3 |
| **B — classificadores binários** | VulLLM, SecureFalcon, Devign, ReVeal… (rótulo por função) | P, R, F1, MCC, FPR; *pairwise accuracy* (PrimeVul) nos pares |

Não forçar classificadores binários no CASTLE Score: ele exige linha ou CWE para contar TP.

### Métricas do Nível 2

- `func-sec@1` com e sem o fiscal (ganho de segurança).
- `func@1` com e sem o fiscal (regressão funcional causada pelas correções).
- Número de iterações até convergir e custo adicional (tokens, US$, latência p50/p95).

### Custos

Registrar tokens, custo e latência por amostra em todas as trilhas: para um plugin, isso é
tão decisivo quanto a acurácia. A infra da branch (`src/cost.py`, `src/cache.py`) já cobre
esse registro.

## 5. Ameaças à validade

- **Contaminação**: registrar a data de publicação de cada benchmark e o *cutoff* de cada
  modelo. O CASTLE é público desde mar/2025.
- **Oráculo incompleto**: "seguro" significa "nenhum *exploit*/teste conhecido falhou". É um
  limite inferior de insegurança e deve ser declarado como tal.
- **Circularidade**: FormAI (ESBMC), CyberSecEval (ICD) e *Asleep at the Keyboard* (CodeQL)
  só com ressalva explícita.
- **Viés de auto-preferência**: usar fiscais de famílias diferentes das geradoras, ou
  reportar a matriz gerador × fiscal.
- **Não determinismo**: repetir execuções e reportar variância (o CASTLE observou desvio
  < 3%).
- **Ataques ao fiscal**: o gerador pode inserir comentários enganosos no código (Flashboom,
  IEEE S&P 2025). Incluir um cenário adversarial.
- **Classificadores de segurança dos modelos**: um fiscal baseado em modelo de fronteira
  pode ter a análise bloqueada ou redirecionada por salvaguardas *cyber*. Isso é um modo de
  falha do plugin; registrar o estado `normal/fallback/flagged/error` que `src/client.py` já
  classifica.
