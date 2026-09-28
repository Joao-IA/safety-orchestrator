# Trabalhos relacionados

Levantamento de 2026-09-28. "Venue" só aparece quando confirmado por DOI ou anais; o resto
está marcado como **preprint**.

## 1. Detectores para avaliar

| Método | Venue | Abordagem | Encaixe | Links |
|---|---|---|---|---|
| **LLMxCPG** | USENIX Security 2025 | Code Property Graph (Joern) gera *slices*, a LLM classifica; C/C++ | Trilha A, código público | [paper](https://www.usenix.org/conference/usenixsecurity25/presentation/lekssays) · [código](https://github.com/qcri/llmxcpg) |
| **Vul-RAG** | ACM TOSEM | RAG com conhecimento extraído de CVEs (kernel Linux, C) | Trilha A, código público | [paper](https://dl.acm.org/doi/10.1145/3797277) · [código](https://github.com/KnowledgeRAG4LLMVulD/KnowledgeRAG4LLMVulD) |
| **SecureFalcon** | IEEE TSE 2025 | Classificador de 121M parâmetros derivado do Falcon, treinado no FormAI (C gerado por LLM). Mesmo grupo do CASTLE | Trilha B; pesos a confirmar | [paper](https://ieeexplore.ieee.org/document/10910240/) |
| **VulLLM** | ACL Findings 2024 | *Fine-tuning* multitarefa (detecção + localização + interpretação); pesos no Zenodo | Trilha B | [paper](https://aclanthology.org/2024.findings-acl.625/) · [código](https://github.com/CGCL-codes/VulLLM) |
| **IRIS** | ICLR 2025 | LLM infere especificações de *taint* para o CodeQL | Só Java (CWE-Bench-Java); precisa porte | [paper](https://arxiv.org/abs/2405.17238) |
| **VulTrial** | ICSE 2026 | Multiagente em formato de tribunal (acusação, defesa, juiz, júri) | Trilha A | [paper](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/214/Let-the-Trial-Begin-A-Mock-Court-Approach-to-Vulnerability-Detection-using-LLM-Based) |
| **LLift** | OOPSLA 2024 | LLM + análise estática no kernel Linux | Escopo estreito (uso de variável não inicializada) | — |
| **LLMDFA** | NeurIPS 2024 | Análise de fluxo de dados guiada por LLM | Verificar suporte a C | — |
| **LineVul** | MSR 2022 | CodeBERT com localização por linha | Trilha A (linha) | — |
| **DeepDFA** | ICSE 2024 | Deep learning inspirado em análise de fluxo de dados | Trilha B | — |
| **ReVeal** | IEEE TSE 2022 | GNN + reamostragem | Trilha B (baseline clássico) | — |
| **Devign** | NeurIPS 2019 | GNN | Trilha B (baseline clássico) | — |
| **VulDeePecker** | NDSS 2018 | BLSTM sobre *code gadgets* | Trilha B (baseline clássico) | — |

Somam-se a essas as ferramentas que o CASTLE já avaliou (SAST, ESBMC, CBMC) e as LLMs de
fronteira atuais como baselines genéricas. As LLMs do CASTLE são do início de 2025.

## 2. Plugin / fiscal no loop

Trabalhos mais próximos da nossa proposta; os revisores vão pedir essa comparação.

| Trabalho | Venue | Relação com a proposta |
|---|---|---|
| **CodeShield / LlamaFirewall** (Meta) | preprint (indústria) | É o produto mais próximo da ideia: análise estática *online* do código gerado. O detector reporta P = 96% e R = 79% em código de LLM. Entra como baseline. [paper](https://arxiv.org/abs/2505.03574) |
| **INDICT** | NeurIPS 2024 | Críticos de segurança e de utilidade dentro do loop de geração. [paper](https://proceedings.neurips.cc/paper_files/paper/2024/hash/9b812ee4b831c21e14156ced8659197c-Abstract-Conference.html) |
| **Sifting the Noise** | ISSTA 2026 | Agentes LLM filtrando falsos positivos de SAST, a arquitetura híbrida mais provável para nós. [paper](https://arxiv.org/abs/2601.22952) |
| **Friends or Foes?** | ITEQS @ ICST 2026 (workshop) | Combinação de SAST e LLMs para detecção. |
| **Closing the Gap** | ICSE 2025 | Estudo com usuários sobre detecção e correção por IA dentro da IDE, útil para a discussão de usabilidade. [paper](https://arxiv.org/abs/2412.14306) |

### Abordagem oposta: "seguro por treinamento"

O próprio gerador aprende a não produzir código inseguro. Serve de contraste com o fiscal
externo.

| Trabalho | Venue |
|---|---|
| **PurpCode** | NeurIPS 2025 ([paper](https://arxiv.org/abs/2507.19060)) |
| **SafeCoder** | ICML 2024 |
| **SVEN** | ACM CCS 2023 |

## 3. Avaliações da capacidade de LLMs como detectores

| Trabalho | Venue | Por que importa |
|---|---|---|
| **SecLLMHolmes** | IEEE S&P 2024 | Trocar nomes de variáveis muda a resposta em 17–26% dos casos: falta robustez. [paper](https://ieeexplore.ieee.org/document/10646663/) |
| **SV-TrustEval-C** | IEEE S&P 2025 | Raciocínio estrutural e semântico em C. [código](https://github.com/Jackline97/SV-TrustEval-C) |
| **From Large to Mammoth** | NDSS 2025 | Comparação ampla de LLMs em detecção. |
| **PrimeVul** | ICSE 2025 | Dataset com pares e protocolo que mostram quanto os resultados anteriores estavam inflados. [código](https://github.com/DLVulDet/PrimeVul) |
| **JitVul** | ACL 2025 | LLMs e agentes em detecção no nível do repositório. [código](https://github.com/alperen21/JitVul) |
| **LLM-based Vulnerability Discovery through the Lens of Code Metrics** | ICSE 2026 | Análise do que as LLMs realmente aprendem. |
| **Asleep at the Keyboard** | IEEE S&P 2022 | Metodologia clássica: Copilot + cenários CodeQL. |

## 4. Ameaças ao fiscal

- **Flashboom** (IEEE S&P 2025): cega auditores de código baseados em LLM. Um gerador pode
  inserir comentários enganosos, então isso entra no modelo de ameaça.
- **ALIBI** (preprint, 2026): ataques adaptativos via comentários adversariais.
  [paper](https://arxiv.org/abs/2607.24964)

## 5. Preprints relevantes (sem venue confirmado)

Checar o status antes da submissão; alguns podem ter sido aceitos depois deste levantamento.

| Trabalho | Observação |
|---|---|
| **VulnLLM-R** | Modelo de raciocínio de 7B especializado, pesos no HF. [paper](https://arxiv.org/abs/2512.07533) |
| **R2Vul** | RLAIF + destilação de raciocínio; multilíngue. [paper](https://arxiv.org/abs/2504.04699) · [código](https://github.com/martin-wey/R2Vul) |
| **VULPO**, **VulInstruct** | *Fine-tuning* com contexto e especificações de segurança. |
| **MSIVD** | *Fine-tuning* multitarefa auto-instruído. |
| **ESBMC-AI** | ESBMC + LLM para detectar e corrigir C (mesmo grupo do CASTLE). [paper](https://arxiv.org/abs/2305.14752) |
| **CyberSecEval 1–3** | Benchmarks da Meta; base do CodeShield. |

## 6. Sobre o que já estava anotado

- **Sakana AI — Fugu-Cyber**: orquestrador multiagente comercial. Reporta 86,9% no CyberGym,
  mas foi divulgado só em [post de blog](https://sakana.ai/fugu-cyber-release/), sem paper.
- **ExploitGym**: [preprint](https://arxiv.org/abs/2605.11086) (mai/2026) de UC Berkeley,
  MPI-SP e outros. É benchmark de **geração de *exploits*** (898 instâncias: userspace, V8 e
  kernel Linux), não de detecção.

Os dois servem como contexto do estado da arte ofensivo, não como detectores revisados por
pares.

## Índices úteis

- [Awesome-LLMs-for-Vulnerability-Detection](https://github.com/huhusmang/Awesome-LLMs-for-Vulnerability-Detection):
  lista mantida com venues; a marcação de venue pode estar desatualizada.
