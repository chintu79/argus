FROM python:3.11-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
WORKDIR /home/app

# Install uv
COPY --from=astral/uv:0.4.0 /usr/local/bin/uv /usr/local/bin/uv

# Copy requirements first for caching
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev --group dev 2>/dev/null || true
RUN uv sync --frozen 2>/dev/null

# Copy source code
COPY src/ ./src/
COPY configs/ ./configs/
COPY data/ ./data/
COPY artifacts/ ./artifacts/
COPY migrations/ ./migrations/
COPY tests/ ./tests/
COPY notebooks/ ./notebooks/
COPY scripts/ ./scripts/

# Expose port for API
EXPOSE 8000

# Default command
ENTRYPOINT ["uv", "run"]
CMD ["python", "-m", "agent_eval.cli", "validate", "--config", "configs/test.yaml"]