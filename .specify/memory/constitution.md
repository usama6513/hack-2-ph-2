<!--
Sync Impact Report:
Version change: 1.0.0 → 1.1.0
Modified principles: Technology Constraints (expanded with phase-specific details)
Added sections: Phase-specific Technology Constraints subsections
Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending
- .specify/templates/spec-template.md ⚠ pending
- .specify/templates/tasks-template.md ⚠ pending
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->

# Evolution of Todo Constitution

## Core Principles

### Spec-Driven Development (NON-NEGOTIABLE)
No agent may write code without approved specs and tasks. All work must follow: Constitution → Specs → Plan → Tasks → Implement.
<!-- Rationale: Ensures all development is intentional, traceable, and aligned with business goals. Prevents feature creep and maintains quality standards. -->

### Agent Behavior Rules
No manual coding by humans, no feature invention, no deviation from approved specifications. Refinement must occur at spec level, not code level.
<!-- Rationale: Maintains consistency and prevents scope creep. Ensures all changes go through proper review and planning processes. -->

### Phase Governance
Each phase is strictly scoped by its specification. Future-phase features must never leak into earlier phases. Architecture may evolve only through updated specs and plans.
<!-- Rationale: Maintains clear boundaries between development phases and prevents premature implementation of future requirements. -->

### Technology Constraints
Technology stack evolves by phase: Phase I (in-memory console), Phase II (full-stack web with auth), Phase III+ (advanced cloud/agents/AI). Each phase MUST only use technologies specified for its phase.
<!-- Rationale: Provides consistent technology evolution across project phases to ensure maintainability, proper sequencing, and appropriate complexity at each stage. -->

### Quality Principles
Clean architecture, stateless services where required, clear separation of concerns, cloud-native readiness.
<!-- Rationale: Ensures maintainable, scalable, and deployable systems that meet modern software engineering standards. -->

### Implementation Discipline
All code changes must be traceable to approved tasks. No speculative development or "just in case" features.
<!-- Rationale: Maintains focus on delivering value through approved requirements while preventing technical bloat. -->

## Technology Constraints

### Phase I Requirements (In-memory Console Application)
- Backend: Python console application only (no web framework)
- Database: None (in-memory only)
- Data layer: Simple in-memory structures (lists, dictionaries)
- Frontend: None (CLI only)
- Authentication: Not allowed
- Architecture: Single-file console application

### Phase II Requirements (Full-Stack Web Application)
- Backend: Python REST API with FastAPI
- Database: Neon Serverless PostgreSQL
- ORM/Data layer: SQLModel or equivalent
- Frontend: Next.js (React, TypeScript)
- Authentication: Better Auth (signup/signin)
- Architecture: Full-stack web application with clean separation
- Authorization: Authentication is allowed starting Phase II

### Phase III and Later Requirements (Advanced Cloud/Agents/AI)
- Backend: Python with advanced frameworks as needed
- Database: Neon Serverless PostgreSQL with advanced features
- Infrastructure: Docker, Kubernetes for orchestration
- Services: Kafka for message streaming, Dapr for distributed runtime
- AI/Agents: OpenAI Agents SDK, MCP (Model Context Protocol) for communication
- Advanced: AI, orchestration, and agent frameworks allowed

### Infrastructure Requirements (Cross-Phase)
- Docker for containerization (Phase II+)
- Kubernetes for orchestration (Phase III+)
- Kafka for message streaming (Phase III+)
- Dapr for distributed application runtime (Phase III+)

## Development Workflow

### Specification Process
- All features must begin with an approved specification
- Specifications must clearly define scope, requirements, and acceptance criteria
- Changes to specifications require formal approval process

### Task Management
- All implementation work must be assigned to specific tasks derived from approved specs
- Tasks must be testable and have measurable outcomes
- No implementation work without corresponding approved tasks

### Quality Assurance
- Clean architecture patterns must be followed
- Services must be stateless where required
- Clear separation of concerns in all code
- Cloud-native readiness for all components

## Governance

This constitution is the supreme governing document for all agents working on the Evolution of Todo project. All development work must comply with the principles and constraints outlined herein. Technology usage MUST align with the appropriate phase requirements. No technology from later phases may be used in earlier phases. Amendments to this constitution require explicit approval and must follow a formal change management process that includes impact assessment and review by project stakeholders.

**Version**: 1.1.0 | **Ratified**: 2026-02-24 | **Last Amended**: 2026-02-24
