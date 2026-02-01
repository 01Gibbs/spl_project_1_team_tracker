""" Module for creating tasks use case."""

from domain.entities.task import Task, TaskId
from domain.value_objects.task_priority import TaskPriority
from domain.value_objects.task_status import TaskStatus
from domain.ports.task_repository import TaskRepository
from application.dtos.task import CreateTaskDto, TaskResponseDto

class CreateTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, dto: CreateTaskDto) -> TaskResponseDto:
        """Create a new task based on the provided input data."""
        priority = dto.priority
        if isinstance(priority, str):
            priority = TaskPriority[priority.upper()]

        # If priority is None or invalid, default to UNASSIGNED
        if not priority:
            priority = TaskPriority.UNASSIGNED

        new_task = Task(
            id=TaskId.generate(),
            title=dto.title,
            description=dto.description,
            status=TaskStatus.NOT_STARTED,
            priority=priority
        )
        self.task_repository.save(new_task)
        return TaskResponseDto.from_domain(new_task)