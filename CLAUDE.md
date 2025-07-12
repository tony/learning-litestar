# CLAUDE.md

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
- **app/__init__.py**: Main application module containing:
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