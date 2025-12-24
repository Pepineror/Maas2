FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

WORKDIR /app

# Copy configuration files
COPY pyproject.toml .
# If we have a lockfile, copy it too
# COPY uv.lock .

# Install dependencies
RUN uv pip install --system .

# Copy backend code
COPY backend/ /app/backend/
COPY backend/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

EXPOSE 8000

CMD ["/app/start.sh"]
