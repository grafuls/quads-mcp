# Publishing quads-mcp to PyPI

This guide walks you through publishing the QUADS MCP server to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on both [TestPyPI](https://test.pypi.org/) and [PyPI](https://pypi.org/)
2. **API Tokens**: Generate API tokens for both platforms
3. **Build Tools**: Install required build and upload tools

## Step 1: Install Publishing Tools

```bash
# Install build and upload tools
pip install --upgrade build twine

# Or using uv
uv tool install build
uv tool install twine
```

## Step 2: Configure API Tokens

### Create API Tokens

1. **TestPyPI**: Go to https://test.pypi.org/manage/account/token/
2. **PyPI**: Go to https://pypi.org/manage/account/token/

Create tokens with project scope for better security.

### Configure tokens in ~/.pypirc

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-token-here
```

## Step 3: Prepare for Publication

### Update Version

Update the version in `pyproject.toml`:

```toml
[project]
name = "quads-mcp"
version = "0.1.0"  # Update this version
```

### Verify Package Structure

```bash
# Check package structure
find quads_mcp -name "*.py" | head -10

# Verify imports work
python -c "import quads_mcp.server; print('✅ Package imports correctly')"
```

### Run Tests (if available)

```bash
# Run any tests
make test  # or pytest, if you have tests
```

## Step 4: Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build the package
python -m build

# Verify build artifacts
ls -la dist/
```

You should see:
- `quads_mcp-0.1.0.tar.gz` (source distribution)
- `quads_mcp-0.1.0-py3-none-any.whl` (wheel distribution)

## Step 5: Test on TestPyPI First

### Upload to TestPyPI

```bash
# Upload to TestPyPI for testing
twine upload --repository testpypi dist/*
```

### Test Installation from TestPyPI

```bash
# Create a test environment
python -m venv test_env
source test_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ quads-mcp

# Test the installation
quads-mcp --help
python -c "import quads_mcp.server; print('✅ Package works from TestPyPI')"

# Clean up
deactivate
rm -rf test_env
```

## Step 6: Publish to PyPI

### Final Checks

1. **Version uniqueness**: Ensure the version hasn't been published before
2. **Package name**: Verify the name is available on PyPI
3. **Dependencies**: Check all dependencies are available on PyPI

### Upload to PyPI

```bash
# Upload to real PyPI
twine upload dist/*
```

### Verify Publication

```bash
# Check the package page
open https://pypi.org/project/quads-mcp/

# Test installation from PyPI
pip install quads-mcp
```

## Step 7: Post-Publication

### Create GitHub Release

1. Go to your GitHub repository
2. Create a new release with tag `v0.1.0`
3. Add release notes describing the features

### Update Documentation

1. Add installation instructions to README.md
2. Update any version references
3. Consider adding badges for PyPI version

## Automation with GitHub Actions

You can automate publishing with GitHub Actions. Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## Troubleshooting

### Common Issues

1. **Version conflicts**: Increment version number if already published
2. **Missing dependencies**: Check all dependencies exist on PyPI
3. **Authentication errors**: Verify API tokens are correct
4. **Package name taken**: Choose a different name or contact PyPI support

### Useful Commands

```bash
# Check package metadata
twine check dist/*

# View package contents
tar -tzf dist/quads-mcp-0.1.0.tar.gz

# Test package installation locally
pip install dist/quads_mcp-0.1.0-py3-none-any.whl
```

## Security Best Practices

1. **Use API tokens** instead of username/password
2. **Scope tokens** to specific projects when possible
3. **Use TestPyPI first** to catch issues
4. **Keep tokens secure** and rotate regularly
5. **Enable 2FA** on your PyPI account

## Version Management

Consider using semantic versioning:

- **0.1.0**: Initial release
- **0.1.1**: Bug fixes
- **0.2.0**: New features (backward compatible)
- **1.0.0**: Stable release
- **2.0.0**: Breaking changes

## Next Steps

After publishing:

1. **Monitor downloads** on PyPI
2. **Handle user feedback** and issues
3. **Plan future releases** with new features
4. **Consider documentation** hosting (Read the Docs)
5. **Add CI/CD** for automated testing and publishing