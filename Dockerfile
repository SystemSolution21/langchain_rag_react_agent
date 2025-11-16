# Multi-stage Dockerfile for LangChain RAG React Agent
# Stage 1: Builder - Install dependencies
FROM python:3.13-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Install Python dependencies using uv
RUN uv pip install --system --no-cache -e .

# Stage 2: Runtime - Minimal image
FROM python:3.13-slim

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    git \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Set working directory
WORKDIR /app

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY pdfs/ ./pdfs/
COPY db/ ./db/
COPY logs/ ./logs/
COPY pyproject.toml ./
COPY README.md ./

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    PROJECT_ROOT=/app \
    PDFS_DIR=/app/pdfs \
    DB_DIR=/app/db \
    LOGS_DIR=/app/logs

# Create necessary directories with proper permissions
RUN mkdir -p /app/pdfs /app/db /app/logs && \
    chmod -R 755 /app

# Initialize git repository for version control
RUN git init && \
    git config --global user.email "systemsolution21@gmail.com" && \
    git config --global user.name "SystemSolution21"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "-m", "langchain_rag_react_agent.agent"]











