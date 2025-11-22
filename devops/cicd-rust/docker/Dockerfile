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
FROM rust:1-slim-bookworm AS builder
WORKDIR /app
COPY . .
COPY --from=cacher /app/target target
RUN cargo build --release

# === Stage 4: Runtime ===
FROM debian:bookworm-slim
COPY --from=builder /app/target/release/my-app /usr/local/bin/my-app
ENTRYPOINT ["/usr/local/bin/my-app"]
