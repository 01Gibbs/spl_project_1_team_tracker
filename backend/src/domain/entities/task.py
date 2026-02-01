"""Task entity following domain-driven design principles."""

from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from ..value_objects.task_status import TaskStatus
from ..value_objects.task_priority import TaskPriority


@dataclass
class TaskId:
    """Value object for Task identity."""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("TaskId cannot be empty")

    @classmethod 
    def generate(cls) -> "TaskId":
        """Generate a new unique TaskId."""
        return cls(str(uuid4()))

    def __str__(self) -> str:
        return self.value


@dataclass
class Task:
    """
    Task entity - represents a work item in the team tracker.
    
    Business Rules:
    - Tasks must have a title and description
    - Status transitions follow business constraints
    - Tasks can be assigned to team members
    """
    
    id: TaskId
    title: str
    status: TaskStatus
    priority: TaskPriority
    description: Optional[str] = None
    assignee_id: Optional[str] = None

    def __post_init__(self):
        """Validate task invariants."""
        if not self.title.strip():
            raise ValueError("Task title cannot be empty")
        
        if self.description is not None and not self.description.strip():
            raise ValueError("Task description cannot be empty")

    def assign_to(self, assignee_id: str) -> None:
        """Assign this task to a team member."""
        if not assignee_id:
            raise ValueError("Assignee ID cannot be empty")
        
        if self.status == TaskStatus.COMPLETED:
            raise ValueError("Cannot assign completed tasks")
        
        self.assignee_id = assignee_id

    def unassign(self) -> None:
        """Remove assignment from this task."""
        self.assignee_id = None

    def mark_in_progress(self) -> None:
        """Mark task as in progress."""
        if self.status == TaskStatus.COMPLETED:
            raise ValueError("Cannot change status of completed task")
        
        self.status = TaskStatus.IN_PROGRESS

    def mark_completed(self) -> None:
        """Mark task as completed."""
        if self.status == TaskStatus.NOT_STARTED:
            raise ValueError("Task must be in progress before completion")
        
        self.status = TaskStatus.COMPLETED

    def is_assigned(self) -> bool:
        """Check if task is assigned to someone."""
        return self.assignee_id is not None

    def can_be_deleted(self) -> bool:
        """Check if task can be safely deleted."""
        return self.status != TaskStatus.IN_PROGRESS