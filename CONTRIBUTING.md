# Contributing Guide

## Development Process

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes

```bash
git commit -m "feat: add some feature"
```

4. Push to your fork

```bash
git push origin feature/your-feature-name
```

5. Create a Pull Request

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Changes to build process

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Keep functions focused and small
- Write unit tests for new features

## Testing

Run tests before submitting PR:

```bash
pytest
```

## Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update API documentation 