# AGENTS.md

A personal learning project: a minimal Litestar application with an HTTP
route and a Strawberry GraphQL endpoint sharing one dependency-injected
schema.

Follow the conventions already in the tree, and keep a change scoped to what
was asked for.

## What is here

| Path                          | What it is                                  |
| ------------------------------ | -------------------------------------------- |
| `src/app/__init__.py`         | Litestar app: `GET /`, GraphQL controller at `/graphql` |
| `tests/test_app.py`           | End-to-end tests for both routes via `TestClient` |
| `pyproject.toml`              | Project metadata; ruff, mypy, and pytest configuration |
| `.github/workflows/tests.yml` | CI: ruff check, ruff format --check, mypy, pytest |

## Which policy applies

- Documentation, user-facing text, commit messages, docstrings, and source
  comments: [.github/WRITING.md](.github/WRITING.md)
- Environment, the gates, tests, and pull requests:
  [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

Each of those is the single home for its subject. Where a rule seems to be
stated twice, the file listed above is the one that governs.

## Change discipline

- Make the smallest coherent change that solves the verified problem; keep
  unrelated cleanup out of it.
- Reuse an existing file, helper, API, or test before adding a new one.
  Modify in place when the change fits the file's responsibility.
- Keep new APIs private until a caller outside the module needs them.
- Add a file only for a durable boundary — a distinct responsibility,
  independent reuse, or splitting an oversized module — not for a
  single-use helper or a one-line re-export.
- A passing gate is evidence only once it has been shown capable of
  failing. Pair a new test with a deliberate break that proves it bites.
- Keep this file and the docs it points to pruned: delete a line whose
  removal would not cause a mistake, and grow WRITING.md, CONTRIBUTING.md,
  or a nested AGENTS.md instead of this one.

The Litestar CLI does not auto-discover the app in this layout: pass
`--app app:app` explicitly, or it errors with "Could not find Litestar
instance or factory". A doctest on a function decorated with a Litestar
route decorator (`@get`, `@post`, …) is silently never collected — the
decorator replaces the function object. See
[Documented examples that run](.github/WRITING.md#documented-examples-that-run).

## References

- [Litestar documentation](https://litestar.dev)
- [Strawberry GraphQL documentation](https://strawberry.rocks)
