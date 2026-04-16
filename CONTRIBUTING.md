# Contributing to NovaOS

Thank you for your interest in contributing to NovaOS! Every contribution — whether it's a bug fix, a new skill, a documentation improvement, or a feature request — is warmly welcomed.

## Getting Started

1. **Fork** the repository and clone it locally.
2. Create a virtual environment and install dependencies:
   ```bash
   python3.12 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```
3. Run the test suite to confirm everything works:
   ```bash
   pytest tests/
   ```

## How to Add a New Skill

Skills are the primary extension point for NovaOS. A skill is a single Python file in `novaos/skills/` that subclasses `BaseSkill`.

```python
from novaos.skills import BaseSkill, register

class MySkill(BaseSkill):
    name = "skill_my_skill"
    description = "What this skill does."
    version = "0.1.0"

    def run(self, **kwargs) -> str:
        # Your implementation here
        return "Done!"

register(MySkill())
```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and [Black](https://black.readthedocs.io/) for formatting. Run before committing:

```bash
ruff check novaos/ && black novaos/
```

## Pull Request Guidelines

- Keep PRs focused on a single feature or fix.
- Write or update tests for any new functionality.
- Update the README if you add user-facing features.
- Be respectful and constructive in code reviews.

## Reporting Issues

Please use [GitHub Issues](https://github.com/Safemoonkoa/NovaOS/issues) and include:
- Your OS and Python version.
- Steps to reproduce the problem.
- Expected vs. actual behaviour.
- Relevant logs or screenshots.

We appreciate every contribution. Let's build the future of desktop AI together!
