# Development Best Practices

## Branch Naming Convention
- `feature/` - New features (e.g., `feature/grammar-validation`)
- `bugfix/` - Bug fixes (e.g., `bugfix/ocr-page-range`)
- `hotfix/` - Urgent production fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

## Workflow (Git Flow)
1. **Main Branch** - Production-ready code
2. **Feature Branches** - Development work
3. **Pull Requests** - Code review and merge

## Commit Message Format
```
type: short description

Longer explanation if needed
- Bullet points for details
- Reference issue numbers #123
```

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Testing
- `refactor:` Code restructuring
- `chore:` Maintenance

## Code Quality Checklist
Before creating PR:
- [ ] All tests pass
- [ ] Code is documented
- [ ] No hardcoded values
- [ ] Security review done
- [ ] Performance considered
- [ ] Error handling added

## Testing Strategy
1. **Unit Tests** - Test individual functions
2. **Integration Tests** - Test component interaction
3. **End-to-End Tests** - Test complete workflow
4. **Coverage Target** - Aim for >80%

## PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added where needed
- [ ] Documentation updated
```