# Loguru Tuner 🎭

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A sophisticated configuration orchestrator for the Loguru logger that brings harmony to your Python logging setup. Loguru Tuner extends the powerful [Loguru](https://github.com/Delgan/loguru) library with YAML-based configuration, named loggers, and advanced filtering capabilities.

## ✨ Features

- 📝 YAML-based configuration for easy setup
- 🎯 Named logger support with context binding
- 🔍 Advanced filtering capabilities
- 🎨 Customizable formatters
- 🔄 Dynamic handler management
- 🚀 Zero-config default setup

## 🚀 Installation

```bash
# Install from PyPI (recommended)
pip install loguru-tuner

# Install from source
git clone https://github.com/juchengquan/loguru_tuner.git
cd loguru_tuner
pip install .

# For development installation (includes dev dependencies)
pip install -e ".[dev]"
```

## 📖 Quick Start

```python
from loguru_tuner import logger

# Initialize logger with config
logger.init_with_config("config/logger_config.yaml")

# Use logger with named configurations
logger.bind(logger_name="my_logger").info("Hello from my logger!")
```

## 🛠️ Configuration

Example configuration in `config/logger_config.yaml`:

```yaml
formatters:
  simple: "<level>{message}</level>"
  detailed: "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

handlers:
  console:
    sink: ext://sys.stderr
    format: detailed
    level: DEBUG
    
  file:
    sink: log/app.log
    format: detailed
    level: INFO
    rotation: "500 MB"
    retention: "10 days"

loggers:
  root:
    handlers: [console]
    level: INFO
  
  api:
    handlers: [console, file]
    level: DEBUG
```

## 🧪 Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=src/

# Type checking
mypy src/

# Code formatting
black src/ tests/
isort src/ tests/
```

## 📚 Documentation

For detailed documentation and advanced usage examples, please visit our [documentation](https://github.com/juchengquan/loguru_tuner/wiki).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✨ Acknowledgments

- [Loguru](https://github.com/Delgan/loguru) - The awesome logging library this project extends
- All our contributors and users
