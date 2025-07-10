.PHONY: setup run dev install deploy test clean format type-check container-build container-run compose-up compose-down

# Set the Python version from cookiecutter or default to 3.10
PYTHON_VERSION := 3.10

# Setup with uv
setup:
	# Check if uv is installed, install if not
	@which uv >/dev/null || pip install uv
	# Create a virtual environment
	uv venv
	# Install dependencies with development extras
	uv pip install -e ".[dev]"
	@echo "✅ Environment setup complete. Activate it with 'source .venv/bin/activate' (Unix/macOS) or '.venv\\Scripts\activate' (Windows)"

# Run the server directly
run:
	python -m quads_mcp.server

# Run in development mode with MCP inspector
dev:
	mcp dev quads_mcp.server

# Install in Claude Desktop
install:
	mcp install quads_mcp.server

# Run tests
test:
	pytest

# Format code with black and isort
format:
	black quads_mcp
	isort quads_mcp

# Check types with mypy
type-check:
	mypy quads_mcp

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Container build with Podman
container-build:
	podman build -t quads-mcp:latest .

# Build production image with multi-stage Containerfile
container-build-prod:
	podman build -f Containerfile.multistage -t quads-mcp:production .

# Build ultra-secure image with distroless base
container-build-distroless:
	podman build -f Containerfile.distroless -t quads-mcp:distroless .

# Run with Podman
container-run:
	podman run -p 8000:8000 quads-mcp:latest

# Run production image
container-run-prod:
	podman run -p 8000:8000 quads-mcp:production

# Run distroless image
container-run-distroless:
	podman run -p 8000:8000 quads-mcp:distroless

# Podman Compose commands
compose-up:
	podman-compose up -d

compose-down:
	podman-compose down

compose-logs:
	podman-compose logs -f

# Development with Podman Compose
compose-dev:
	podman-compose --profile dev up -d quads-mcp-dev