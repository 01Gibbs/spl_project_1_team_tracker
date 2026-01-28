# Team Task Tracker

A **deliberate learning project** focused on career development toward senior/tech-lead level engineering.

## 🎯 Learning Objectives

- Master hexagonal architecture fundamentals
- Develop engineering judgment and system design skills
- Practice explaining technical decisions clearly
- Build confidence in architectural discussions
- Build towards mastery of Python + TypeScript

**The finished application matters less than how and why it is built.**

## 🏗️ Project Structure

```
backend/          # Python backend with hexagonal architecture
  src/
    domain/       # Pure business logic (no framework imports)
    application/  # Use cases and orchestration
    adapters/     # Framework implementations
frontend/         # TypeScript/NextJS frontend
shared/           # Shared contracts and types
scripts/          # Development and enforcement tools
```

## 🚀 Getting Started

### Backend (Python)

```bash
cd backend
uv sync           # Install dependencies
uv run main.py    # Start development server
```

### Frontend (TypeScript)

```bash
cd frontend
# Setup coming soon
```

### Development Tools

```bash
# Check architectural boundaries
python scripts/check_boundaries.py

# Run all tests
cd backend && uv run pytest
```

## 📚 Architecture

This project follows **Hexagonal Architecture** with strict boundary enforcement:

- **Domain**: Pure business logic, no external dependencies
- **Application**: Use cases, orchestrates domain objects
- **Adapters**: Framework-specific code (FastAPI, SQLAlchemy, etc.)

See [docs/architectural-boundaries.md](docs/architectural-boundaries.md) for detailed patterns.

## 🤖 AI Assistant Guidance

This project includes specialized AI instruction files:

- [.github/.copilot-instructions.md](.github/.copilot-instructions.md) - Core AI behavior
- [.github/agent-roles.md](.github/agent-roles.md) - 5 specialized AI personas
- [.github/architectural-guidelines.md](.github/architectural-guidelines.md) - Technical constraints

## 🎓 Learning Philosophy

- **Clarity over cleverness** - Explicit domain models over magic
- **Explicitness over magic** - Clear dependency injection over hidden complexity
- **Maintainability over speed** - Well-structured code over premature optimization

**Success Criteria**: Can explain every major decision and defend architectural choices confidently.
