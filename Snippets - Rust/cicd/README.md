Engineering Manual and Workflow
===============================

This document defines the project structure, required tools, and the full development-to-release pipeline for this repository. The goal is to keep builds fast, code clean, and releases predictable instead of chaotic.

Project Structure and Best Practices
------------------------------------

We use a workspace pattern (monorepo) to isolate business logic from executable binaries. This keeps compilation efficient and avoids dragging unrelated crates into your build graph.

### Tooling Requirements

The following tools must be installed locally:

-   rustup: manages Rust toolchains

-   bacon: live background compiler and test runner

-   cargo nextest: high performance test executor

-   cargo release: automated versioning and tagging

-   cargo wizard: applies optimized Cargo profiles

### Repository Layout
```
`.
├── Cargo.toml              # Workspace root and member definitions
├── bacon.toml              # Bacon configuration, wired for nextest
├── rust-toolchain.toml     # Pinned Rust toolchain
├── release.toml            # Release automation rules
├── crates/                 # All first party code
│   ├── my-app-core/        # Library crate: domain logic, DB access, models
│   │   └── src/
│   │       ├── lib.rs
│   │       └── prelude.rs  # Re-export pattern for ergonomic imports
│   └── my-app-server/      # Binary crate: server CLI or HTTP runtime
│       └── src/
│           └── main.rs     # Thin entrypoint that delegates to core`
```
### Structural Principles

-   Core business logic always lives inside a library crate.

-   Binary crates must stay thin. They should parse config, initialize runtime, and call into core.

-   Shared types, utilities, and DB layers belong inside core.

-   Never put domain logic in the binary. That path only leads to sadness.

Development Workflow
--------------------

### 1\. Initializing a New Workspace

Create a workspace and immediately apply performance optimizations so you do not suffer slow compiles later.

```
cargo new my-app
cargo wizard apply    # Choose "Production" when prompted
```

The wizard configures LTO, panic aborts, codegen units, and other flags that reduce binary size and improve runtime speed.

### 2\. Live Development Loop with Bacon

Bacon gives you near instant feedback while editing. It watches the workspace, compiles incrementally, and reports issues without waiting for a manual test run.

```
bacon nextest
```

If bacon turns red, fix your crimes before committing more.

### 3\. Pre Push Checklist

Before pushing to any feature branch (feat/*), confirm that the CI pipeline will not burst into flames.

```
cargo fmt
cargo clippy -- -D warnings
cargo nextest run
```

If clippy finds a problem, assume it is right. It usually is.

CI and Caching
--------------

GitHub Actions uses swatinem/rust cache to avoid unnecessary recompilation. The cache key is derived from Cargo.lock. If dependencies remain unchanged, CI restores binaries directly from cache.

No configuration is needed on your side. Every push to every branch benefits from the cache.

### Docker Build Strategy

Staging builds (feature branches):

-   Pushing to any feat/* branch triggers CI to build an image named `my-app:feat-branchname`.

Production builds (releases):

-   Creating a tag like `v1.0.0` triggers CI to build `my-app:1.0.0` and `my-app:latest`.

If you need manual tagging, something already went wrong upstream.

Release Workflow
----------------

Releases are handled through cargo release to ensure version consistency across crates and tags.

### Golden Rules

-   Never edit versions manually in Cargo.toml.

-   Never create git tags yourself.

-   Never try to outsmart cargo release. You will lose.

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

-   Versions are incremented and committed.

-   A tag is created and pushed.

-   GitHub Actions triggers the production pipeline.

-   Docker images `my-app:1.1.0` and `my-app:latest` are built and published.

Configuration File Templates
----------------------------

This section provides reference templates for the core configuration files used in the workspace. Copy these into new projects to ensure consistent builds, releases, and toolchain behavior across the organization.

### release.toml

```
# Config for cargo release
allow-branch = ["main", "master"]
sign-commit = false
sign-tag = false
push = true
publish = false

pre-release-commit-message = "chore: release version {{version}}"
tag-message = "chore: release version {{version}}"
```

### rust-toolchain.toml

```[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
```

### Cargo.toml (Workspace Root)

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

### bacon.toml

```
# Use nextest for fast and reliable test feedback
default_job = "nextest"

[jobs.nextest]
command = ["cargo", "nextest", "run"]
need_stdout = false
watch = ["."]
```

### .cargo/config.toml

```
[build]
target-dir = "target"

[profile.dev]
debug = true
incremental = true

[profile.release]
lto = "fat"
codegen-units = 1
panic = "abort"
strip = true
```

### clippy.toml

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

### Nextest config (optional)

```
# .config/nextest.toml
[profile.default]
status-level = "fail"
final-status-level = "fail"
```

