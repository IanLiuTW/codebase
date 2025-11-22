# Engineering Manual and Workflow

This document defines the project structure, required tools, and the full development-to-release pipeline for this repository. The goal is to keep builds fast, code clean, and releases predictable instead of chaotic.

## Project Structure and Best Practices

We use a workspace pattern (monorepo) to isolate business logic from executable binaries. This keeps compilation efficient and avoids dragging unrelated crates into your build graph.

### Tooling Requirements

The following tools must be installed locally:

- rustup: manages Rust toolchains

- bacon: live background compiler and test runner

- cargo-nextest: high performance test executor

- cargo-release: automated versioning and tagging

- cargo-wizard: applies optimized Cargo profiles

- git-cliff: automated changelog generation

- lld: faster linker for release builds

### Repository Layout

For single workspace projects, delete the `crates/` folder and place all code directly in the root.

```
.
├── Cargo.toml              # Workspace root and member definitions
├── bacon.toml              # Bacon configuration, wired for nextest
├── rust-toolchain.toml     # Pinned Rust toolchain
├── release.toml            # Release automation rules
├── crates/                 # All first party code
│   ├── my-app-core/        # Library crate: domain logic, DB access, models
│   │   ├── src/
│   │   │   ├── lib.rs      # (Unit tests live inside here, at the bottom)
│   │   │   └── prelude.rs  # Re-export pattern for ergonomic imports
│   │   └── tests/          # Integration tests (Black box testing of Public API)
│   │       └── flow_it.rs  # Example integration test file
│   └── my-app-server/      # Binary crate: server CLI or HTTP runtime
│       ├── src/
│       │   └── main.rs     # Thin entrypoint that delegates to core
│       └── tests/          # Integration tests for the executable/CLI
│           └── cli_it.rs   # Example CLI test
```

### Structural Principles

- Core business logic always lives inside a library crate.

- Binary crates must stay thin. They should parse config, initialize runtime, and call into core.

- Shared types, utilities, and DB layers belong inside core.

- Never put domain logic in the binary. That path only leads to sadness.

## Development Workflow

### 1. Initializing a New Workspace

Create a workspace and immediately apply performance optimizations so you do not suffer slow compiles later.

```
cargo new my-app
cd my-app

# Use cargo wizard to set optimal profiles
cargo wizard
```

The wizard configures LTO, panic aborts, codegen units, and other flags that reduce binary size and improve runtime speed.

### 2. Create all the configuration files

- rust-toolchain.toml
- release.toml
- bacon.toml
- cliff.toml

### 3. Live Development Loop with Bacon

Bacon gives you near instant feedback while editing. It watches the workspace, compiles incrementally, and reports issues without waiting for a manual test run.

```
bacon nextest
```

Use `t` to see tests and `c` to see cippy warnings. If bacon turns red, fix your crimes before committing more.

### 4. Pre Push Checklist

Before pushing to any feature branch, confirm that the CI pipeline will not burst into flames.

```
cargo fmt
cargo clippy -- -D warnings
cargo nextest run
```

If clippy finds a problem, assume it is right. It usually is.

## CI and Caching

GitHub Actions uses swatinem/rust cache to avoid unnecessary recompilation. The cache key is derived from Cargo.lock. If dependencies remain unchanged, CI restores binaries directly from cache.

No configuration is needed on your side. Every push to every branch benefits from the cache.

### Docker Build Strategy

Staging builds (feature branches):

- Pushing to any feature branch triggers CI to build an image named `my-app:feat-branchname`.

Production builds (releases):

- Creating a tag like `v1.0.0` triggers CI to build `my-app:1.0.0` and `my-app:latest`.

If you need manual tagging, something already went wrong upstream.

## Release Workflow

Releases are handled through cargo release to ensure version consistency across crates and tags.

### Golden Rules

- Never edit versions manually in Cargo.toml.

- Never create git tags yourself.

- Never try to outsmart cargo release. You will lose.

### How to Ship

1.  Ensure you are on the main branch with a clean working tree.

2.  Perform a dry run:

```
cargo release 1.1.0
```

1.  Execute the release:

```
cargo release 1.1.0 --execute
```

### What Happens After

- Versions are incremented and committed.

- A tag is created and pushed.

- GitHub Actions triggers the production pipeline.

