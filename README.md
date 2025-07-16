# Loguru Maestro 🎭

A sophisticated configuration orchestrator for Loguru logger that brings harmony to your logging setup.

## Installation

```bash
# Install from current directory
pip install .

# For development installation
pip install -e ".[dev]"
```

## Usage

```python
from src.logger import logger

# Initialize logger with config
logger.init_with_config("config/loguru_config.yaml")

# Use logger with named configurations
logger.bind(logger_name="my_logger").info("Message")
```

## Development

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy src/

# Format code
black src/ tests/
isort src/ tests/
```

## Configuration

Example configuration in `config/loguru_config.yaml`:

```yaml
formatters:
  simple: "<level>{message}</level>"
handlers:
  console:
    sink: ext://sys.stderr
    format: simple
    level: DEBUG
loggers:
  root:
    handlers:
      console:
```
