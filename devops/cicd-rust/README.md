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

### 2. Create config files and set up git and versioning

- [rust-toolchain.toml](rust-toolchain.toml)
- [release.toml](release.toml)
- [bacon.toml](bacon.toml)
- [cliff.toml](cliff.toml)
- [clippy.toml](clippy.toml) - (Optional)
- [Cargo.toml](Cargo.toml) - (Optional) Example of a workspace setup

> [!NOTE]
> Create an initial git commit and set up the upstream git repository here. Consider adding a license.

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

Make sure you have set up Dockerfile and CI pipeline. This section will assume you are using the examples provided below.

- [Example Dockerfile](docker/)
- [Example CI Github Actions](github/)

GitHub Actions uses swatinem/rust cache to avoid unnecessary recompilation. The cache key is derived from Cargo.lock. If dependencies remain unchanged, CI restores binaries directly from cache.

No configuration is needed on your side. Every push to every branch benefits from the cache.

> [!NOTE]
> Go through the docker and CI files to double check the content. Make sure all CI secrets are set up.

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
cargo release 0.1.0
```

3.  Execute the release:

```
cargo release 0.1.0 --execute
```

### What Happens After

- Versions are updated and committed.

- A tag is created and pushed.

- GitHub Actions triggers the production pipeline.

- Docker images `my-app:1.1.0` and `my-app:latest` are built and published.

## 📘 Operational Playbook

### 🧠 Part 1: Team Coordination Principles

To make this technical setup work, your team must agree on **Trunk-Based Development**.

**The 4 Golden Rules:**

1. **Main is Sacred:** The main branch must *always* be compile-able and deployable. You never push broken code to main.
2. **Short-Lived Branches:** Feature branches (feat/login) should live for 1-2 days max. If a feature takes 2 weeks, break it down or use Feature Flags (Scenario E).
3. **Immutable Artifacts:** Once a Docker image is built (e.g., my-app:1.0.0), it **never** changes. If you find a bug, you don't overwrite 1.0.0; you release 1.0.1.
4. **DevOps is Everyone's Job:** Developers don't just write code; they own the release process (via cargo release).

### 🎬 Part 2: Workflows & Scenarios

Here are the specific recipes for daily life in this repository.

#### Scenario A: The Daily Feature (Standard Dev)

*Goal: Add a new login button.*

1. **Start:** Update your local main.

    ```bash
    git checkout main && git pull
    git checkout -b feat/login-button
    ```

2. **Develop:**
    * Open terminal 1: Run cargo bacon (it watches your code).
    * Write code. If Bacon turns red, fix it immediately.
    * Write a test in src/lib.rs or tests/.

3. **Staging Deployment (The "Magic" Step):**
    * You want to show your Product Manager the button, but it's not merged yet.
    * **Action:** git push origin feat/login-button
    * **Result:** Your CI builds my-registry/my-app:feat-login-button.
    * **Note:** This tag is *mutable*. If you push again in an hour, this image gets overwritten with the new code.
    * **Team:** Tell the PM: *"Deploy the image feat-login-button to the staging server."*

4. **Merge:**
    * Open a Pull Request (PR).
    * CI runs nextest, clippy, fmt.
    * Team reviews.
    * **Merge to Main.**

#### Scenario B: The Release Train (Going to Production)

*Goal: We have accumulated 5 features on Main. Time to ship v1.1.0.*

1. **Preparation:**

    ```bash
    git checkout main && git pull
    ```

2. **The Release:**
    * You don't edit files manually. You let the tool do the math.
    * *Assumption: We added features, so this is a Minor release.*

    ```bash
    # 1. Check what will happen (Dry Run)
    cargo release minor

    # 2. Fire the laser
    cargo release minor --execute
    ```

3. **The Automation Result:**
    * Cargo.toml updates (e.g., 1.0.0 -> 1.1.0).
    * CHANGELOG.md is auto-generated with the 5 features.
    * Git tag v1.1.0 is pushed.
    * **CI:** Builds my-app:1.1.0 and my-app:latest.

4. **Deploy:** Update your production Kubernetes/Docker-Compose to use my-app:1.1.0.

#### Scenario C: The "Alpha" Cycle (Big Risky Feature)

*Goal: We are rewriting the database layer. It will take weeks. We need to test it on servers without breaking Production.*

1. **Development Phase:**
    * Merge code to main as usual. Do **not** tag yet. Wait until you have enough changes to justify a test snapshot.

2. **Start Cycle (First Drop):**
    * We are bumping from 1.1.0 to the next feature alpha.

    ```bash
    cargo release minor alpha --execute
    # Result: v1.2.0-alpha.1
    ```


3. **Iterate (Subsequent Drops):**
    * Fixed bugs? Ready for drop #2?

    ```bash
    cargo release alpha --execute
    # Result: v1.2.0-alpha.2
    ```

    * **Safety:** CI builds the image, but does **NOT** update my-app:latest.

4. **Finalize (Go Gold):**
    * QA approves. Promote alpha to Stable.

    ```bash
    cargo release release --execute
    # Result: v1.2.0 (Stable)
    ```

#### Scenario D: The Emergency Hotfix (Firefighting)

*Goal: Production is running v1.1.0. A critical crash is found. Main is already on v1.2.0-dev (unstable).*

1. **Travel to the Past:**

    ```bash
    git fetch --tags
    git checkout -b hotfix/v1.1.1 v1.1.0
    ```

2. **Fix:**
    * Apply the fix. Run cargo nextest.

3. **Release the Patch:**
    * Because we updated release.toml, hotfix branches are allowed.

    ```bash
    cargo release patch --execute
    # Result: v1.1.1
    ```

4. **Deploy:** Ship my-app:1.1.1 to Prod immediately.

5. **Reconcile (Cherry Pick):**
    * **CRITICAL:** You must fix main too, or the bug will come back in v1.2.0.

    ```bash
    git checkout main
    git cherry-pick &lt;commit-hash-of-fix>
    git push
    ```

#### Scenario E: The "Long Feature" (Feature Flags)

*Goal: A massive feature that takes 3 weeks, but you don't want a 3-week-old branch (Merge Hell).*

**The Strategy:** You merge code to main *every day*, but you keep it disabled.

1. **Cargo.toml:**

    ``` TOML
    [features]
    default = []
    new_billing_system = [] # The flag
    ```

2. **The Code:**

    ```Rust
    #[cfg(feature = "new_billing_system")]
    fn calculate_billing() {
       // New complex logic
    }
    ```

3. **The Flow:**
    * You merge to main daily.
    * Production uses my-app:latest (default features). The code is there, but compiled out or disabled.
    * You test locally with: cargo run --features new_billing_system.

### 🛡️ Monitoring Your CI Health

With this setup, here is how to read your pipeline signals:

* **Red "Test" Job:** The code is logically broken. Check cargo nextest locally.
* **Red "Lint/Clippy" Job:** The code works, but looks messy or unsafe. Check cargo clippy.
* **Red "Security Audit":** A dependency you use has a known vulnerability. Run cargo audit locally and upgrade that library.
* **Red "Docker Build":** Usually means you added a file to the repo but forgot to update the Dockerfile COPY command, or the cargo-chef recipe failed.

### 💡 Cargo Release Cheatsheet

<table>
  <tr>
   <td><strong>Current Ver</strong>
   </td>
   <td><strong>Command</strong>
   </td>
   <td><strong>New Ver</strong>
   </td>
   <td><strong>Context</strong>
   </td>
  </tr>
  <tr>
   <td><strong>1.0.0</strong>
   </td>
   <td>cargo release patch
   </td>
   <td><strong>1.0.1</strong>
   </td>
   <td>Standard bug fix
   </td>
  </tr>
  <tr>
   <td><strong>1.0.0</strong>
   </td>
   <td>cargo release minor
   </td>
   <td><strong>1.1.0</strong>
   </td>
   <td>New features added
   </td>
  </tr>
  <tr>
   <td><strong>1.0.0</strong>
   </td>
   <td>cargo release minor alpha
   </td>
   <td><strong>1.1.0-alpha.1</strong>
   </td>
   <td>Start a new Alpha cycle
   </td>
  </tr>
  <tr>
   <td><strong>1.1.0-alpha.1</strong>
   </td>
   <td>cargo release alpha
   </td>
   <td><strong>1.1.0-alpha.2</strong>
   </td>
   <td>Next alpha drop
   </td>
  </tr>
  <tr>
   <td><strong>1.1.0-alpha.2</strong>
   </td>
   <td>cargo release release
   </td>
   <td><strong>1.1.0</strong>
   </td>
   <td>Promote Alpha to Stable
   </td>
  </tr>
</table>

