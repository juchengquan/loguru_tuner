"""
Type hints for enhanced loguru logger functionality.
"""
from loguru._logger import Logger
from typing import Protocol, Dict, cast
from loguru_tuner._filters import filter_by_name, filter_by_level
from loguru_tuner._utils import load_config, add_formatter_to_handlers, ensure_root_logger
from loguru_tuner._aux import create_loguru_filter, handle_external_sink, update_handler_mapping, configure_mapping
# from loguru_tuner._utils import create_protocol_from_class

# _BaseLogger = create_protocol_from_class(Logger)


class EnhancedLogger(Logger):
    """Protocol defining enhanced logger functionality for loguru_tuner.
    
    This protocol extends the base Loguru Logger with additional methods
    for configuration management, handler operations, and named loggers.
    """
    def init_with_config(self, config_path: str) -> None:
        """Configure loguru logger from a YAML config file.
        
        Args:
            config_path (str): Path to the YAML config file.
        """
        self.remove()
        self.configure(extra={"logger_name": "root"})

        config = load_config(config_path)
        config = add_formatter_to_handlers(config)
        config = ensure_root_logger(config)

        # Initialize handlers
        for handler_name, handler_conf in config.get("handlers", {}).items():
            self.add_handler(
                handler_name, handler_conf, validate_handler=False
            )
        
        # Initialize loggers (don't validate handlers as they're not added yet)
        for logger_name, logger_config in config.get("loggers", {}).items():
            configure_mapping(
                logger_name, 
                logger_config,
                self.loggers_map,
                self.handlers_map,
                validate_handler=False
            )
            
    
    def add_handler(self, handler_name: str, handler_conf: dict, validate_handler: bool = True) -> None:
        """Add a new handler to the logger.
        Args:
            handler_name (str): Name of the handler to add.
            handler_conf (dict): Configuration for the handler.
            validate_handler (bool): Whether to validate that the handler does not already exist.
        """
        if validate_handler:
            assert handler_name not in self.handlers_map, f"Handler {handler_name} already exists!"
        
        handler_conf = handler_conf.copy()  # Avoid mutating input
        handler_conf["sink"] = handle_external_sink(handler_conf["sink"])

        # TODO
        filter_functions = [filter_by_level, filter_by_name]
        # Add handler ID to the handlers map and CREATE loguru sink
        self.handlers_map.setdefault(handler_name, {})["id"] = self.add(
            **handler_conf,
            filter=create_loguru_filter(self, handler_name, filter_functions)
        )

    def remove_handler(self, handler_name: str) -> None:
        """Remove a handler from the logger.
        
        Args:
            handler_name: Name of the handler to remove
        
        Raises:
            AssertionError: If the handler doesn't exist
        """
        assert handler_name in self.handlers_map, f"Handler {handler_name} does not exist!"

        handler_id = self.handlers_map.pop(handler_name)["id"]
        self.remove(handler_id)

    def add_logger(self, logger_name: str, logger_config: dict) -> None:
        """Add a new logger configuration with specified handlers.
    
        Args:
            logger_name: Unique name for the logger
            logger_config: Configuration dictionary for the logger
            
        Raises:
            AssertionError: If the logger already exists or references non-existent handlers
        """
        configure_mapping(
            logger_name,
            logger_config,
            self.loggers_map,
            self.handlers_map,
            validate_handler=True
        )        

    def get_logger(self, logger_name: str) -> "EnhancedLogger":
        """Get a logger by name."""
        assert logger_name in self.loggers_map, \
            f"Logger {logger_name} does not exist!"
        return cast(EnhancedLogger, self.bind(logger_name=logger_name))
    
    def update_logger(self, logger_name: str, logger_config: dict) -> None:
        """Update an existing logger's configuration.
        
        Args:
            logger_name: Name of the logger to update
            logger_config: New configuration dictionary for the logger
            
        Raises:
            AssertionError: If the logger doesn't exist or references non-existent handlers
        """
        
        assert logger_name in self.loggers_map, \
            f"Logger {logger_name} does not exist!"

        # Remove existing logger bindings from handlers
        for handler_name, handler_info in self.handlers_map.items():
            if logger_name in handler_info.get("loggers", {}):
                handler_info["loggers"].pop(logger_name)

        # Update logger config in loggers map
        self.loggers_map[logger_name] = logger_config

        # Add new handler bindings
        for handler_name, handler_params in logger_config.get("handlers", {}).items():
            update_handler_mapping(
                handler_name=handler_name,
                handler_params=handler_params if handler_params else {},
                logger_name=logger_name,
                handlers_map=self.handlers_map
            )

    def remove_logger(self, logger_name: str) -> None:
        """Remove a logger by name.
        
        Args:
            logger_name: Name of the logger to remove
            
        Raises:
            AssertionError: If the logger doesn't exist
        """
        assert logger_name in self.loggers_map, \
            f"Logger {logger_name} does not exist!"
        
        # Remove all handlers associated with this logger
        # for handler_name, handler_info in self.handlers_map.items():
        #     if logger_name in handler_info.get("loggers", {}):
        #         self.remove_handler(handler_name)
        
        # Remove the logger from the loggers map
        self.loggers_map.pop(logger_name)

    def set_patched_assets(self):
        self._patched_assets = {
            "handlers_map": {},
            "loggers_map": {}
        }

    @property
    def _patched_assets(self) -> Dict:
        print("EEE")
        return self._patched_assets

    # @_patched_assets.setter
    # def _patched_assets(self):
    #     self.__patched_assets


    @property
    def handlers_map(self) -> Dict[str, dict]:
        """Get the handlers mapping.
        
        Returns:
            Dictionary mapping handler names to their configurations
        """
        return self._patched_assets["handlers_map"]

    @property
    def loggers_map(self) -> Dict[str, dict]:
        """Get the loggers mapping.
        
        Returns:
            Dictionary mapping logger names to their configurations
        """
        return self._patched_assets["loggers_map"]

# Re-export the Protocol
__all__ = ['EnhancedLogger']
