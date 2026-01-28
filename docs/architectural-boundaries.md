# Architectural Boundaries & Data Contracts

This document defines strict architectural boundaries inspired by **Shopify's Packwerk** and **Sorting Hat** principles, adapted for Python and hexagonal architecture.

## Core Principles

### 1. **Components Must Not Know Each Other's Internals**

Each layer and component should interact through well-defined contracts only.

### 2. **Data Contracts Are Sacred**

No internal data structures should leak across boundaries.

### 3. **Dependencies Flow Inward**

Outer layers depend on inner layers, never the reverse.

---

## Strict Data Contracts 📋

### The Golden Rule: **No Shared Entities**

```python
# ❌ VIOLATION: Domain entity leaking to adapter
class TaskController:
    def create_task(self, request) -> Task:  # Domain Task exposed!
        return self.task_service.create(request)

# ✅ CORRECT: DTO contract at boundary
class TaskController:
    def create_task(self, request) -> TaskDto:  # Clean contract
        task = self.task_service.create(request)
        return TaskDto.from_domain(task)
```

### DTO Patterns

**1. Boundary DTOs** - Data crossing architectural layers:

```python
@dataclass
class CreateTaskDto:
    title: str
    description: str
    assignee_id: Optional[str] = None

    def to_domain_command(self) -> CreateTaskCommand:
        """Convert DTO to domain command"""
        return CreateTaskCommand(
            title=self.title,
            description=self.description,
            assignee_id=UserId(self.assignee_id) if self.assignee_id else None
        )

@dataclass
class TaskResponseDto:
    id: str
    title: str
    status: str
    assignee_name: Optional[str]

    @classmethod
    def from_domain(cls, task: Task, assignee: Optional[Member] = None):
        """Convert domain entity to DTO"""
        return cls(
            id=str(task.id),
            title=task.title,
            status=task.status.value,
            assignee_name=assignee.name if assignee else None
        )
```

**2. Integration DTOs** - Data crossing service boundaries:

```python
@dataclass
class NotificationDto:
    """Contract for external notification service"""
    recipient_email: str
    subject: str
    message: str
    template: str
```

---

## Packwerk-Inspired Component Isolation 📦

### Component Definition

Each major domain concept is a **component** with strict boundaries:

```
src/
  components/
    tasks/          # Task component
      domain/       # Task entities, value objects
      application/  # Task use cases
      adapters/     # Task repositories, controllers
      __init__.py   # Public interface ONLY
    teams/          # Team component
      domain/
      application/
      adapters/
      __init__.py
    members/        # Member component
      domain/
      application/
      adapters/
      __init__.py
```

### Public Interface Pattern

Each component exposes **only** what others need:

```python
# components/tasks/__init__.py
"""Public interface for Task component"""

# Public DTOs
from .application.dtos import (
    CreateTaskDto,
    TaskResponseDto,
    UpdateTaskDto,
)

# Public use cases
from .application.use_cases import (
    CreateTaskUseCase,
    AssignTaskUseCase,
    CompleteTaskUseCase,
)

# Public ports (interfaces)
from .domain.ports import (
    TaskRepository,
    TaskNotificationService,
)

# NEVER expose domain entities or internal details
```

### Cross-Component Communication Rules

```python
# ❌ VIOLATION: Direct domain entity access
from components.tasks.domain.entities import Task  # FORBIDDEN

# ✅ CORRECT: Use public interface only
from components.tasks import CreateTaskDto, CreateTaskUseCase

class TeamTaskService:
    def __init__(self, task_use_case: CreateTaskUseCase):
        self.task_use_case = task_use_case

    def create_team_task(self, team_id: str, task_data: dict) -> TaskResponseDto:
        create_dto = CreateTaskDto(**task_data)
        return self.task_use_case.execute(create_dto)
```

---

## Boundary Enforcement 🚧

### 1. Import Violations

**Domain Layer Violations:**

```python
# ❌ FORBIDDEN in domain layer
from fastapi import HTTPException      # Framework import
from sqlalchemy import Column          # Infrastructure import
from components.teams import TeamDto   # Cross-component import

# ✅ ALLOWED in domain layer
from typing import Protocol            # Standard library
from dataclasses import dataclass      # Standard library
from .value_objects import TaskStatus  # Same component
```

**Application Layer Violations:**

```python
# ❌ FORBIDDEN in application layer
from sqlalchemy.orm import Session     # Infrastructure detail
from fastapi import Request           # Web framework detail

# ✅ ALLOWED in application layer
from .domain.entities import Task     # Same component domain
from .dtos import CreateTaskDto       # Same layer DTOs
from .ports import TaskRepository     # Domain ports only
```

### 2. Detection Strategies

**Static Analysis with Custom Rules:**

