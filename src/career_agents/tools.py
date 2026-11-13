from __future__ import annotations

import json
import re
import unicodedata

from agents.decorators import tool

SKILL_TERMS: dict[str, tuple[str, ...]] = {
    "Python": ("python",),
    "TypeScript": ("typescript",),
    "JavaScript": ("javascript",),
    "Next.js": ("next.js", "nextjs"),
    "SQL": ("sql",),
    "PostgreSQL": ("postgresql", "postgres"),
    "API REST": ("api rest", "rest api"),
    "Active Directory": ("active directory",),
    "Linux": ("linux",),
    "Redes": ("redes de computadores", "redes", "networking"),
    "Docker": ("docker",),
    "AWS": ("aws", "amazon web services"),
    "Azure": ("azure",),
    "Supabase": ("supabase",),
    "Stripe": ("stripe",),
    "Git e GitHub": ("github", "git"),
    "Zebra": ("zebra",),
    "Honeywell": ("honeywell",),
    "ICQA": ("icqa",),
    "NFC": ("nfc",),
    "Bluetooth": ("bluetooth",),
    "OpenAI Agents SDK": ("openai agents sdk", "agents sdk"),
    "Agentes de IA": ("agente de ia", "agentes de ia", "inteligencia artificial"),
}


def normalizar(texto: str) -> str:
    decomposed = unicodedata.normalize("NFD", texto.casefold())
    return "".join(char for char in decomposed if unicodedata.category(char) != "Mn")


def contem_termo(texto: str, termo: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(termo)}(?!\w)", texto) is not None


@tool
def mapear_evidencias(curriculo: str, vaga: str) -> str:
    """Localiza termos técnicos explícitos no currículo e na descrição da vaga."""
    resume = normalizar(curriculo)
    job = normalizar(vaga)

    no_resume: list[str] = []
    in_job: list[str] = []
    for skill, aliases in SKILL_TERMS.items():
        if any(contem_termo(resume, normalizar(alias)) for alias in aliases):
            no_resume.append(skill)
        if any(contem_termo(job, normalizar(alias)) for alias in aliases):
            in_job.append(skill)

    resume_set = set(no_resume)
    result = {
        "evidencias_lexicais_compartilhadas": [skill for skill in in_job if skill in resume_set],
        "termos_da_vaga_nao_encontrados_no_curriculo": [skill for skill in in_job if skill not in resume_set],
        "limite": "A lista é inicial e lexical. Ausência de termo não comprova ausência de competência.",
    }
    return json.dumps(result, ensure_ascii=False)


@tool
def calcular_carga_estudo(horas_por_semana: int, semanas: int) -> str:
    """Calcula a carga total disponível para um plano de estudos."""
    if not 1 <= horas_por_semana <= 40:
        return "Informe de 1 a 40 horas por semana."
    if not 1 <= semanas <= 52:
        return "Informe um período de 1 a 52 semanas."

    horas_totais = horas_por_semana * semanas
    result = {
        "horas_por_semana": horas_por_semana,
        "semanas": semanas,
        "horas_totais": horas_totais,
        "blocos_semanais_sugeridos": min(4, horas_por_semana),
        "observacao": "A distribuição é uma referência; adapte os dias à sua rotina.",
    }
    return json.dumps(result, ensure_ascii=False)
