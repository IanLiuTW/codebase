# Engineering Manual and Workflow

This document defines the project structure, required tools, and the full development-to-release pipeline for this repository. The goal is to keep builds fast, code clean, and releases predictable instead of chaotic.

## Project Structure and Best Practices

We use a workspace pattern (monorepo) to isolate business logic from executable binaries. This keeps compilation efficient and avoids dragging unrelated crates into your build graph.

### Tooling Requirements

The following tools must be installed locally:

- uv:

### Repository Layout

```
.
├── pyproject.toml          # Thr file for pependencies, build, configs
├── uv.lock                 # The file for pinning versions
├── .dockerignore
├── Dockerfile
├── src/
│   └── my_app/             # Your package source
│       ├── __init__.py
│       ├── main.py         # Entry point
│       └── core/           # Domain logic
└── tests/
    ├── __init__.py
    └── test_something.py
```

### Structural Principles

- Core business logic always lives inside the source package. Logic should reside within src/{app_name}/ (specifically the core submodule), not at the root level or mixed into scripts.

- The entry point (main.py) must stay thin. It should only handle argument parsing, environment configuration, and logging setup before handing off execution to the core package.

- Shared types, utilities, and data layers belong inside core. Keep domain models and infrastructure code isolated within src/my_app/core/ to ensure the application remains modular and testable.

- Never put domain logic in the entry point. Avoid writing business rules in main.py. That path makes testing difficult and leads to sadness.

## Development Workflow

### 1. Initializing a New Workspace

Create a project.

```
# Initialize with python 3.12 (or your preferred version)
uv init --python 3.12 --app --package my_app
cd my_app
```

```
# Runtime dependencies
uv add fastapi uvicorn pydantic

# Dev dependencies (The "toolchain" components)
uv add --dev ruff pytest pytest-cov pytest-watcher commitizen pip-audit
```

### 2. Create config files and set up git and versioning

Include configs in `pyproject.toml`.

```toml
[tool.pytest.ini_options]
addopts = "-ra -q"
testpaths = ["tests"]

[tool.coverage.run]
source = ["src"]
branch = true
omit = [
]

[tool.coverage.report]
show_missing = true
skip_empty = true
fail_under = 80

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "SIM", "UP"] # Enable rules (Errors, formatting, imports, bugbear)
ignore = []

[tool.commitizen]
name = "cz_conventional_commits"
tag_format = "v$version"
version_scheme = "semver"
version_provider = "pep621" # Reads version from [project] table above
update_changelog_on_bump = true
major_version_zero = true
```

> [!NOTE]
> Create an initial git commit and set up the upstream git repository here. Consider adding a license.

### 3. Live Development Loop

A. The Server Loop (Hot Reload) When working on the API, you want the server to restart on save.

```Bash
# Runs the app, reloading whenever code changes
uv run fastapi dev src/my_app/main.py

```

B. The Test Loop (TDD) To get immediate feedback on broken tests:

```Bash
uv run ptw .
```

### 4. Pre Push Checklist

Before pushing to any feature branch, confirm that the CI pipeline will not burst into flames.

```
uv run ruff format
uv run ruff check --fix
uv run pytest
```

## CI and Caching

Make sure you have set up Dockerfile and CI pipeline. This section will assume you are using the examples provided below.

- [Example Dockerfile](docker/)
- [Example CI Github Actions](github/)

> [!NOTE]
> Go through the docker and CI files to double check the content. Make sure all CI secrets are set up.

### Docker Build Strategy

Staging builds (feature branches):

- Pushing to any feature branch triggers CI to build an image named `my_app:feat-branchname`.

Production builds (releases):

- Creating a tag like `v1.0.0` triggers CI to build `my_app:1.0.0` and `my-app:latest`. (See Release Workflow)

If you need manual tagging, something already went wrong upstream.

## Release Workflow

Releases are handled through cargo release to ensure version consistency across crates and tags.

### Golden Rules

- Never edit versions manually in pyproject.toml.

- Never create git tags yourself.

### How to Ship

1.  Ensure you are on the main branch with a clean working tree.

2.  Perform a dry run:

```
uv run cz bump --dry-run --increment patch
```

3.  Execute the release:

```
uv run cz bump --increment patch
```

4. Push to git

```
git push --follow-tags
```

### What Happens After

- Versions are updated and committed.

- A tag is created and pushed.

- GitHub Actions triggers the production pipeline.

- Docker images `my_app:1.1.0` and `my-app:latest` are built and published.

📘 Operational Playbook (Python Edition)

### 🧠 Part 1: Team Coordination Principles

To make this technical setup work, your team must agree on **Trunk-Based Development**.

**The 4 Golden Rules:**

1.  **Main is Sacred:** The `main` branch must _always_ pass tests and be deployable. You never push broken code to main.

2.  **Short-Lived Branches:** Feature branches (`feat/login`) should live for 1-2 days max. If a feature takes 2 weeks, break it down or use Feature Flags (Scenario E).

3.  **Immutable Artifacts:** Once a Docker image is built (e.g., `my_app:1.0.0`), it **never** changes. If you find a bug, you don't overwrite 1.0.0; you release 1.0.1.

4.  **DevOps is Everyone's Job:** Developers don't just write code; they own the release process (via `cz bump` / `commitizen`).

### 🎬 Part 2: Workflows & Scenarios

Here are the specific recipes for daily life in this repository.

#### Scenario A: The Daily Feature (Standard Dev)

_Goal: Add a new login button._

