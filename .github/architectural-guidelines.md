# Architectural Guidelines - Technical Constraints & Patterns

## Hexagonal Architecture Constraints 🏗️

This project follows **Hexagonal Architecture** (Ports & Adapters).

### Hard Rules

**Domain Layer** (`src/domain/`):

- Pure Python only
- No FastAPI, SQLAlchemy, or framework imports
- Contains business rules and invariants only
- Example: `Task.can_be_completed()` checks dependencies

**Application/Service Layer** (`src/application/`):

- Orchestrates use cases
- Depends on domain abstractions only
- No direct I/O operations
- Example: `AssignTaskUseCase` coordinates domain entities

**Adapters** (`src/adapters/`):

- Framework-specific implementations (FastAPI, DB, CLI)
- Implement domain ports/interfaces
- No business logic
- Example: `SqlTaskRepository` implements `TaskRepository`

AI suggestions must respect these boundaries.

## Data Contract Enforcement 📋

- **No sharing of domain entities** between layers - use DTOs for all cross-boundary data
- **Explicit mapping** required between internal models and external contracts
- **Import violations** should be flagged immediately (e.g., domain importing FastAPI types)

_See [docs/architectural-boundaries.md](../docs/architectural-boundaries.md) for detailed boundary enforcement patterns._

## Testing Expectations 🧪

AI should assume:

- Tests are written alongside features
- Domain logic is unit-tested without frameworks
- Integration tests are explicit and limited
- Test names describe behavior, not implementation

When suggesting code:

- Also suggest what should be tested
- Highlight edge cases (circular dependencies, permission violations)
- Consider domain invariant violations

## Data Structures & Algorithms 🧩

For team/task management operations, AI should:

- Identify appropriate data structures (graphs for dependencies, sets for permissions)
- Explain why it fits the team/task use case
- Mention complexity implications for dependency resolution
- Consider cyclic dependency detection algorithms

## Common Architectural Patterns

### Repository Pattern

```python
# Domain port (interface)
class TaskRepository(Protocol):
    def save(self, task: Task) -> None: ...
    def find_by_id(self, task_id: TaskId) -> Optional[Task]: ...

# Infrastructure implementation
class SqlTaskRepository:
    def save(self, task: Task) -> None:
        # SQL-specific implementation
        pass
```

### Use Case Pattern

```python
@dataclass
class AssignTaskUseCase:
    task_repository: TaskRepository
    member_repository: MemberRepository

    def execute(self, command: AssignTaskCommand) -> TaskResponseDto:
        task = self.task_repository.find_by_id(command.task_id)
        member = self.member_repository.find_by_id(command.assignee_id)

        # Domain logic - not infrastructure concerns
        task.assign_to(member)

        self.task_repository.save(task)
        return TaskResponseDto.from_domain(task)
```

### DTO Mapping Pattern

```python
@dataclass
class TaskResponseDto:
    id: str
    title: str
    status: str
    assignee_name: Optional[str]

    @classmethod
    def from_domain(cls, task: Task, assignee: Optional[Member] = None):
        """Convert domain entity to DTO - explicit boundary crossing"""
        return cls(
            id=str(task.id),
            title=task.title,
            status=task.status.value,
            assignee_name=assignee.name if assignee else None
        )
```

## Import Rules & Violations

### ✅ Allowed Imports by Layer

**Domain Layer**:

```python
from typing import Protocol, Optional  # Standard library only
from dataclasses import dataclass      # Standard library
from .value_objects import TaskStatus  # Same component
```

**Application Layer**:

```python
from .domain.entities import Task      # Same component domain
from .dtos import CreateTaskDto        # Same layer DTOs
from .ports import TaskRepository      # Domain ports only
```

**Adapter Layer**:

```python
from fastapi import APIRouter          # Framework imports allowed
from sqlalchemy.orm import Session     # Infrastructure imports allowed
from ..application.use_cases import CreateTaskUseCase  # Application layer
```

### ❌ Common Violations to Flag

```python
# Domain importing framework
from fastapi import HTTPException      # VIOLATION: Framework in domain

# Application importing infrastructure
from sqlalchemy.orm import Session     # VIOLATION: Infrastructure in application

# Cross-component entity access
from components.teams.domain.entities import Team  # VIOLATION: Bypass public interface
```

## Quality Gates

### Pre-Commit Checks

- No domain layer imports of frameworks
- All DTOs have explicit `from_domain()` and `to_domain()` methods
- Repository interfaces defined in domain, implementations in adapters
- Use cases orchestrate but don't contain business logic

### Code Review Focus

- Are domain invariants protected?
- Do changes respect architectural boundaries?
- Are DTOs used for all boundary crossings?
- Can this be tested without infrastructure?
