"""
create_task
"""

from domain.entities.task import TaskId
from application.dtos.task import CreateTaskDto, TaskResponseDto
from domain.value_objects.task_priority import TaskPriority
from domain.value_objects.task_status import TaskStatus

def execute(self, input_data: CreateTaskDto) -> TaskResponseDto:
  task_id = TaskId.generate()
  title = input_data.title
  description = input_data.description
  priority = input_data.priority
  status = 