- Docker images `my-app:1.1.0` and `my-app:latest` are built and published.

## Configuration File Templates

This section provides reference templates for the core configuration files used in the workspace. Copy these into new projects to ensure consistent builds, releases, and toolchain behavior across the organization.

### rust-toolchain.toml

```
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
```

### release.toml

```
allow-branch = ["main", "master"]
sign-commit = false
sign-tag = false
push = true
publish = false 

pre-release-hook = ["sh", "-c", "git cliff -o CHANGELOG.md --tag {{version}} && git add CHANGELOG.md"]
```

### bacon.toml

```
default_job = "nextest"

[jobs.nextest]
command = [
    "cargo", "nextest", "run",
    "--hide-progress-bar", "--failure-output", "final"
]
need_stdout = true
analyzer = "nextest"
```

### cliff.toml

```
# git-cliff ~ configuration file
# https://git-cliff.org/docs/configuration

[changelog]
header = """
# Changelog

"""
body = """
---
{% if version %}\
    {% if previous.version %}\
        ## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
    {% else %}\
        ## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
    {% endif %}\
{% else %}\
    ## [unreleased]
{% endif %}\
{% for group, commits in commits | group_by(attribute="group") %}
    ### {{ group | striptags | trim | upper_first }}
    {% for commit in commits
    | filter(attribute="scope")
    | sort(attribute="scope") %}
        - **({{commit.scope}})**{% if commit.breaking %} [**breaking**]{% endif %} \
            {{ commit.message }} - *{{ commit.id | truncate(length=7, end="") }}* by {{ commit.author.name }}
    {%- endfor -%}
    {% raw %}\n{% endraw %}\
    {%- for commit in commits %}
        {%- if commit.scope -%}
        {% else -%}
            - {% if commit.breaking %} [**breaking**]{% endif %}\
                {{ commit.message }} - *{{ commit.id | truncate(length=7, end="") }}* by {{ commit.author.name }}
        {% endif -%}
    {% endfor -%}
{% endfor %}\n
### Commit Statistics\n
- {{ statistics.commit_count }} commit(s) contributed to the release.
- {{ statistics.commits_timespan | default(value=0) }} day(s) passed between the first and last commit.
- {{ statistics.conventional_commit_count }} commit(s) parsed as conventional.
- {{ statistics.links | length }} linked issue(s) detected in commits.
{%- if statistics.links | length > 0 %}
	{%- for link in statistics.links %}
        {{ "  " }}- [{{ link.text }}]({{ link.href }}) (referenced {{ link.count }} time(s))
	{%- endfor %}
{%- endif %}
{%- if statistics.days_passed_since_last_release %}
	- {{ statistics.days_passed_since_last_release }} day(s) passed between releases.
{%- endif %}\n\n
"""
trim = true

[git]
conventional_commits = true
filter_unconventional = false
split_commits = false
commit_parsers = [
  { message = "^feat", group = "Features" },
  { message = "^fix", group = "Bug Fixes" },
  { message = "^doc", group = "Documentation" },
  { message = "^perf", group = "Performance" },
  { message = "^refactor", group = "Refactor" },
  { message = "^chore|ci", group = "Miscellaneous", skip = true },
]
# Protects against parsing the generated changelog itself
filter_commits = false
tag_pattern = "v[0-9].*"
```

### clippy.toml (Optional)

```
# Fail on any warning produced by Clippy
warn-once = false

# Turn selected categories into hard errors
# Good for teams that want consistency enforced by the compiler
deny = [
    "clippy::unwrap_used",
    "clippy::expect_used",
    "clippy::panic",
    "clippy::todo",
    "clippy::unimplemented",
    "clippy::clone_on_ref_ptr",
    "clippy::map_unwrap_or",
]

warn = [
    "clippy::pedantic",
    "clippy::nursery",
]

# Allow lints that tend to create noise without real value
allow = [
    "clippy::module_name_repetitions",
    "clippy::missing_errors_doc",
    "clippy::missing_panics_doc",
]
```

### Cargo.toml (Example for Workspace Root)

```
[workspace]
members = [
    "crates/my-app-core",
    "crates/my-app-server"
]

resolver = "2"

[workspace.package]
edition = "2021"

[workspace.metadata.release]
# Ensures cargo release respects the workspace structure
shared-version = true
dependent-version = "upgrade"
```
