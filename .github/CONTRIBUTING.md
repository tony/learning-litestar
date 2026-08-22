# Contributing

Thanks for looking. This is a personal learning project exploring Litestar
and Strawberry GraphQL; bug reports with a reproduction and notes on where
the documentation misled you are the most useful thing to send.

How this project writes prose — README, commit messages, docstrings, and
source comments — is set out separately in [WRITING.md](WRITING.md). Read
that before changing any of it. The constraints every change is held to, and
the map of what is where, are in [AGENTS.md](../AGENTS.md).

## Getting set up

```console
$ uv sync --all-extras --dev
```

## Running the app

```console
$ uv run litestar --app app:app run --reload
```

The Litestar CLI does not auto-discover the application instance in this
layout — omitting `--app app:app` fails with "Could not find Litestar
instance or factory". The server listens on <http://127.0.0.1:8000/> by
default.

## The gates

Format:

```console
$ uv run ruff format .
```

Lint:

```console
$ uv run ruff check .
```

Type-check:

```console
$ uv run mypy .
```

Test:

```console
$ uv run pytest
```

CI (`.github/workflows/tests.yml`) runs exactly these four, in this order,
against Python 3.14, plus `uv run py.test` as the test invocation — an alias
for the same command. Every gate it runs has to pass before a change is
done.

Documentation is a gate, not a courtesy: `pyproject.toml` configures
`--doctest-modules` under `[tool.pytest]`, and `uv run pytest` above
collects doctests from `src` and `tests` on every run — there is no
separate doctest step. There are no doctests yet, and one repo-specific
gotcha when adding one — see
[Documented examples that run](WRITING.md#documented-examples-that-run).

Before claiming a test or a gate works, show it failing. A gate that has
never been red is an assumption.

## Tests

Tests use `litestar.testing.TestClient` as a context manager against the
`app` instance from `src/app/__init__.py`, with `app.debug = True` set at
module scope in `tests/test_app.py`. There are no external services, no
environment variables, and no custom pytest markers or fixtures to know
about.

To re-run tests on save, pass the directory to watch — `pytest-watcher`
takes it as a required argument:

```console
$ uv run pytest-watcher .
```

## Pull requests

One subject per pull request. Unrelated cleanup found along the way belongs
in its own commit, and usually in its own pull request.

Discuss a substantial change via an issue before making it.

Commit format is in [WRITING.md](WRITING.md#commits).

## Decorum

- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of
  personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should
  always assume good intentions.
- Behaviour which can be reasonably considered harassment will not be
  tolerated.

Based on [Ruby's Community Conduct Guideline](https://www.ruby-lang.org/en/conduct/).
