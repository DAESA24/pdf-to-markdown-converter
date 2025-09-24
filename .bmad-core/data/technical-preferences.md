<!-- Powered by BMAD™ Core -->

# User-Defined Preferred Patterns and Preferences

## Python Package Management

**Preferred Tool:** UV (uv) - Extremely fast Python package and project manager
- **Installation:** Use `uv init` for new projects
- **Package Management:** Use `uv add <package>` instead of `pip install`
- **Environment Management:** UV creates standard `.venv` environments compatible with VS Code
- **Execution:** Use `uv run <command>` for running scripts in project environment
- **Legacy Compatibility:** Use `uv pip <command>` for pip-compatible operations when needed

**Fallback Options:** pip, poetry (for projects where UV is not suitable)

**VS Code Integration:** UV works seamlessly with existing Python VS Code extensions
- Interpreter detection works automatically
- IntelliSense and debugging fully functional
- Terminal integration uses `uv run` workflow instead of traditional venv activation

## Package Management Philosophy

**Performance Priority:** Choose UV for Python projects due to 10-100x speed improvement over traditional tools

**Compatibility Assurance:** UV maintains pip compatibility via `uv pip` commands for team members or CI/CD systems not yet using UV

**Multi-Machine Workflow:** UV's universal lockfiles ensure consistent dependencies across development machines
