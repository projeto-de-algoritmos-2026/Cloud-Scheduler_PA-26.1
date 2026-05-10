import random
from typing import List
from src.task import Task


def generate_tasks(n=100, seed=42):
    rng = random.Random(seed)
    tasks = []

    for i in range(n):
        duration = rng.uniform(1.0, 20.0)
        # deadline tem uma folga em relação à duração
        deadline = duration * rng.uniform(1.0, 3.0) + rng.uniform(0, 10)
        penalty = rng.uniform(50.0, 500.0)

        tasks.append(Task(
            task_id=i + 1,
            name=f"Job-{i+1:04d}",
            duration=round(duration, 2),
            deadline=round(deadline, 2),
            penalty=round(penalty, 2),
        ))

    return tasks