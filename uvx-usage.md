# Running QUADS MCP Server with uvx

The QUADS MCP server can be run using `uvx`, which allows you to run Python applications in isolated environments without manual virtual environment management.

## Prerequisites

Make sure you have `uv` installed:

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

## Running with uvx

### Option 1: Run from Local Directory

From the project root directory:

```bash
# Run the server directly
uvx --from . quads-mcp

# Or run the module
uvx --from . python -m quads_mcp.server
```

### Option 2: Run from Git Repository

You can run directly from the Git repository without cloning:

```bash
# Run from GitHub (replace with actual repository URL)
uvx --from git+https://github.com/user/quads-mcp.git quads-mcp

# Run specific branch or tag
uvx --from git+https://github.com/user/quads-mcp.git@main quads-mcp
```

### Option 3: Run with Custom Configuration

Set environment variables for configuration:

```bash
# Set QUADS API configuration
export MCP_QUADS__BASE_URL="https://your-quads-api.com/api/v3"
export MCP_QUADS__AUTH_TOKEN="your-auth-token"

# Run the server
uvx --from . quads-mcp
```

### Option 4: Run with .env File

```bash
# Create .env file with your configuration
cp .env.example .env
# Edit .env with your values

# Run the server (it will automatically load .env)
uvx --from . quads-mcp
```

## Development Mode

For development with MCP inspector:

```bash
# Install mcp if not already available
uvx install mcp

# Run in development mode
uvx mcp dev quads_mcp.server
```

## Installing as a Global Tool

If you want to install the tool globally:

```bash
# Install from local directory
uvx install .

# Now you can run it from anywhere
quads-mcp

# Uninstall when done
uvx uninstall quads-mcp
```

## Advantages of uvx

1. **Isolated Environment**: Each run gets its own isolated environment
2. **No Global Installation**: Doesn't pollute your global Python environment
3. **Automatic Dependencies**: Handles all dependencies automatically
4. **Version Management**: Can run different versions side by side
5. **Fast Execution**: Caches environments for faster subsequent runs

## Troubleshooting

### Permission Issues
```bash
# If you get permission errors, ensure uv has proper permissions
uvx --from . quads-mcp --verbose
```

### Configuration Issues
```bash
# Check if environment variables are set
uvx --from . python -c "import os; print('QUADS URL:', os.environ.get('MCP_QUADS__BASE_URL', 'Not set'))"
```

### Dependency Issues
```bash
# Force reinstall dependencies
uvx --from . --reinstall quads-mcp
```

## Examples

### Basic Usage
```bash
# Run with default configuration
uvx --from . quads-mcp
```

### With Custom Configuration
```bash
# Run with specific QUADS API settings
MCP_QUADS__BASE_URL="https://quads.example.com/api/v3" \
MCP_QUADS__AUTH_TOKEN="your-token" \
uvx --from . quads-mcp
```

### Development Mode
```bash
# Run with debug logging
MCP_DEBUG=true uvx --from . quads-mcp
```

This approach provides a clean, isolated way to run the QUADS MCP server without manual environment management!