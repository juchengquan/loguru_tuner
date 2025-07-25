"""
Type hints for enhanced loguru logger functionality.
"""
from loguru._logger import Logger
from typing import Protocol, Dict
from loguru_tuner._utils import create_protocol_from_class


_BaseLogger = create_protocol_from_class(Logger)

class EnhancedLogger(_BaseLogger, Protocol):
    """Protocol defining enhanced logger functionality for loguru_tuner.
    
    This protocol extends the base Loguru Logger with additional methods
    for configuration management, handler operations, and named loggers.
    """
    
    def init_with_config(self, config_path: str) -> None:
        """Configure loguru logger from a YAML config file.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        ...

    def add_handler(self, handler_name: str, handler_conf: dict, validate_handler: bool = True) -> None:
        """Add a new handler to the logger.
        
        Args:
            handler_name: Unique name for the handler
            handler_conf: Configuration dictionary for the handler
            validate_handler: Whether to validate that the handler doesn't already exist
        """
        ...
    
    def remove_handler(self, handler_name: str) -> None:
        """Remove a handler from the logger.
        
        Args:
            handler_name: Name of the handler to remove
        
        Raises:
            AssertionError: If the handler doesn't exist
        """
        ...

    def add_logger(self, logger_name: str, logger_config: dict) -> None:
        """Add a new logger configuration with specified handlers.
        
        Args:
            logger_name: Unique name for the logger
            logger_config: Configuration dictionary for the logger
            
        Raises:
            AssertionError: If the logger already exists or references non-existent handlers
        """
        ...

    def get_logger(self, logger_name: str) -> 'EnhancedLogger':
        """Get a logger by name.
        
        Args:
            logger_name: Name of the logger to retrieve
            
        Returns:
            A bound logger instance with the specified name
            
        Raises:
            AssertionError: If the logger doesn't exist
        """
        ...

    def remove_logger(self, logger_name: str) -> None:
        """Remove a logger by name.
        
        Args:
            logger_name: Name of the logger to remove
            
        Raises:
            AssertionError: If the logger doesn't exist
        """
        ...

    @property
    def handlers_map(self) -> Dict[str, dict]:
        """Get the handlers mapping.
        
        Returns:
            Dictionary mapping handler names to their configurations
        """
        ...

    @property
    def loggers_map(self) -> Dict[str, dict]:
        """Get the loggers mapping.
        
        Returns:
            Dictionary mapping logger names to their configurations
        """
        ...

# Re-export the Protocol
__all__ = ['EnhancedLogger']
