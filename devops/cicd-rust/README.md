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

For single workspace projects, delete the `crates/` folder and place all structure directly in the root.

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
```

The wizard configures LTO, panic aborts, codegen units, and other flags that reduce binary size and improve runtime speed.

```
# Use cargo wizard to set optimal profiles
cargo wizard
```

### 2. Create all the configuration files

- [rust-toolchain.toml](rust-toolchain.toml)
- [release.toml](release.toml)
- [bacon.toml](bacon.toml)
- [cliff.toml](cliff.toml)
- [clippy.toml](clippy.toml) - (Optional)
- [Cargo.toml](Cargo.toml) - (Optional) Example of a workspace setup

### 3. Live Development Loop with Bacon

Bacon gives you near instant feedback while editing. It watches the workspace, compiles incrementally, and reports issues without waiting for a manual test run.

```
bacon
```

### 4. Pre Push Checklist

Before pushing to any feature branch, confirm that the CI pipeline will not burst into flames.

```
cargo nextest run
cargo fmt
cargo clippy -- -D warnings
```

## CI and Caching

- [Example Dockerfile](docker/)
- [Example CI Github Actions](github/)

GitHub Actions uses swatinem/rust cache to avoid unnecessary recompilation. The cache key is derived from Cargo.lock. If dependencies remain unchanged, CI restores binaries directly from cache.

No configuration is needed on your side. Every push to every branch benefits from the cache.

### Docker Build Strategy

Staging builds (feature branches):

- Pushing to any feature branch triggers CI to build an image named `my-app:feat-branchname`.

Production builds (releases):

- Creating a tag like `v1.0.0` triggers CI to build `my-app:1.0.0` and `my-app:latest`. (See Release Workflow)

If you need manual tagging, something already went wrong upstream.

## Release Workflow

Releases are handled through cargo release to ensure version consistency across crates and tags.

### Golden Rules

- Never edit versions manually in Cargo.toml.

- Never create git tags yourself.

### How to Ship

1.  Ensure you are on the main branch with a clean working tree.

2.  Perform a dry run:

```
cargo release 1.1.0
```

3.  Execute the release:

```
cargo release 1.1.0 --execute
```

### What Happens After

- Versions are updated and committed.

- A tag is created and pushed.

- GitHub Actions triggers the production pipeline.

- Docker images `my-app:1.1.0` and `my-app:latest` are built and published.
