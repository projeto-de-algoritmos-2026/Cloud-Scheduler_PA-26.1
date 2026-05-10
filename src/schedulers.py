import copy
import random
from src.task import Task


# roda a simulação na ordem que receber e preenche os tempos
def simulate(tasks):
    result = copy.deepcopy(tasks)
    clock = 0.0
    for t in result:
        t.start_time = clock
        t.finish_time = clock + t.duration
        clock = t.finish_time
    return result


def get_stats(tasks, name):
    if not tasks:
        return {
            "algorithm":     name,
            "total_tasks":   0,
            "late_count":    0,
            "on_time_count": 0,
            "late_pct":      0.0,
            "max_lateness":  0.0,
            "avg_lateness":  0.0,
            "total_penalty": 0.0,
            "makespan":      0.0,
        }

    late = [t for t in tasks if t.is_late]
    avg_late = (sum(t.lateness for t in late) / len(late)) if late else 0.0
    return {
        "algorithm":     name,
        "total_tasks":   len(tasks),
        "late_count":    len(late),
        "on_time_count": len(tasks) - len(late),
        "late_pct":      round(100 * len(late) / len(tasks), 1),
        "max_lateness":  round(max(t.lateness for t in tasks), 2),
        "avg_lateness":  round(avg_late, 2),
        "total_penalty": round(sum(t.total_penalty for t in tasks), 2),
        "makespan":      round(tasks[-1].finish_time, 2),
    }


# edf ordena pelo deadline mais cedo primeiro
def schedule_edf(tasks):
    ordered = sorted(tasks, key=lambda t: t.deadline)
    result = simulate(ordered)
    return result, get_stats(result, "EDF")


# fila processa na ordem que chegou, sem nenhuma inteligência
def schedule_fifo(tasks):
    ordered = sorted(tasks, key=lambda t: t.task_id)
    result = simulate(ordered)
    return result, get_stats(result, "FIFO")


# random ordem aleatória, serve só pra comparar com o EDF
def schedule_random(tasks, seed=7):
    shuffled = copy.deepcopy(tasks)
    random.Random(seed).shuffle(shuffled)
    result = simulate(shuffled)
    return result, get_stats(result, "Random")