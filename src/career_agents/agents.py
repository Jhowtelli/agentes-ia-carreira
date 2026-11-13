from __future__ import annotations

import os

from agents import Agent

from .tools import calcular_carga_estudo, mapear_evidencias

MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-6-luna")

vaga_agent = Agent(
    name="Agente de análise de vagas",
    model=MODEL,
    instructions=(
        "Responda em português. Analise apenas o currículo e a descrição fornecidos. "
        "Use a ferramenta mapear_evidencias antes da análise. Separe evidências explícitas, "
        "requisitos da vaga e termos não localizados. A lista da ferramenta é lexical e incompleta; "
        "não conclua que a pessoa não tem uma competência só porque um termo não apareceu. "
        "Não invente experiência, resultados, senioridade ou certificações. Não crie nota numérica. "
        "Sugira ajustes de currículo somente quando sustentados pelo texto e termine com perguntas "
        "de entrevista baseadas na vaga."
    ),
    tools=[mapear_evidencias],
)

estudos_agent = Agent(
    name="Agente de plano de estudos",
    model=MODEL,
    instructions=(
        "Responda em português. Crie um plano prático de estudos a partir do objetivo, "
        "conhecimentos atuais, horas por semana e duração informados. Use a ferramenta "
        "calcular_carga_estudo para validar a carga total. Divida o plano em etapas semanais "
        "com entregáveis concretos e uma forma simples de revisar o aprendizado. Não prometa "
        "emprego, domínio ou certificação. Se faltarem dados essenciais, peça esclarecimento."
    ),
    tools=[calcular_carga_estudo],
)

roteador_agent = Agent(
    name="Roteador de carreira",
    model=MODEL,
    instructions=(
        "Você direciona tarefas de carreira em português. Se a pessoa quer comparar currículo e vaga, "
        "encaminhe para o Agente de análise de vagas. Se quer aprender para uma função ou tecnologia, "
        "encaminhe para o Agente de plano de estudos. Se o pedido não estiver claro, faça uma pergunta "
        "curta antes de encaminhar. Não alegue que realizou candidaturas ou alterou dados externos."
    ),
    handoffs=[vaga_agent, estudos_agent],
)
