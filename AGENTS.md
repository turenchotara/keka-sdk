# Keka SDK — AI Agent Instructions

> **Single Source of Truth**: This document is the authoritative entry point for all AI agents, code editors, and IDE assistants working in this repository. All tool-specific configuration files (`.cursor/rules/`, `CLAUDE.md`, `GEMINI.md`, `.windsurfrules`) point here.

---

## 1. Repository Knowledge Base (`.ai/` Directory)

Before exploring source code or making architectural changes, **always consult the documentation in the `.ai/` directory**:

- **[project.md](file:///.ai/project.md)** — Project scope, business domain, tech stack, dependencies, and build/test/dev commands.
- **[architecture.md](file:///.ai/architecture.md)** — High-level architecture, component diagrams, request lifecycle, data flow, and error hierarchy.
- **[modules.md](file:///.ai/modules.md)** — Detailed responsibilities, interfaces, entry points, and dependencies for all modules.
- **[coding-style.md](file:///.ai/coding-style.md)** — Coding conventions, naming rules, error handling, logging, testing, and typing practices.
- **[patterns.md](file:///.ai/patterns.md)** — Implementation patterns (Composition, Sync/Async Mirroring, Builder Functions, Lazy Pagination).
- **[glossary.md](file:///.ai/glossary.md)** — Business terminology, technical terms, status enum values, and domain concepts.
- **[decisions.md](file:///.ai/decisions.md)** — Architectural Decision Records (ADRs) with rationale and evidence.
- **[changes.md](file:///.ai/changes.md)** — Historical changelog of major refactors and feature additions.

---

## 2. Core Directives

1. **Consult `.ai/` First**: Use the `.ai/` directory as the primary reference for repository context, patterns, and conventions before searching or modifying source files.
2. **Adhere to Invariants**: Follow the core invariants documented in [.ai/architecture.md](file:///.ai/architecture.md) and [.ai/patterns.md](file:///.ai/patterns.md).
3. **Maintain Knowledge Base**: Update the appropriate files in `.ai/` (especially [.ai/changes.md](file:///.ai/changes.md)) after completing significant features or refactors.

---

## 3. Verification Commands

Run verification checks before declaring any task complete:

```bash
# Code formatting
python -m black --check keka/ tests/
python -m isort --check-only keka/ tests/

# Type checking & linting
python -m mypy keka/
python -m flake8 keka/

# Tests
python -m pytest tests/ -v
```
