"""Task Entity related DTOs"""

from dataclasses import dataclass
from typing import Optional

from domain.entities.task import Task
from domain.value_objects.task_priority import TaskPriority


@dataclass
class CreateTaskDto:
  title: str
  description: Optional[str] = None
  priority: Optional[TaskPriority] = TaskPriority.UNASSIGNED


@dataclass
class TaskResponseDto:
    task_id: str
    status: str
    title: str
    description: Optional[str]
    priority: str
    assignee_id: Optional[str]

    @classmethod
    def from_domain(cls, task: Task) -> "TaskResponseDto":
        return cls(
            task_id=task.id.value,
            status=task.status.value,
            priority=task.priority.value,
            title=task.title,
            description=task.description,
            assignee_id=task.assignee_id
        )