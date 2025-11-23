# === Stage 1: Planner ===
FROM lukemathwalker/cargo-chef:latest-rust-1 AS planner
WORKDIR /app
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

# === Stage 2: Cacher ===
FROM lukemathwalker/cargo-chef:latest-rust-1 AS cacher
WORKDIR /app
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json

# === Stage 3: Builder ===
FROM lukemathwalker/cargo-chef:latest-rust-1 AS builder
WORKDIR /app
COPY . .
COPY --from=cacher /app/target target
COPY --from=cacher /app/recipe.json recipe.json

RUN cargo build --release

# --- THE MAGIC PART ---
# 1. Parse the project name from Cargo.toml
# 2. Find that binary in target/release
# 3. Copy it to a generic name "server"
RUN PROJECT_NAME=$(sed -n 's/^name = "\(.*\)"/\1/p' Cargo.toml | head -n1) && \
    cp target/release/$PROJECT_NAME /bin/server

# === Stage 4: Runtime ===
FROM debian:bookworm-slim
WORKDIR /app

# Now we just copy "server" - we don't care what the original name was
COPY --from=builder /bin/server /usr/local/bin/server

ENTRYPOINT ["/usr/local/bin/server"]
