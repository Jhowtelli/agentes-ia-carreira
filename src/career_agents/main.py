from __future__ import annotations

import os

from agents import Runner

from .agents import roteador_agent


def read_multiline(label: str) -> str:
    print(f"\n{label}\nDigite /fim em uma linha quando terminar:")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().casefold() == "/fim":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def main() -> int:
    if not os.getenv("OPENAI_API_KEY"):
        print("Configure OPENAI_API_KEY no ambiente antes de iniciar.")
        return 2

    print("Agentes de IA para carreira")
    print("1. Analisar uma vaga a partir do currículo")
    print("2. Montar um plano de estudos")
    choice = input("Escolha 1 ou 2: ").strip()

    if choice == "1":
        resume = read_multiline("Cole o currículo ou um resumo profissional")
        job = read_multiline("Cole a descrição da vaga")
        if not resume or not job:
            print("Currículo e descrição da vaga são necessários para esta análise.")
            return 2
        prompt = (
            "Analise esta vaga com base somente nas informações fornecidas.\n\n"
            f"CURRÍCULO:\n{resume}\n\nDESCRIÇÃO DA VAGA:\n{job}"
        )
    elif choice == "2":
        goal = input("Qual função ou tecnologia você quer estudar? ").strip()
        current = input("O que você já sabe sobre o assunto? ").strip()
        hours = input("Quantas horas por semana pode estudar? ").strip()
        weeks = input("Por quantas semanas? ").strip()
        if not all((goal, hours, weeks)):
            print("Objetivo, horas por semana e duração são necessários.")
            return 2
        prompt = (
            "Monte um plano de estudos para este objetivo.\n"
            f"OBJETIVO: {goal}\nCONHECIMENTOS ATUAIS: {current or 'não informado'}\n"
            f"HORAS POR SEMANA: {hours}\nDURAÇÃO EM SEMANAS: {weeks}"
        )
    else:
        print("Escolha 1 ou 2.")
        return 2

    try:
        result = Runner.run_sync(roteador_agent, prompt)
    except Exception as exc:
        print(f"Não foi possível concluir a execução: {type(exc).__name__}.")
        return 1

    print("\nResultado\n")
    print(result.final_output)
    print(f"\nEspecialista: {result.last_agent.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
