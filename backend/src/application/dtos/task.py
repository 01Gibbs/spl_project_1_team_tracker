"""Task Entity DTOs module."""

from dataclasses import dataclass
from typing import Optional

from domain.value_objects.task_priority import TaskPriority
from domain.entities.task import Task

@dataclass
class CreateTaskDTO:
    """Data Transfer Object for creating a Task."""
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.UNASSIGNED

@dataclass
class TaskResponseDto:
    task_id: str
    status: str
    title: str
    description: str
    priority: str
    assignee_id: Optional[str]

@classmethod
def from_domain(cls, task: Task) -> "TaskResponseDto":
    """Create a TaskResponseDto from a Task domain entity."""
    return cls(
        task_id=task.id.value,
        status=task.status.value,
        priority=task.priority.value,
        title=task.title,
        description=task.description,
        assignee_id=task.assignee_id
    )