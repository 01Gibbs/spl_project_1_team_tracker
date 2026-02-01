from typing import Protocol, Optional
from domain.entities.task import Task, TaskId

class TaskRepository(Protocol):
    def save(self, task: Task) -> None:
         ...

    def find_by_id(self, task_id: TaskId) -> Optional[Task]:
        ...
    