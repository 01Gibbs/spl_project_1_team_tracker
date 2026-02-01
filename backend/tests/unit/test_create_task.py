from adapters.persistence.in_memory_task_repository import InMemoryTaskRepository
from application.use_cases.task.create_task import CreateTaskUseCase
from application.dtos.task import CreateTaskDto
from domain.entities.task import TaskId

def test_create_and_fetch_task():
    repo = InMemoryTaskRepository()
    use_case = CreateTaskUseCase(repo)
    dto = CreateTaskDto(title="Test Task", description="Try hexagonal!", priority=None)
    response = use_case.execute(dto)
    task = repo.find_by_id(TaskId(response.task_id))
    assert task is not None
    assert task.title == "Test Task"
    assert task.description == "Try hexagonal!"