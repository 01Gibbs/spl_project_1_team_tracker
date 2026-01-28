"""Task Entity related DTOs"""

from dataclasses import dataclass
from typing import Optional

from domain.value_objects.task_priority import TaskPriority
from domain.entities.task import Task


@dataclass
class CreateTaskDto:
  title: str
  description: str
  priority: Optional[TaskPriority] = TaskPriority.UNASSIGNED


@dataclass
class TaskResponseDto:
  task_id: str
  status: str
  title: str
  description: str
  priority: str
  assignee: Optional[str]

@classmethod
def from_domain(cls, task: Task) -> "TaskResponseDto":
    return cls(
        task_id=task.id.value,
        status=task.status.value,
        priority=task.priority.value,
        title=task.title,
        description=task.description,
        assignee=task.assignee_id
    )