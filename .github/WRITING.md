# Writing

How this project writes prose, for humans and agents alike. It governs
`README.md`, commit messages, docstrings, and source comments — every surface
a reader reaches. There is no `CHANGES` file, release notes, or CLI in this
repository, so those sections are omitted; see the end of this document if
that ever changes.

For environment setup, the gates, and pull request workflow, see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Voice

Three surfaces, one voice. A docstring says what a caller may rely on;
`README.md` says what happens; a commit message says why. All are present
tense, lead with the thing being described, and stop. Why it was built that
way belongs in the commit message, which is timestamped and attached to the
diff.

The most useful editing operation is deleting the introductory sentence.

Lead with verbs and name concrete things. Put identifiers in backticks. Prefer
short declarative sentences, one operational fact each. Do not explain Python
to Python developers; do explain this project's semantics.

Type annotations describe shape. Documentation describes meaning. A sentence
that restates a signature has said nothing.

Use MUST, SHOULD, and MAY only where the normative sense is meant. Say what
actually happens rather than that something is "supported".

| Instead of                       | Prefer                            |
| --------------------------------- | ---------------------------------- |
| "We added…"                      | "`GET /` now returns…"            |
| "New and improved"               | "The GraphQL schema now…"         |
| "powerful", "seamless"           | state the capability              |
| "easily", "simply", "just"       | omit                              |
| "simple", "obvious", "intuitive" | omit                              |
| "robust"                         | name the failure that is handled  |
| "comprehensive"                  | name what is covered              |
| "production-ready"               | state the guarantee               |
| "optimized", "blazingly fast"    | give the magnitude                |
| "various fixes"                  | name the components               |
| "under the hood"                 | omit unless observable            |
| "please note that", "note that"  | state the fact                    |
| "leverage", "utilize"            | "use"                             |
| "delve into"                     | "read", or omit                   |
| "best practices"                 | name the practice                 |
| "in order to"                    | "to"                              |

## Who you are writing for

The default reader is fluent in Python and new to this project. They can read
a signature; they cannot guess how the Litestar app and the Strawberry
GraphQL schema fit together. Serve them first.

Rules that follow:

- **Second person, present tense, active.** "You send a request to `/`", not
  "A response is generated". Address the reader who is doing the thing.
- **Concept before API surface.** Open by saying what a route or resolver
  *does* for the reader. The signature is the last detail they need, not the
  first.
- **Say when they can stop.** Lead with the default and the reassurance. Let
  a skimmer leave after one paragraph.
- **Progressive disclosure.** Order by how many readers need it: the common
  call, then the one argument a few will tune, then the lower-level
  primitive.
- **Name the trade-off.** If a choice costs something — an extra dependency,
  a synchronous handler that blocks the loop — say so, and say what it buys.
  State it; do not sell it.

## README

A README is the shortest path from "what is this?" to competent use, not the
project's autobiography.

The first sentence is a contract. It says what abstraction the reader has
been handed, concretely enough to tell this package apart from the
neighbouring one.

Get to a runnable command or snippet before anything the reader can skip.

State the minimum Python version in prose, not only in the requirement
string. `requires-python` in `pyproject.toml` is the authority; the README
must agree with it.

Name the distribution, the import, and the executable separately wherever
they differ. In this repository the distribution is `learning-litestar`, the
import is `app` (`src/app/__init__.py`), and there is no console script.

