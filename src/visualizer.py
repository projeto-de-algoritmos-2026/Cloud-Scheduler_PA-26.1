import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

COLORS = {"EDF": "#00C896", "FIFO": "#E8445A", "Random": "#F5A623"}
OUT = "reports"


def salvar(fig, nome):
    os.makedirs(OUT, exist_ok=True)
    caminho = os.path.join(OUT, nome)
    fig.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  salvo: {caminho}")


def plot_penalty_bar(stats_list):
    algos = [s["algorithm"] for s in stats_list]
    valores = [s["total_penalty"] for s in stats_list]
    cores = [COLORS[a] for a in algos]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#0F1117")

    barras = ax.bar(algos, valores, color=cores, width=0.5, edgecolor="none")
    for b, v in zip(barras, valores):
        ax.text(b.get_x() + b.get_width() / 2,
                b.get_height() + max(valores) * 0.02,
                f"R$ {v:,.0f}", ha="center", fontsize=11,
                fontweight="bold", color="white")

    ax.set_title("Multa Total por Algoritmo", color="white", fontsize=14, pad=14)
    ax.set_ylabel("Multa Total (R$)", color="#AAAAAA", fontsize=11)
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
    ax.set_ylim(0, max(valores) * 1.2)
    ax.grid(axis="y", color="#222", linewidth=0.8)
    salvar(fig, "01_multa_total.png")


def plot_late_tasks(stats_list):
    algos = [s["algorithm"] for s in stats_list]
    atrasadas = [s["late_count"] for s in stats_list]
    no_prazo = [s["on_time_count"] for s in stats_list]
    x = np.arange(len(algos))
    w = 0.35

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#0F1117")

    b1 = ax.bar(x - w/2, atrasadas, w, label="Atrasadas",
                color=[COLORS[a] for a in algos], alpha=0.95)
    b2 = ax.bar(x + w/2, no_prazo, w, label="No Prazo",
                color=[COLORS[a] for a in algos], alpha=0.35, hatch="///")

    for b in b1:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.5,
                str(int(b.get_height())), ha="center", color="white", fontsize=10)
    for b in b2:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.5,
                str(int(b.get_height())), ha="center", color="#AAAAAA", fontsize=10)

    ax.set_title("Tarefas Atrasadas vs. No Prazo", color="white", fontsize=14, pad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(algos, color="white", fontsize=12)
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="y", color="#222", linewidth=0.8)
    ax.legend(facecolor="#1A1D27", labelcolor="white", fontsize=10)
    salvar(fig, "02_tarefas_atrasadas.png")


def plot_cumulative_penalty(results):
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#0F1117")

    for algo, tasks in results.items():
        ordenadas = sorted(tasks, key=lambda t: t.finish_time)
        tempos, acumulado, total = [], [], 0.0
        for t in ordenadas:
            total += t.total_penalty
            tempos.append(t.finish_time)
            acumulado.append(total)
        ax.plot(tempos, acumulado, label=algo, color=COLORS[algo], linewidth=2.3)

    ax.set_title("Multa Acumulada ao Longo do Tempo", color="white", fontsize=14, pad=14)
    ax.set_xlabel("Tempo (s)", color="#AAAAAA", fontsize=11)
    ax.set_ylabel("Multa Acumulada (R$)", color="#AAAAAA", fontsize=11)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(color="#222", linewidth=0.8)
    ax.legend(facecolor="#1A1D27", labelcolor="white", fontsize=11)
    salvar(fig, "03_multa_acumulada.png")


def plot_gantt(tasks, n=25):
    subset = tasks[:n]
    fig, ax = plt.subplots(figsize=(13, max(5, n * 0.33)))
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#0F1117")

    for i, t in enumerate(subset):
        cor = "#E8445A" if t.is_late else "#00C896"
        ax.barh(i, t.duration, left=t.start_time, color=cor,
                alpha=0.85, edgecolor="none", height=0.65)
        ax.axvline(t.deadline, color="#555", linewidth=0.6, linestyle=":")
        ax.text(t.start_time + t.duration + 0.3, i,
                f"{'⚠' if t.is_late else '✓'} {t.name}",
                va="center", fontsize=7.5, color="white")

    ax.set_yticks(range(n))
    ax.set_yticklabels([t.name for t in subset], fontsize=8, color="white")
    ax.set_xlabel("Tempo (s)", color="#AAAAAA", fontsize=11)
    ax.set_title("Gantt — EDF (primeiras 25 tarefas)", color="white", fontsize=13, pad=14)
    ax.invert_yaxis()
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="x", color="#222", linewidth=0.8)

    ax.legend(handles=[
        mpatches.Patch(color="#00C896", label="No prazo"),
        mpatches.Patch(color="#E8445A", label="Atrasada"),
    ], facecolor="#1A1D27", labelcolor="white", fontsize=10)
    salvar(fig, "04_gantt_edf.png")


def plot_scalability(data):
    ns =   [d["n"]      for d in data]
    edf =  [d["EDF"]    for d in data]
    fifo = [d["FIFO"]   for d in data]
    rand = [d["Random"] for d in data]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#0F1117")

    ax.plot(ns, edf,  marker="o", label="EDF",    color=COLORS["EDF"],    linewidth=2.3)
    ax.plot(ns, fifo, marker="^", label="FIFO",   color=COLORS["FIFO"],   linewidth=2.0, linestyle="--")
    ax.plot(ns, rand, marker="D", label="Random", color=COLORS["Random"], linewidth=2.0, linestyle="--")

    ax.set_title("Escalabilidade: Multa vs. Número de Tarefas", color="white", fontsize=14, pad=14)
    ax.set_xlabel("n", color="#AAAAAA", fontsize=11)
    ax.set_ylabel("Multa Total (R$)", color="#AAAAAA", fontsize=11)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(color="#222", linewidth=0.8)
    ax.legend(facecolor="#1A1D27", labelcolor="white", fontsize=11)
    salvar(fig, "05_escalabilidade.png")