# === Stage 1: Builder  ===
FROM python:3.12-slim-bookworm AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# 1. Copy ONLY dependency files to cache this layer
COPY pyproject.toml uv.lock ./

# 2. Install dependencies into a virtual environment
# --frozen ensures we strictly use the lockfile
RUN uv sync --frozen --no-install-project --no-dev

# === Stage 2: Runtime ===
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Copy the actual source code (This layer changes most often)
COPY src/ ./src

# Add venv to PATH so we can run "python" or "uvicorn" directly
ENV PATH="/app/.venv/bin:$PATH"

# Entrypoint
CMD ["uvicorn", "src.my_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