Examples are executable, not illustrative fiction. Never
`your-command <some-options>`. See
[Documented examples that run](#documented-examples-that-run) for which
blocks are executed and how to write one that qualifies.

Document the semantic model, not the flag list — what a route returns, what
status code it uses, what the GraphQL schema exposes.

State defaults explicitly — defaults are API.

Headings stay conventional and stable, because people deep-link them.

## Documented examples that run

**Every function and method should carry a working doctest.** Examples in
this fleet are tests, and that is true here too: `pyproject.toml` sets
`addopts`, `doctest_optionflags`, and `testpaths` under `[tool.pytest]`, and
pytest 9 reads that table as native TOML configuration — do not conclude
otherwise from a bare `pytest` run printing no `configfile:` line;
`--no-header` is itself one of the configured `addopts`, so a working
configuration looks unconfigured at a glance. Confirm the real state by
comparing collection with configuration disabled against configuration
active:

```console
$ uv run pytest --collect-only -c /dev/null
```

```console
$ uv run pytest --collect-only --override-ini=addopts=
```

The second form reports `configfile: pyproject.toml` and
`testpaths: src, tests` in the header. `--doctest-modules` is active,
`ELLIPSIS` and `NORMALIZE_WHITESPACE` are enabled, and both `src` and
`tests` are scanned for `>>> ` prompts.

**Today, zero doctests exist**, so `pytest --collect-only` reports only the
two tests in `tests/test_app.py`. That is a content gap, not a
configuration problem — add an `Examples` block under `src/` or `tests/`
and it runs on the next `pytest` invocation, with one exception below.

**A Litestar route handler swallows its own doctest.** `@get`, `@post`, and
the other Litestar route decorators replace the decorated function with a
handler instance (`litestar.handlers.http_handlers.decorators.get`, for
`hello_world`) whose `__module__` points at Litestar's own package, not
`app`. `pytest --doctest-modules` uses `doctest.DocTestFinder`, which only
extracts docstrings from objects it can attribute to the module under test
— so a doctest written on `hello_world`'s docstring is silently never
collected, with no warning and no error. Verified: adding an `Examples`
block to `hello_world` and running
`pytest --collect-only --doctest-modules src/app/__init__.py` collects
nothing, while the same block on `Query.hello` — decorated with
`@strawberry.field`, which does not replace the function object the same
way — collects and passes normally. Put runnable examples on plain
functions, `strawberry` resolvers, or module-level helpers; do not rely on
a docstring under a Litestar route decorator being tested.

Docstring examples use the NumPy `Examples` section:

    Examples
    --------
    >>> Query().hello()
    'Hello World'

When editing a file that already contains `>>> ` prompts, count them before
and after — removing prompts silently deletes a test even while the suite
stays green.

## Docstrings

The prime directive: never restate the type. The annotation is the source of
truth; the docstring carries what the annotation cannot.

Document instead the dimensions the type system cannot encode: what a
handler mutates, what must be awaited before a result is valid, which
exceptions a resolver raises and what triggers each, whether a route is
idempotent, and platform or version constraints.

The first sentence stands alone; tooling truncates there. PEP 257 applies:
triple double quotes, an imperative one-line summary ending in a period, a
blank line before any extended description. Do not repeat an introspectable
signature.

This repository's docstring dialect is NumPy, enforced by
`ruff.lint.pydocstyle.convention = "numpy"` — not relitigated in review.

**Classes with fields** — `NamedTuple`, dataclasses, `strawberry.type` —
document every field in an `Attributes` section:

```python
@strawberry.type
class Query:
    """Root GraphQL query type.

    Attributes
    ----------
    greeting : str
        Configured greeting returned by the `hello` resolver.
    """
```

A type says how a field is shaped, not what it holds. Describing each one
keeps that meaning next to the code, and anything that renders the class —
autodoc, a REPL, an editor tooltip — has a description to show instead of a
bare name.

## Source comments

A comment ships only if it passes all three gates. Fail any: delete or
rewrite. Borderline: delete — borderline means the information is
reconstructible, which is what makes deletion cheap.

**Loss.** Three years from now, would losing this cost a maintainer real
time rediscovering intent, an invariant, a constraint, or a failure mode the
code and tests do not already make obvious?

**Elite.** Would SQLite, Redis, the Go standard library, or CPython write
this comment, at this length? Those projects state the constraint and stop.
They do not argue with an imagined objector.

**Upkeep.** Will it stay true without maintenance? A comment that hand-syncs
a value the code owns — a count, an offset, a line reference, a duplicated
constant — is false the first time that value moves.

### Ceiling

One or two lines. A comment reaching four is either carrying several facts,
in which case split it, or arguing, in which case cut it to the fact.

Rationale, alternatives weighed, and the story of how the code got here
belong in the commit message: timestamped, attached to the exact diff, and
free to maintain.

### Keep

- Why over how: upstream quirks, protocol and compatibility constraints,
  performance tradeoffs still part of the contract.
- Invariants, preconditions, ordering, lifetime, and concurrency
  requirements that types and tests cannot express.
- Code that looks wrong but is not, so a later cleanup does not reintroduce
  the bug.
- A high-level sketch of an algorithm whose local operations do not reveal
  the whole.

### Delete

- Narration of the next lines; code translated into English.
- Restated names, types, defaults, or control flow.
- Values duplicated from the code and hand-synced.
- Justification, hedging, or apology for a choice.
- Speculation about future requirements.
- History version control already holds, including commented-out code.
- Ticket and issue numbers. They say nothing to a reader without tracker
  access, and they rot when the tracker moves.
- Transient observations — "currently", "for now", "the latest release" —
  that go stale with no nearby edit.

### The upkeep gate in practice

It reaches values that track our own code. It does not reach frozen
external facts.

Bad (Delete):

```python
# There are 321 tests to complete for servers.
```

Good (Keep):

```python
# CPython < 3.11 has no ExceptionGroup, so this branch stays.
```

### Documentation exception

Minimal usage examples, and parameter, return, and raises entries on public
API, are exempt from the loss gate — they serve the caller, not the
maintainer. They are exempt from nothing else. Ceiling: a good man page
entry.

## Terminology and capitalization

Pick the domain noun and keep it. If a function is a "resolver", do not call
it a "query function" in one paragraph and a "handler" in the next. If the
route is `GET /`, write "route" everywhere rather than alternating with
"endpoint" and "path".

Stable vocabulary is what makes search, deep links, and an agent's retrieval
work at all.

Litestar, Strawberry, GraphQL, and Python keep their own capitalisation.
Distribution names are written as they are published: `learning-litestar`.

Do not write counts into prose — how many routes exist, how many tests there
are. They go stale silently and no reader needs them.

## Markdown

Prose wraps at 80 columns. Table rows, badge lines, and long links are
exempt, because breaking them harms rendering. A pull request or issue body
does not wrap at all: GitHub renders a single newline as a space in a file
and as a line break in a comment, so a wrapped comment body arrives as
ragged stubs.

GitHub alert blocks — `> [!NOTE]`, `> [!WARNING]` — render as literal text
outside GitHub, so reserve them for at most one load-bearing warning per
document.

Do not use a local absolute path or an email address in anything published.

## Code blocks

Code blocks are paste-and-run units: pasting one block runs exactly one
intended action.

- **One command per block.** Multiple steps may share a block only when
  explicitly chained with `&&`, `;`, or `\` continuations — the chain is
  then one logical command.
- **Explanations go in prose above the block**, never as `#` comments
  inside it.
- **Command menus are per-command blocks with prose lead-ins**, not tables.
- **Shell commands use the `console` tag with a `$ ` prefix.** This
  separates interactive commands from scripts and enables prompt-aware
  copy.
- **Split long commands with `\`** — one flag or flag+value pair per
  indented continuation line, positional arguments last.

Good — show the last ten commits as a graph:

```console
$ git log \
    --max-count=10 \
    --graph \
    --oneline
```

Bad:

```console
# Show the last ten commits as a graph
$ git log --max-count=10 --graph --oneline
```

## Commits

```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

Keep the subject to 50 characters or fewer, excluding any trailing `(#NN)`
pull request reference, and wrap body lines at 72. A blank line separates
the `why:` and `what:` blocks.

Subjects are plain English. Never put curriculum codes or other
repo-internal shorthand in the subject line — a reader of
`git log --oneline` should understand every title cold. Mark a breaking
change with `BREAKING:` in the body.

Routine maintenance commits drop the colon and take a capitalised
description, which is what distinguishes them at a glance in
`git log --oneline`:

```
py(deps[dev]) Bump dev packages
ai(rules[AGENTS]) Judge comments by three gates
```

Everything that changes behaviour keeps the colon.

Common types:

- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (`CLAUDE.md`)

Example:

```
Pane(feat[send_keys]): Add support for a literal flag

why: Send characters without tmux interpreting them.

what:
- Add a literal parameter to send_keys
- Pass -l when it is set
```

For a multi-line message, use a heredoc so the formatting survives:

```console
$ git commit -m "$(cat <<'EOF'
Scope(feat[detail]): Concise description

why: Explanation of the change.

what:
- First change
- Second change
EOF
)"
```

## Slop prevention

Treat AI slop as review-hostile noise, not as proof that text or code is
wrong. The goal is to maximise information density.

- **AI signatures.** No "Generated by", no conversational filler, no
  unexplained emoji, no tool metadata.
- **Brittle references.** No hard-coded line numbers, fragile file counts,
  dated "as of" claims, bare SHAs, or local absolute paths — unless they are
  strict evidentiary artefacts such as a benchmark log.
- **Diff narration.** Do not restate what moved, was renamed, or was
  removed in anything the reader holds alongside the diff: code,
  docstrings, README, or a pull request description.
- **Branch-internal narrative.** Do not mention intermediate states,
  abandoned approaches, or "no longer" behaviour unless users of a
  published release actually experienced the old state — see
  [The published-release test](#the-published-release-test).
- **Low-value scaffolding.** No ownerless TODOs, unused future-proofing,
  debug artefacts, or defensive wrappers around failure modes nothing can
  reach.
- **Prose inflation.** The diction table under [Voice](#voice) governs;
  replace an inflated word with a concrete description of behaviour,
  constraints, or trade-offs.
- **Coded labels.** Write rules and findings as plain imperatives. No
  `[R1]`, `Option B`, or any index a reader has to decode.

Preserve the "why". Never delete a comment documenting an invariant, a
protocol constraint, a platform quirk, or an upstream workaround — those are
the facts [Source comments](#source-comments) keeps, and every other
comment is judged by it.

**Evidence is immune.** Preserve exact counts, dates, and SHAs when they
serve as evidence — a benchmark result, a stack trace, a lockfile diff.
Coincidentally looking like a brittle reference does not make evidence
disposable.

**Behaviour over inventory.** A useful description explains what changed
for the system or the reader; it does not provide an inventory of files or
functions the diff already shows.

### Durable source links

Link to a pinned revision, never to trunk. A pinned permalink is not a
brittle reference; an unlinked SHA dropped into prose is. `blob/main/…`
links rot silently — the file moves, lines shift, and the anchor lands on
unrelated code while still resolving.

- Prefer a release tag (`blob/v1.4.0/…`). Most durable, and it tells the
  reader which released version the claim held for.
- Otherwise use a 7-char commit ref (`blob/9a29b1a/…`) reachable from
  trunk. Use when there is no tag or the claim is about unreleased code.
  Never a PR-head SHA — it can be rebased or garbage-collected.
- Reserve `blob/main/…` for living documents meant to always show the
  latest state, such as a contributing guide.
- Line anchors (`#L120-L145`) are only safe on a pinned ref.

### The published-release test

Long-running branches accumulate tactical decisions — renames, refactors,
attempts-then-reverts. When deciding what counts as branch-internal, use
trunk or the parent branch as the baseline — not intermediate states inside
the current branch. Ask:

> Did users of the most recently published release ever experience this old
> name, old behavior, or bug?

If the answer is no, it is branch-internal narrative. Move it to the commit
message and describe only the final state in the artifact.

Keep in shipped artifacts: comments explaining why the current code looks
this way (invariants, platform quirks) that make sense to a reader who
never saw the previous version.

### Cleanup in hindsight

When applying these rules retroactively from inside a feature branch, first
establish scope by diffing against the parent branch or trunk to identify
which commits the branch actually introduced. For in-branch commits, choose
between `fixup!` commits squashed with `git rebase --autosquash` to address
each causal commit at its source, or a single cleanup commit at branch tip.
Leave trunk or parent-branch commits alone unless explicitly asked to
rewrite them, and never rewrite shared history.
