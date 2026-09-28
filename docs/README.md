# Documentação da pesquisa

> Rascunho vivo. Levantamento feito em 2026-09-28; venues verificados via DOI/anais
> nessa data. Preprints estão marcados como tal.

## Objetivo

Escrever um artigo científico sobre um **fiscal de terceiros** (*third-party checker*) que
inspeciona o código gerado por uma LLM e aponta vulnerabilidades — pensado para ser usado
como *tool*/plugin (ex.: servidor MCP) dentro do próprio fluxo da LLM.

Primeiro passo: **avaliar os detectores que já existem** (SAST, verificação formal, LLMs
genéricas, modelos especializados e sistemas híbridos) antes de propor o nosso.

## Documentos

| Arquivo | Conteúdo |
|---|---|
| [benchmarks.md](benchmarks.md) | Requisitos do benchmark, avaliação de cada candidato (CASTLE, AutoPenBench, …) e a composição proposta |
| [castle.md](castle.md) | Análise do CASTLE e a discrepância encontrada no CASTLE Score publicado |
| [trabalhos-relacionados.md](trabalhos-relacionados.md) | Detectores e plugins com artigo revisado por pares, preprints e ameaças |

## Resumo das decisões até agora

1. **O CASTLE sozinho não atende**: o código é escrito por humanos, é só C e não permite
   avaliar o plugin no loop de geração. Serve como camada de calibração e para comparar com
   as 25 ferramentas já publicadas.
2. **O AutoPenBench não atende**: avalia agentes de *pentest* atacando sistemas em rede
   (captura de flag), não análise de código.
3. **Nenhum benchmark revisado por pares cobre todos os requisitos.** A proposta é compor
   três níveis: detector em código gerado por LLM com rótulo por oráculo dinâmico
   (CWEval, BaxBench, SeCodePLT), plugin no loop (os mesmos + SusVibes) e calibração em
   código humano (CASTLE, SeCodePLT, PrimeVul). Detalhes em [benchmarks.md](benchmarks.md).
4. **Sakana Fugu-Cyber e ExploitGym** entram como contexto, não como detectores avaliados:
   o primeiro é produto (post de blog, sem paper) e o segundo é preprint de um benchmark de
   geração de *exploits*.

## Pendências

- [ ] Confirmar se os pesos do SecureFalcon são públicos.
- [ ] Checar o status de revisão dos preprints listados (VulnLLM-R, R2Vul, VULPO, …).
- [ ] Decidir as LLMs geradoras do Nível 1 (famílias diferentes das usadas como fiscal).
- [ ] Reimplementar a Eq. 2 do CASTLE e reproduzir a Tabela 3 com o notebook original.
- [ ] Considerar contatar os autores do CASTLE sobre a discrepância do bônus.
