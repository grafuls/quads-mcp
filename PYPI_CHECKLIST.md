# PyPI Publication Checklist

Use this checklist before publishing to PyPI.

## ✅ Pre-Publication Checklist

### Package Structure
- [x] **Package structure**: Proper Python package with `__init__.py` files
- [x] **pyproject.toml**: Complete with all required metadata
- [x] **README.md**: Comprehensive documentation
- [x] **LICENSE**: MIT license file included
- [x] **MANIFEST.in**: Includes all necessary files
- [x] **Console scripts**: Entry point configured (`quads-mcp = "quads_mcp.server:main"`)

### Metadata
- [x] **Package name**: `quads-mcp` (available on PyPI)
- [x] **Version**: `0.1.0` (semantic versioning)
- [x] **Description**: Clear and descriptive
- [x] **Author**: Contact information included
- [x] **License**: MIT license specified
- [x] **Python version**: `>=3.12` requirement
- [x] **Dependencies**: All required packages listed
- [x] **Keywords**: Relevant search terms
- [x] **Classifiers**: Appropriate PyPI classifiers
- [x] **Project URLs**: Repository, bug tracker, documentation

### Code Quality
- [x] **Imports work**: All modules import correctly
- [x] **Console script**: `quads-mcp` command works
- [x] **No test files**: Test files excluded from distribution
- [x] **No secrets**: No `.env` or credential files included
- [x] **Documentation**: All features documented

### Build & Test
- [x] **Build successful**: `python -m build` completes without errors
- [x] **Twine check**: `twine check dist/*` passes
- [x] **Local install**: Package installs from wheel
- [x] **Import test**: Package imports work after installation

## 📋 Publication Steps

### 1. Prepare for Publication

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build the package
python -m build

# Validate the package
twine check dist/*
```

### 2. Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ quads-mcp
```

### 3. Publish to PyPI

```bash
# Upload to PyPI
twine upload dist/*
```

### 4. Verify Publication

```bash
# Check package page
open https://pypi.org/project/quads-mcp/

# Test installation
pip install quads-mcp
quads-mcp --version
```

## 🔧 Configuration Requirements

### PyPI Account Setup
- [ ] PyPI account created
- [ ] TestPyPI account created  
- [ ] API tokens generated
- [ ] `~/.pypirc` configured

### Local Environment
- [ ] `build` package installed
- [ ] `twine` package installed
- [ ] Git repository clean
- [ ] All changes committed

## 🚀 Post-Publication

### GitHub Release
- [ ] Create GitHub release with tag `v0.1.0`
- [ ] Add release notes
- [ ] Link to PyPI package

### Documentation Updates
- [ ] Update README with PyPI installation instructions
- [ ] Add PyPI badge to README
- [ ] Update Claude Desktop configuration examples

### Monitoring
- [ ] Monitor PyPI package page for downloads
- [ ] Watch for user issues and feedback
- [ ] Plan next release with new features

## 📦 Package Information

- **Package Name**: `quads-mcp`
- **Version**: `0.1.0`
- **PyPI URL**: https://pypi.org/project/quads-mcp/
- **Repository**: https://github.com/grafuls/quads-mcp
- **License**: MIT
- **Python**: >=3.12

## 🔍 Common Issues

### Version Conflicts
- If version already exists on PyPI, increment version number
- Use semantic versioning: `MAJOR.MINOR.PATCH`

### Dependency Issues
- Ensure all dependencies are available on PyPI
- Test installation in clean environment

### Authentication Errors
- Verify API tokens are correct
- Check ~/.pypirc configuration
- Ensure 2FA is properly configured

### Build Errors
- Check pyproject.toml syntax
- Verify all files are included in MANIFEST.in
- Test build in clean environment

## 🛡️ Security Checklist

- [x] **No secrets**: No credentials in code or config files
- [x] **Secure dependencies**: All dependencies from trusted sources
- [x] **License compliance**: All code properly licensed
- [x] **API tokens**: Secure storage of PyPI API tokens
- [x] **2FA enabled**: Two-factor authentication on PyPI account