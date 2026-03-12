---
id: 1
title: "Amend Tech Matrix"
stage: constitution
date_iso: "2026-02-24"
surface: agent
model: claude-opus-4-6
feature: "none"
branch: main
user: user
command: "/sp.constitution"
labels: ["constitution", "technology", "phase", "constraints"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml:
  - "none"
outcome: "completed"
evaluation: "Constitution successfully amended with phase-specific technology matrix"
---

# Evolution of Todo Constitution

## User Input
```
Amend the global constitution technology matrix to reflect Phase II requirements as follows:

Phase II:
- Backend: Python REST API
- Database: Neon Serverless PostgreSQL
- ORM/Data layer: SQLModel or equivalent
- Frontend: Next.js (React, TypeScript)
- Authentication: Better Auth (signup/signin)
- Architecture: Full-stack web application

Phase I remains:
- In-memory console application only

Phase III and later:
- Advanced cloud infrastructure, agents, AI, orchestration

Rules:
- Authentication is allowed starting Phase II
- Web frontend is allowed starting Phase II
- Neon PostgreSQL is allowed starting Phase II
- No AI or agent frameworks until later phases

This amendment must preserve phase isolation and act as the authoritative technology policy.
```

## Response
The constitution has been successfully amended to version 1.1.0 with a detailed phase-specific technology matrix:

### Key Changes Made:
1. **Updated Technology Constraints principle** to emphasize phase-specific technology usage
2. **Added Phase I Requirements section** - specifying in-memory console application only
3. **Added Phase II Requirements section** - specifying full-stack web with authentication
4. **Added Phase III+ Requirements section** - specifying advanced cloud/agents/AI technologies
5. **Enhanced governance section** - clarifying that technology usage must align with appropriate phase requirements

### Phase Isolation Preserved:
- Phase I: Console application only, no web/auth features
- Phase II: Full-stack web application with authentication using Better Auth
- Phase III+: Advanced features like AI, orchestration, and agent frameworks
- Clear prohibition against using later-phase technologies in earlier phases

The amendment maintains the authoritative technology policy while ensuring proper phase isolation as requested.