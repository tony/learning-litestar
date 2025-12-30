# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python web application using Litestar framework with GraphQL support via Strawberry GraphQL. The project follows modern Python development practices with strict type checking and comprehensive linting.

## Development Commands

### Package Management
- **Install dependencies**: `uv sync --all-extras --dev`
- **Add a dependency**: `uv add <package>`
- **Add a dev dependency**: `uv add --dev <package>`

### Testing
- **Run all tests**: `uv run pytest` or `uv run py.test`
- **Run a specific test**: `uv run pytest tests/test_app.py::test_hello_world`
- **Watch mode (auto-test)**: `uv run pytest-watcher`

### Code Quality
- **Run all checks**: `uv run ruff check . && uv run ruff format . --check && uv run mypy .`
- **Lint code**: `uv run ruff check .`
- **Format code**: `uv run ruff format .`
- **Type checking**: `uv run mypy .`

### Running the Application
- **Development server**: `uv run litestar run --reload`
- **Production server**: `uv run litestar run`

## Architecture

### Application Structure
- **src/app/__init__.py**: Main application module containing:
  - REST endpoint at `/` returning "Hello, world!"
  - GraphQL endpoint at `/graphql` with Strawberry GraphQL schema
  - Litestar application instance configured with route handlers

### Key Components
1. **Litestar Framework**: Modern async Python web framework handling HTTP requests
2. **Strawberry GraphQL**: Type-safe GraphQL implementation using Python type hints
3. **Testing**: Uses pytest with Litestar's TestClient for integration testing

### Configuration
- **pyproject.toml**: Central configuration for dependencies, tools, and project metadata
- **Strict Type Checking**: mypy configured with strict mode enforcing type safety
- **Comprehensive Linting**: ruff configured with extensive rule sets for code quality

## Doctests

**All functions and methods MUST have working doctests.** Doctests serve as both documentation and tests.

**CRITICAL RULES:**
- Doctests MUST actually execute - never comment out function calls or similar
- Doctests MUST NOT be converted to `.. code-block::` as a workaround (code-blocks don't run)
- If you cannot create a working doctest, **STOP and ask for help**

**Available tools for doctests:**
- `doctest_namespace` fixtures: `tmp_path`
- Ellipsis for variable output: `# doctest: +ELLIPSIS`
- Update `conftest.py` to add new fixtures to `doctest_namespace`

**`# doctest: +SKIP` is NOT permitted** - it's just another workaround that doesn't test anything. Use fixtures properly.

**Using fixtures in doctests:**
```python
>>> from litestar.testing import TestClient
>>> from app import app
>>> client = TestClient(app)
>>> response = client.get("/")
>>> response.status_code
200
```

## Git Commit Standards

### Commit Message Format
```
Component/File(commit-type[Subcomponent/method]): Concise description

why: Explanation of necessity or impact.
what:
- Specific technical changes made
- Focused on a single topic
```

### Common Commit Types
- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting

### Dependencies Commit Format
- Python packages: `py(deps): Package update`
- Python dev packages: `py(deps[dev]): Dev package update`

### Examples

#### Feature Addition
```
core/schema(feat[Query]): Add fruit filtering by color

why: Users need to filter fruits by color in GraphQL queries
what:
- Add color filter parameter to fruits query
- Update resolver to handle color filtering
- Add tests for color filtering
```

#### Bug Fix
```
core/types(fix[FruitType]): Correct optional color relationship

why: Color field was incorrectly marked as required
what:
- Change color field to use Optional type
- Update tests to handle None values
```

#### Dependencies Update
```
py(deps[dev]): Add django-stubs for type checking

why: Improve type safety for Django models and ORM
what:
- Add django-stubs to dev dependencies
- Configure MyPy to use django-stubs plugin
```
For multi-line commits, use heredoc to preserve formatting:
```bash
git commit -m "$(cat <<'EOF'
feat(Component[method]) add feature description

why: Explanation of the change.
what:
- First change
- Second change
EOF
)"
```

### Guidelines
- Subject line: Maximum 50 characters
- Body lines: Maximum 72 characters
- Use imperative mood ("Add", "Fix", not "Added", "Fixed")
- One topic per commit
- Separate subject from body with blank line
- Mark breaking changes: `BREAKING:`
