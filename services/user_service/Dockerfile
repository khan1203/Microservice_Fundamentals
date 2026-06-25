#-----------------------------------------
# Stage-01: The Builder
#-----------------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_HTTP_TIMEOUT=120
WORKDIR /app

# Copy the dependency files first for docker caching
COPY pyproject.toml uv.lock ./

# Copy the specific services files
COPY services/user_service/pyproject.toml services/user_service/

# Install dependencies for the user-service
RUN uv sync --package user_service --frozen --no-dev

# Copy rest of the code
COPY . .

#-----------------------------------------
# Stage-02: The Final Image
#-----------------------------------------
FROM python:3.12-slim-bookworm
WORKDIR /app

# Copy the environment and code from the builder
COPY --from=builder /app /app

# Put the virtual environment on the path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/services/user-service:/app"

# Run the FastAPI server.
CMD ["fastapi", "run", "services/user_service/main.py", "--port", "8000", "--host", "0.0.0.0"]