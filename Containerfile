# Use Python 3.12 Alpine image for better security and smaller size
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies and security updates
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    && apk upgrade \
    && rm -rf /var/cache/apk/*

# Copy project files
COPY pyproject.toml ./
COPY README.md ./
COPY quads_mcp/ ./quads_mcp/

# Install uv for faster dependency management
RUN pip install uv

# Install project dependencies
RUN uv pip install --system -e .

# Create non-root user for security
RUN addgroup -g 1001 -S mcp && \
    adduser -u 1001 -S mcp -G mcp
RUN chown -R mcp:mcp /app
USER mcp

# Expose port (if needed for HTTP serving)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from quads_mcp.server import mcp; print('Server OK')" || exit 1

# Default command
CMD ["python", "-m", "quads_mcp.server"]