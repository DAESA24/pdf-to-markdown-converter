<!-- Powered by BMAD™ Core -->

# UV Package Manager Workflow Guide

## Overview

UV is the preferred Python package manager for all BMAD projects due to its exceptional performance (10-100x faster than pip) and VS Code compatibility. This guide provides standardized workflows for BMAD AI agents and human developers.

## Project Initialization

### New Python Projects
```bash
# Initialize new UV project
uv init project-name

# Navigate to project
cd project-name

# Project structure created:
# ├── .git/
# ├── .gitignore
# ├── .python-version
# ├── README.md
# ├── main.py
# └── pyproject.toml
```

### Existing Projects (Migration)
```bash
# For existing projects with requirements.txt
uv add -r requirements.txt

# For existing projects with pyproject.toml
uv sync
```

## Package Management Commands

### Adding Dependencies
```bash
# Add production dependency
uv add requests

# Add development dependency
uv add --dev pytest

# Add with version specification
uv add "django>=4.0,<5.0"

# Add from specific index
uv add --index-url https://custom-index.com package-name
```

### Removing Dependencies
```bash
# Remove package
uv remove requests

# Remove development dependency
uv remove --dev pytest
```

### Environment Management
```bash
# Create/sync virtual environment
uv sync

# Install all dependencies (production + dev)
uv sync --all-extras

# Install only production dependencies
uv sync --no-dev
```

## Code Execution

### Running Scripts
```bash
# Run Python scripts in project environment
uv run python main.py

# Run specific module
uv run python -m pytest

# Run with environment variables
uv run --env-file .env python main.py
```

### Interactive Development
```bash
# Start Python REPL in project environment
uv run python

# Run Jupyter notebook (if installed)
uv run jupyter notebook
```

## VS Code Integration

### Environment Detection
- UV creates standard `.venv` directories
- VS Code automatically detects UV-managed interpreters
- Select interpreter: `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (Linux/Mac)

### Terminal Integration
- VS Code terminal shows `(project-name)` instead of `(.venv)`
- Use `uv run` commands instead of traditional venv activation
- IntelliSense and debugging work seamlessly

### Debugging Setup
1. VS Code detects UV interpreter automatically
2. Set breakpoints normally
3. Use F5 or Run/Debug configuration
4. All installed packages available for import

## BMAD Agent Guidelines

### For Development Agents
```bash
# Always use UV for Python projects
uv add package-name

# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Format code
uv run black .
```

### For Architecture Agents
- Include UV in Technology Stack table
- Version: Current stable (e.g., 0.8.19)
- Rationale: "10-100x faster than pip, universal lockfiles, VS Code compatible"
- Category: Package Manager

### For QA Agents
```bash
# Install test dependencies
uv add --dev pytest pytest-cov

# Run test suite
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

## Legacy Compatibility

### Pip-Compatible Commands
```bash
# When pip compatibility needed
uv pip install package-name
uv pip list
uv pip freeze > requirements.txt
uv pip install -r requirements.txt
```

### Team Integration
- UV coexists with pip (no conflicts)
- CI/CD systems can use `uv pip` commands
- Gradual team migration supported

## Docker Integration

### Dockerfile with UV
```dockerfile
FROM python:3.12-slim

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Run application
CMD ["uv", "run", "python", "main.py"]
```

## Troubleshooting

### Common Issues

**Issue**: VS Code doesn't detect UV environment
**Solution**:
1. Restart VS Code
2. Command Palette → "Python: Select Interpreter"
3. Choose `.venv/Scripts/python.exe`

**Issue**: Import errors in VS Code
**Solution**:
1. Ensure packages installed: `uv sync`
2. Restart Python language server: Command Palette → "Python: Restart Language Server"

**Issue**: UV command not found
**Solution**:
1. Restart terminal/VS Code
2. Check PATH: `echo $PATH` (should include UV directory)
3. Reinstall UV if needed

### Rollback Strategy
```bash
# Export UV dependencies to pip format
uv pip freeze > requirements.txt

# Install with pip if needed
pip install -r requirements.txt
```

## Performance Benefits

- **Package Installation**: 10-100x faster than pip
- **Dependency Resolution**: Parallel processing, advanced algorithms
- **Lock Files**: Universal format, deterministic builds
- **Disk Usage**: Global cache, reduced redundancy
- **Cold Start**: Faster environment creation

## Best Practices

1. **Always use UV for new Python projects**
2. **Pin UV version in CI/CD**: Use specific UV version for reproducibility
3. **Commit lock files**: Include `uv.lock` in version control
4. **Use uv run**: Prefer `uv run` over manual venv activation
5. **Regular updates**: Keep UV updated for latest performance improvements

---

*This guide is maintained as part of BMAD Core and should be referenced by all AI agents working on Python projects.*