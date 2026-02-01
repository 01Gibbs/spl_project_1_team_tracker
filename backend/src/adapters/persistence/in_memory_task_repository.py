from domain.entities.task import Task, TaskId
from typing import Optional

class InMemoryTaskRepository:
    def __init__(self):
        self.tasks = {}

    def save(self, task: Task) -> None:
        self.tasks[task.id.value] = task

    def find_by_id(self, task_id: TaskId) -> Optional[Task]:
        return self.tasks.get(task_id.value)