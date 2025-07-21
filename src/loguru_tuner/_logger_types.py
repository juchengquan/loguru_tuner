"""
Type hints for enhanced loguru logger functionality.
"""
import inspect
from loguru._logger import Logger
def get_all_methods(cls):
    methods = []
    for name, member in inspect.getmembers(cls, predicate=inspect.isfunction):
        # Exclude built-in methods (dunder methods)
        if not name.startswith('__'):
            methods.append(name)
    return methods

# Get methods from MyClass (which implements MyProtocol)
class_methods = get_all_methods(Logger)
print(f"Methods in MyClass: {class_methods}")

g = type("wtf", (Logger,), {})
print(type(g))

from typing import Protocol, Dict, Any, Union, Optional, Callable

class BaseLogger(Protocol):
    """Protocol defining base logger functionality."""
    
    def bind(self, **kwargs: Any) -> 'BaseLogger':
        """Bind context variables."""
        ...

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log info message."""
        ...
    
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log critical message."""
        ...

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log error message."""
        ...

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log warning message."""
        ...

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log debug message."""
        ...

    def remove(self, handler_id: Optional[Union[str, int]] = None) -> None:
        """Remove a handler."""
        ...

    def add(self, sink: Union[str, Callable, Any], **kwargs: Any) -> int:
        """Add a handler."""
        ...

    def configure(self, **kwargs: Any) -> None:
        """Configure logger."""
        ...

class EnhancedLogger(BaseLogger, Protocol):
    """Protocol defining enhanced logger functionality."""
    
    def init_with_config(self, config_path: str) -> None:
        """Configure loguru logger from a YAML config file."""
        ...

    def add_handler(self, handler_name: str, handler_conf: dict, **kwargs) -> None:
        """Add a new handler to the logger."""
        ...
    
    def remove_handler(self, handler_name: str) -> None:
        """Remove a handler from the logger."""
        ...

    def add_logger(self, logger_name: str, logger_config: dict) -> None:
        """Add a new logger configuration."""
        ...

    def get_logger(self, logger_name: str) -> 'EnhancedLogger':
        """Get a logger by name."""
        ...

    def remove_logger(self, logger_name: str) -> None:
        """Remove a logger by name."""
        ...

    @property
    def handlers_map(self) -> Dict[str, dict]:
        """Get the handlers mapping."""
        ...

    @property
    def loggers_map(self) -> Dict[str, dict]:
        """Get the loggers mapping."""
        ...

# Re-export the Protocol
__all__ = ['EnhancedLogger']
