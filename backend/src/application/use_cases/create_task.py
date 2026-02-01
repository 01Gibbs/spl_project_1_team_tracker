""" Module for creating tasks use case."""

from domain.entities.task import Task, TaskId
from application.dtos.task import CreateTaskDto, TaskResponseDto
from domain.value_objects.task_priority import TaskPriority
from domain.value_objects.task_status import TaskStatus

def execute(self, input_data: CreateTaskDto) -> TaskResponseDto:
    """Create a new task based on the provided input data."""
    new_task = Task(
        id=TaskId.generate(),
        title=input_data.title,
        description=input_data.description,
        status=TaskStatus.PENDING,
        priority=input_data.priority
    )
    
    return TaskResponseDto.from_domain(new_task)