1.  **Start:** Update your local main.

    ```bash
    git checkout main && git pull
    git checkout -b feat/login-button

    ```

2.  **Develop:**
    - **Open terminal 1:** Run the watcher.

      Bash

      ```
      uv run ptw . --now --clear

      ```

    - Write code in `src/`. If the watcher turns red, fix it immediately.

    - Write a test in `tests/`.

3.  **Staging Deployment (The "Magic" Step):**
    - You want to show your Product Manager the feature, but it's not merged yet.

    - **Action:** `git push origin feat/login-button`

    - **Result:** Your CI builds `my-registry/my_app:feat-login-button`.

    - **Note:** This tag is _mutable_. If you push again in an hour, this image gets overwritten with the new code.

    - **Team:** Tell the PM: _"Deploy the image `feat-login-button` to the staging server."_

4.  **Merge:**
    - Open a Pull Request (PR).

    - CI runs `pytest`, `ruff check`, `ruff format`.

    - Team reviews.

    - **Merge to Main.**

#### Scenario B: The Release Train (Going to Production)

_Goal: We have accumulated 5 features on Main. Time to ship v1.1.0._

1.  **Preparation:**

    ```bash
    git checkout main && git pull

    ```

2.  **The Release:**
    - You don't edit files manually. You let the tool do the math.

    - _Assumption: We added features, so `commitizen` detects this is a MINOR release._

    ```bash
    # 1. Preview changes (Dry Run)
    uv run cz bump --dry-run

    # 2. Fire the laser
    uv run cz bump

    ```

3.  **The Automation Result:**
    - `pyproject.toml` updates (e.g., `1.0.0` -> `1.1.0`).

    - `CHANGELOG.md` is auto-generated with the 5 features.

    - Git tag `v1.1.0` is created and pushed.

    - **CI:** Builds `my_app:1.1.0` and `my_app:latest`.

4.  **Deploy:** Update your production Kubernetes/Docker-Compose to use `my_app:1.1.0`.

#### Scenario C: The "Alpha" Cycle (Big Risky Feature)

_Goal: We are rewriting the database layer. It will take weeks. We need to test it on servers without breaking Production._

1.  **Development Phase:**
    - Merge code to main as usual. Do **not** tag yet. Wait until you have enough changes to justify a test snapshot.

2.  **Start Cycle (First Drop):**
    - We are bumping from 1.1.0 to the next feature alpha.

    ```bash
    uv run cz bump --prerelease alpha
    # Result: v1.2.0-a0 (or similar, depending on config)

    ```

3.  **Iterate (Subsequent Drops):**
    - Fixed bugs? Ready for drop #2?

    ```bash
    uv run cz bump --prerelease alpha
    # Result: v1.2.0-a1

    ```

    - **Safety:** CI builds the image, but does **NOT** update `my_app:latest`.

4.  **Finalize (Go Gold):**
    - QA approves. Promote alpha to Stable.

    ```bash
    uv run cz bump
    # Result: v1.2.0 (Stable)

    ```

#### Scenario D: The Emergency Hotfix (Firefighting)

_Goal: Production is running v1.1.0. A critical crash is found. Main is already on v1.2.0-dev (unstable)._

1.  **Travel to the Past:**

    ```bash
    git fetch --tags
    git checkout -b hotfix/v1.1.1 v1.1.0

    ```

2.  **Fix:**
    - Apply the fix. Run `uv run pytest`.

3.  **Release the Patch:**
    - Manually force a patch increment since we are on a detached timeline.

    ```bash
    uv run cz bump --increment patch
    # Result: v1.1.1

    ```

4.  **Deploy:** Ship `my_app:1.1.1` to Prod immediately.

5.  **Reconcile (Cherry Pick):**
    - **CRITICAL:** You must fix `main` too, or the bug will come back in v1.2.0.

    ```bash
    git checkout main
    git cherry-pick <commit-hash-of-fix>
    git push

    ```

#### Scenario E: The "Long Feature" (Feature Flags)

_Goal: A massive feature that takes 3 weeks, but you don't want a 3-week-old branch (Merge Hell)._

**The Strategy:** You merge code to main _every day_, but you keep it disabled using runtime configuration.

1.  **Config (src/config.py):**

    ```python
    import os

    class Settings:
        ENABLE_NEW_BILLING: bool = os.getenv("ENABLE_NEW_BILLING", "false").lower() == "true"

    settings = Settings()

    ```

2.  **The Code:**

    ```python
    from my_app.config import settings

    def calculate_billing():
        if settings.ENABLE_NEW_BILLING:
            return _complex_new_logic()
        else:
            return _old_logic()

    ```

3.  **The Flow:**
    - You merge to `main` daily.

    - Production uses `my_app:latest`. The code is there, but the environment variable is `false` (default).

    - You test locally with: `ENABLE_NEW_BILLING=true uv run pytest`.

---

### 🛡️ Monitoring Your CI Health

With this setup, here is how to read your pipeline signals:

- **Red "Test" Job:** The code is logically broken. Check `uv run pytest` locally.

- **Red "Lint/Ruff" Job:** The code works, but violates style guides or import rules. Check `uv run ruff check`.

- **Red "Security Audit":** A dependency you use has a known vulnerability. Run `uv pip audit` (or your chosen security tool) and upgrade that library.

- **Red "Docker Build":** Usually means you added a file to the repo but forgot to update the `Dockerfile` COPY command, or the `uv sync` step failed inside the container.
