import argparse
import time
from src.generator import generate_tasks
from src.schedulers import schedule_edf, schedule_fifo, schedule_random

G = "\033[92m"
B = "\033[94m"
W = "\033[1m"
R = "\033[0m"


def print_table(stats_list):
    print(f"\n{W}{'─'*70}{R}")
    print(f"{W}  {'Algoritmo':<10} {'Atrasadas':>10} {'% Atras.':>9} {'Atraso Máx':>12} {'Multa Total':>16}{R}")
    print(f"{W}{'─'*70}{R}")

    menor_multa = min(s["total_penalty"] for s in stats_list)

    for s in stats_list:
        melhor = s["total_penalty"] == menor_multa
        cor = G if melhor else R
        tag = f" {G}<-- melhor{R}" if melhor else ""
        print(
            f"  {cor}{s['algorithm']:<10}{R}"
            f"  {s['late_count']:>8}"
            f"  {s['late_pct']:>8.1f}%"
            f"  {s['max_lateness']:>11.1f}s"
            f"  R$ {s['total_penalty']:>12,.2f}"
            f"{tag}"
        )

    print(f"{W}{'─'*70}{R}")

    edf_multa = next(s["total_penalty"] for s in stats_list if s["algorithm"] == "EDF")
    rand_multa = next(s["total_penalty"] for s in stats_list if s["algorithm"] == "Random")
    economia = rand_multa - edf_multa
    pct = 100 * economia / rand_multa

    print(f"\n{G}  EDF economizou R$ {economia:,.2f} comparado ao Random ({pct:.1f}% a menos){R}\n")


def analise_escalabilidade():
    tamanhos = [25, 50, 100, 250, 500, 1000]
    resultados = []

    for n in tamanhos:
        tasks = generate_tasks(n=n, seed=42)
        _, se = schedule_edf(tasks)
        _, sf = schedule_fifo(tasks)
        _, sr = schedule_random(tasks)

        resultados.append({
            "n": n,
            "EDF": se["total_penalty"],
            "FIFO": sf["total_penalty"],
            "Random": sr["total_penalty"]
        })

        print(f"    n={n:>5}:  EDF=R${se['total_penalty']:>12,.0f}  "
              f"FIFO=R${sf['total_penalty']:>12,.0f}  "
              f"Random=R${sr['total_penalty']:>12,.0f}")

    return resultados


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.tasks < 1:
        parser.error("--tasks deve ser >= 1")

    print(f"\n{W}Escalonamento de Tarefas — EDF{R}")
    print(f"  {args.tasks} tarefas | seed={args.seed}\n")

    tasks = generate_tasks(n=args.tasks, seed=args.seed)

    inicio = time.perf_counter()
    tasks_edf, s_edf = schedule_edf(tasks)
    tasks_fifo, s_fifo = schedule_fifo(tasks)
    tasks_random, s_random = schedule_random(tasks)
    fim = time.perf_counter()

    print(f"  tempo de execução: {(fim - inicio)*1000:.1f} ms\n")

    print_table([s_edf, s_fifo, s_random])

    print(f"\n{B}analise de escalabilidade:{R}")
    analise_escalabilidade()


if __name__ == "__main__":
    main()