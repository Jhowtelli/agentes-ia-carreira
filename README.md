# Agentes de IA para carreira

Um pequeno assistente de linha de comando que encaminha tarefas a agentes especialistas: análise de evidências entre currículo e vaga, ou planejamento de estudos com etapas semanais.

Projeto de portfólio desenvolvido com apoio de IA. O código não faz candidaturas, não altera perfis e não toma decisões pela pessoa.

## O que demonstra

- Roteamento de solicitações para agentes especialistas com handoffs.
- Ferramentas locais e determinísticas para mapear termos e calcular carga horária.
- Instruções para não inventar experiência, competências, senioridade ou certificações.
- Limites explícitos de privacidade e revisão humana.

## Arquitetura

```text
Pessoa → Roteador
            ├── Análise de vaga → mapeamento lexical de evidências
            └── Plano de estudos → cálculo da carga horária
```

## Requisitos

- Python 3.10 ou superior.
- Chave de API da OpenAI. O uso da API pode gerar cobranças conforme sua conta e o modelo configurado.

## Instalação no Windows

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
$env:OPENAI_API_KEY = "sua-chave"
python -m career_agents.main
```

No macOS ou Linux, crie e ative o ambiente virtual com os comandos padrão do Python, instale com `pip install -e .` e configure `OPENAI_API_KEY` no ambiente.

O modelo padrão é `gpt-6-luna`. Para selecionar outro modelo disponível na sua conta:

```powershell
$env:OPENAI_DEFAULT_MODEL = "nome-do-modelo"
```

## Uso

1. Selecione análise de vaga ou plano de estudos.
2. Informe o texto da vaga e do currículo, ou o objetivo e o tempo disponível.
3. Para terminar um bloco de texto, digite `/fim` em uma linha.
4. Revise as sugestões antes de alterar seu currículo ou plano.

A comparação lexical é apenas um apoio: um termo não aparecer no currículo não prova que a pessoa não tenha aquela competência.

## Privacidade

O texto informado é enviado ao provedor do modelo pela API para produzir a resposta. O programa não grava currículo, vaga ou plano em arquivos. Evite incluir dados pessoais desnecessários. Nenhum agente envia candidaturas, altera perfis ou acessa serviços externos.

A lista de tecnologias da ferramenta é inicial e pode não reconhecer sinônimos ou experiências descritas de outra forma.

## Stack

Python · OpenAI Agents SDK · ferramentas locais
