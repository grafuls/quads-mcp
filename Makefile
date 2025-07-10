.PHONY: setup run dev install deploy test clean format type-check check-venv status reinstall container-build container-run compose-up compose-down

# Set the Python version from cookiecutter or default to 3.10
PYTHON_VERSION := 3.10

# Virtual environment paths
VENV_DIR := .venv
VENV_BIN := $(VENV_DIR)/bin
PYTHON := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip

# Check if we're in a virtual environment, if not use the local one
ifeq ($(VIRTUAL_ENV),)
    PYTHON_CMD := $(PYTHON)
    PIP_CMD := $(PIP)
else
    PYTHON_CMD := python
    PIP_CMD := pip
endif

# Check if virtual environment exists
check-venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "❌ Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi

# Show virtual environment status
status:
	@echo "Virtual Environment Status:"
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "✅ Virtual environment exists at $(VENV_DIR)"; \
		echo "📍 Python: $(PYTHON_CMD)"; \
		if [ -f "$(PYTHON)" ]; then \
			echo "🐍 Version: $$($(PYTHON) --version)"; \
		fi; \
	else \
		echo "❌ Virtual environment not found"; \
		echo "💡 Run 'make setup' to create it"; \
	fi

# Setup with uv
setup:
	# Check if uv is installed, install if not
	@which uv >/dev/null || pip install uv
	# Create a virtual environment
	uv venv
	# Install dependencies with development extras using uv
	uv pip install -e ".[dev]"
	@echo "✅ Environment setup complete. You can now run 'make run' to start the server."

# Reinstall package in development mode (useful after code changes)
reinstall: check-venv
	uv pip install -e ".[dev]"
	@echo "✅ Package reinstalled in development mode."

# Run the server directly
run: check-venv
	$(PYTHON_CMD) -m quads_mcp.server

# Run in development mode with MCP inspector
dev: check-venv
	$(VENV_BIN)/mcp dev quads_mcp.server

# Install in Claude Desktop
install: check-venv
	$(VENV_BIN)/mcp install quads_mcp.server

# Run tests
test: check-venv
	$(VENV_BIN)/pytest

# Format code with black and isort
format: check-venv
	$(VENV_BIN)/black quads_mcp
	$(VENV_BIN)/isort quads_mcp

# Check types with mypy
type-check: check-venv
	$(VENV_BIN)/mypy quads_mcp

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