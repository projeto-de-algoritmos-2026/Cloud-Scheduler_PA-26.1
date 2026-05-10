from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    task_id: int
    name: str
    duration: float
    deadline: float
    penalty: float = 100.0

    start_time: Optional[float] = None
    finish_time: Optional[float] = None

    @property
    def lateness(self):
        if self.finish_time is None:
            return 0.0
        return max(0.0, self.finish_time - self.deadline)

    @property
    def is_late(self):
        return self.lateness > 0

    # multa = atraso * penalidade por segundo
    @property
    def total_penalty(self):
        return self.lateness * self.penalty