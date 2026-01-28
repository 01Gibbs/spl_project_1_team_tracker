# Project Purpose & Intent

_(For AI Coding Assistants and Review Agents)_

## High-Level Purpose

This project exists as a deliberate learning and architecture exercise, not just a feature-delivery application.

The goal is to build a small but well-structured system that demonstrates:

- Sound architectural thinking
- Clear separation of concerns
- Strong fundamentals in backend engineering
- The ability to reason about trade-offs, not just implement solutions

_The finished application matters less than how and why it is built._

## What This Project Is

At the surface level, this project is a Team Task Tracker:

- Create, update, and track tasks
- Organise tasks into projects or groups
- Maintain simple state (open, in progress, completed)
- Support basic workflows that resemble real production systems

However, this is not intended to be a feature-rich product.

It is intentionally scoped to remain:

- Small
- Understandable end-to-end
- Easy to reason about

This constrained scope allows focus on engineering quality, not product sprawl.

## What This Project Is Really About

This project is a vehicle for mastering fundamentals:

### ### Engineering Fundamentals

- Writing clear, idiomatic Python
- Designing code that is easy to test and reason about
- Using explicit data models instead of ad-hoc dictionaries
- Applying appropriate data structures intentionally

### Architectural Discipline

Practising hexagonal (ports & adapters) architecture

Enforcing boundaries between:

- Domain logic
- Application orchestration
- Infrastructure / frameworks

Keeping business rules independent of FastAPI, databases, or UI

### Systems Thinking

Thinking in terms of:

- Inputs, outputs, invariants
- Failure modes
- Change over time

Avoiding premature complexity while still planning for extension

## What the Developer Is Trying to Learn

The developer is explicitly not optimising for speed.

They are trying to:

- Become comfortable dropping into any Python codebase
- Understand unfamiliar systems by structure, not guesswork
- Develop confidence in architectural discussions
- Build intuition for why certain patterns exist

This project is designed to simulate:

- Reading and extending an existing system
- Making careful design decisions under constraints
- Justifying choices during code review or design discussion

## Career Intent Behind This Project

This project is part of a longer-term goal to grow into a senior / tech-lead-level engineer.

That means demonstrating:

- Ownership of system design, not just implementation
- Ability to explain decisions clearly to others
- Comfort working across layers (domain → service → infrastructure)
- Judgement about when not to add complexity

The project should therefore reflect:

- Professional standards
- Thoughtful trade-offs
- Clear reasoning that could be defended in an interview or review

## How AI Assistance Should Be Used

AI agents are expected to act as:

- A thought partner
- A reviewer
- A teacher

They should prioritise:

- Explanation over implementation
- Alternatives over single "correct" answers
- Surfacing trade-offs and edge cases

They should not:

- Solve problems end-to-end
- Collapse learning steps
- Hide complexity behind abstractions without explanation

If there is a faster or “clever” solution, it should be discussed — not silently applied.

## Definition of Success

This project is successful if:

- The developer can explain every major decision in plain language
- The architecture remains understandable without diagrams
- Business logic can be tested without infrastructure
- Features can be added without fear of breaking unrelated parts
- The code reads like it was written on purpose

_A smaller, well-explained system is preferable to a larger, poorly-reasoned one._

## Final Guiding Principle

**The primary output of this project is engineering judgement, not lines of code.**

If an AI suggestion does not strengthen understanding, clarity, or reasoning, it should be rejected — even if it works.