```python
# scripts/check_boundaries.py
import ast
import sys
from pathlib import Path

class BoundaryChecker(ast.NodeVisitor):
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.violations = []

    def visit_ImportFrom(self, node):
        if self.is_domain_layer() and self.is_framework_import(node.module):
            self.violations.append(
                f"Domain layer importing framework: {node.module}"
            )

    def is_domain_layer(self) -> bool:
        return "domain" in self.file_path.parts

    def is_framework_import(self, module: str) -> bool:
        frameworks = ['fastapi', 'sqlalchemy', 'requests']
        return any(module.startswith(fw) for fw in frameworks)
```

**Pre-commit Hook:**

```bash
#!/bin/bash
# .git/hooks/pre-commit
echo "Checking architectural boundaries..."
python scripts/check_boundaries.py src/
if [ $? -ne 0 ]; then
    echo "❌ Boundary violations detected!"
    exit 1
fi
echo "✅ Boundary checks passed"
```

### 3. Violation Recovery Patterns

**When Domain Imports Infrastructure:**

```python
# ❌ Before: Domain entity knows about database
class Task:
    def save(self):
        db.session.add(self)
        db.session.commit()

# ✅ After: Repository pattern with port
class Task:
    def mark_completed(self):
        self.status = TaskStatus.COMPLETED
        # No persistence concerns in domain

# Domain port
class TaskRepository(Protocol):
    def save(self, task: Task) -> None: ...

# Infrastructure implementation
class SqlTaskRepository:
    def save(self, task: Task) -> None:
        db.session.add(self.to_sql_model(task))
        db.session.commit()
```

**When DTOs Are Missing:**

```python
# ❌ Before: Controller returns domain entity
def get_task(task_id: str) -> Task:
    return task_service.get_by_id(task_id)

# ✅ After: DTO boundary enforced
def get_task(task_id: str) -> TaskResponseDto:
    task = task_service.get_by_id(task_id)
    return TaskResponseDto.from_domain(task)
```

---

## Sorting Hat Principles 🎩

### 1. **Clear Component Ownership**

Every piece of code belongs to exactly one component:

```python
# Who owns task assignment logic?
# Answer: Task component (task is the primary entity)

# components/tasks/domain/services/task_assignment_service.py
class TaskAssignmentService:
    def assign_task(self, task: Task, assignee: UserId) -> Task:
        # Task assignment business rules here
        pass
```

### 2. **Minimize Cross-Component Dependencies**

```python
# ❌ Too many cross-component calls
class ProjectService:
    def create_project(self, data):
        project = self.project_repo.save(data)
        self.task_service.create_default_tasks(project.id)      # Coupling
        self.team_service.assign_default_members(project.id)   # Coupling
        self.notification_service.send_welcome(project.id)     # Coupling

# ✅ Event-driven decoupling
class ProjectService:
    def create_project(self, data):
        project = self.project_repo.save(data)
        self.event_bus.publish(ProjectCreated(project.id))     # Loose coupling
        return project

# Other components subscribe to events
class TaskEventHandler:
    def handle_project_created(self, event: ProjectCreated):
        self.task_service.create_default_tasks(event.project_id)
```

### 3. **Interface Segregation by Component**

```python
# ❌ Fat interface crossing components
class TaskServiceInterface:
    def create_task(self, dto: CreateTaskDto) -> TaskDto: ...
    def assign_to_team(self, task_id: str, team_id: str): ...      # Teams concern
    def send_notification(self, task_id: str, message: str): ...   # Notification concern

# ✅ Focused interfaces per component
class TaskServiceInterface:
    def create_task(self, dto: CreateTaskDto) -> TaskDto: ...
    def assign_task(self, task_id: str, assignee_id: str): ...

class TeamTaskServiceInterface:
    def assign_task_to_team(self, task_id: str, team_id: str): ...

class TaskNotificationServiceInterface:
    def notify_task_assigned(self, task_id: str, assignee_id: str): ...
```

---

## Practical Enforcement Checklist ✅

### During Development

- [ ] **No domain entities cross boundaries** - always use DTOs
- [ ] **Import checking** - domain can't import FastAPI/SQLAlchemy
- [ ] **Component interfaces only** - no reaching into internals
- [ ] **Explicit mapping** between DTOs and entities
- [ ] **Single responsibility** per component

### During Code Review

- [ ] Are any internal data structures leaking?
- [ ] Can this component be tested without external dependencies?
- [ ] Is the public interface minimal and focused?
- [ ] Are cross-component calls necessary or can they be events?
- [ ] Would this change break boundary enforcement?

### Refactoring Red Flags 🚨

- **"Let's just import the entity directly"** → Create proper DTO
- **"It's easier to add this to the existing interface"** → Consider component ownership
- **"We need access to internal methods"** → Rethink component boundaries
- **"The test needs to mock too many things"** → Boundary violation likely

---

## Benefits of Strict Boundaries 🏆

1. **Testability** - Each component tests in isolation
2. **Maintainability** - Changes contained to single components
3. **Team Scaling** - Teams can own components independently
4. **Refactoring Safety** - Internal changes don't break other components
5. **Mental Model** - Clear ownership and responsibility

**Remember**: These boundaries exist to make the system **easier to understand and change**, not harder. If a boundary feels wrong, question whether the component ownership is correct, not whether boundaries matter.
