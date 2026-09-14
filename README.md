# safety-orchestrator

> ⚠️ **Rascunho.** Este README é um esqueleto inicial e será reescrito conforme o projeto tomar forma.

Orquestrador de camadas de segurança para aplicações baseadas em LLMs — coordena validações,
políticas e guardrails antes e depois de cada interação com o modelo.

## Status

Em fase inicial. Ainda não há API pública estável; espere mudanças sem aviso.

## Requisitos

- Python 3.11+ *(a confirmar)*

## Instalação

```bash
git clone https://github.com/Joao-IA/safety-orchestrator.git
cd safety-orchestrator

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Uso

```bash
# a definir
```

## Configuração

Copie `.env.example` para `.env` e preencha as variáveis necessárias.
Nenhum segredo deve ser commitado — veja o `.gitignore`.

## Estrutura do projeto

```
safety-orchestrator/
├── src/            # código da aplicação
├── tests/          # testes automatizados
└── docs/           # documentação
```

## Testes

```bash
pytest
```

## Roadmap

- [ ] Definir o escopo das políticas de segurança
- [ ] Desenhar a interface do orquestrador
- [ ] Implementar os primeiros guardrails
- [ ] Cobertura de testes
- [ ] Documentação de uso

## Licença

Distribuído sob a [Licença Apache 2.0](LICENSE).
