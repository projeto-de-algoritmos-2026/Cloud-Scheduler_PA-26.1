import copy
import random
from typing import List, Tuple
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


# calcula as métricas depois de simular
def get_stats(tasks, name):
    late = [t for t in tasks if t.is_late]
    return {
        "algorithm":     name,
        "total_tasks":   len(tasks),
        "late_count":    len(late),
        "on_time_count": len(tasks) - len(late),
        "late_pct":      round(100 * len(late) / len(tasks), 1),
        "max_lateness":  round(max(t.lateness for t in tasks), 2),
        "avg_lateness":  round(sum(t.lateness for t in tasks) / len(tasks), 2),
        "total_penalty": round(sum(t.total_penalty for t in tasks), 2),
        "makespan":      round(tasks[-1].finish_time, 2),
    }


# EDF - ordena pelo deadline mais cedo primeiro
# é um algoritmo guloso e é ótimo para minimizar o atraso máximo
def schedule_edf(tasks):
    ordered = sorted(tasks, key=lambda t: t.deadline)
    result = simulate(ordered)
    return result, get_stats(result, "EDF")


# FIFO - processa na ordem que chegou, sem nenhuma inteligência
def schedule_fifo(tasks):
    ordered = sorted(tasks, key=lambda t: t.task_id)
    result = simulate(ordered)
    return result, get_stats(result, "FIFO")


# Random - ordem aleatória, serve só pra comparar com o EDF
def schedule_random(tasks, seed=7):
    shuffled = copy.deepcopy(tasks)
    random.Random(seed).shuffle(shuffled)
    result = simulate(shuffled)
    return result, get_stats(result, "Random")