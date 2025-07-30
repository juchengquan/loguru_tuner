"""
Enhanced loguru logger with support for logger and handler mappings.
"""
import sys  # noqa: F401 - when refraction, DO NOT REMOVE!  
from typing import Dict, cast, Any
from loguru import logger as _logger
from loguru_tuner._logger_types import EnhancedLogger
from loguru_tuner._utils import load_config, add_formatter_to_handlers, ensure_root_logger
from loguru_tuner._filters import filter_by_name, filter_by_level


def combined_filter(record: dict, handler_name: str, filter_funcs: list = []) -> bool:
    """Filter records based on handler and logger configurations."""
    binded_loggers_info = logger.handlers_map[handler_name].get("loggers", {})

    return any(
        all(func(record, _logger_config) for func in filter_funcs)
        for _, _logger_config in binded_loggers_info.items()
    )

def _create_loguru_filter(handler_name: str):
    """Create a loguru filter function for the given handler."""
    def loguru_filter(record):
        return combined_filter(
            record,
            handler_name=handler_name,
            filter_funcs=[filter_by_name, filter_by_level]
        )
    return loguru_filter


def _handle_external_sink(sink_config: Any) -> Any:
    """Process external sink configuration.
    
    Args:
        sink_config: The sink configuration value, which might be a string like "ext://sys.stderr"
        
    Returns:
        The processed sink value (e.g., sys.stderr for "ext://sys.stderr")
    """
    if isinstance(sink_config, str) and sink_config.startswith("ext://"):
        return eval(sink_config.replace("ext://", ""))
    return sink_config


def _update_handler_mapping(handler_name: str, handler_params: dict, logger_name: str, handlers_map: dict) -> None:
    """Update the handler-logger bindings in the handlers map.
    
    Args:
        handler_name: Name of the handler
        logger_name: Name of the logger
        handler_params: Parameters for the handler
        handlers_map: The handlers mapping to update
    """
    handlers_map.setdefault(handler_name, {}).setdefault("loggers", {})
    handlers_map[handler_name]["loggers"][logger_name] = {
        "logger_name": logger_name,
        "level": handler_params.get("level", "DEBUG").upper()
    }


def _configure_mapping(
        logger_name: str,
        logger_config: dict,
        loggers_map: Dict[str, dict],
        handlers_map: Dict[str, dict],
        validate_handler: bool = True
    ) -> None:
    """Configure a logger with its handlers.
    
    Args:
        logger_name: Name of the logger to configure
        logger_config: Configuration for the logger
        loggers_map: The loggers mapping to update
        handlers_map: The handlers mapping to update
        validate_handler: Whether to validate that handlers exist before binding
    """
    # Validate logger doesn't already exist
    assert logger_name not in loggers_map, f"Logger {logger_name} already exists!"
    # Update loggers mapping
    loggers_map[logger_name] = logger_config
    
    # Process handlers
    handlers = logger_config.get("handlers", {})
    # Validate handlers exist if required
    if validate_handler:
        for handler_name in handlers:
            assert handler_name in handlers_map, f"Handler {handler_name} does not exist!"
    
    # Update handler bindings
    for handler_name, handler_params in handlers.items():
        _update_handler_mapping(
            handler_name=handler_name,
            handler_params=handler_params if handler_params else {},
            logger_name=logger_name,
            handlers_map=handlers_map,
        )

def monkey_patch() -> None:
    """Apply monkey patches to enhance loguru logger with additional functionality."""
    if not hasattr(_logger, "_patched_assets"):
        setattr(_logger, "_patched_assets", {
            "handlers_map": {},
            "loggers_map": {}
        })

        def init_with_config(self: EnhancedLogger, config_path: str) -> None:
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
                _configure_mapping(
                    logger_name, 
                    logger_config,
                    self.loggers_map,
                    self.handlers_map,
                    validate_handler=False
                )
                
        def add_handler(self: EnhancedLogger, handler_name: str, handler_conf: dict, validate_handler: bool = True) -> None:
            """Add a new handler to the logger.
            Args:
                handler_name (str): Name of the handler to add.
                handler_conf (dict): Configuration for the handler.
                validate_handler (bool): Whether to validate that the handler does not already exist.
            """
            if validate_handler:
                assert handler_name not in self.handlers_map, f"Handler {handler_name} already exists!"
            
            handler_conf = handler_conf.copy()  # Avoid mutating input
            handler_conf["sink"] = _handle_external_sink(handler_conf["sink"])

            # Add handler ID to the handlers map and create loguru sink
            self.handlers_map.setdefault(handler_name, {})["id"] = self.add(
                **handler_conf,
                filter=_create_loguru_filter(handler_name)
            )

        def remove_handler(self: EnhancedLogger, handler_name: str) -> None:
            """Remove a handler from the logger by its name."""
            assert handler_name in self.handlers_map, f"Handler {handler_name} does not exist!"

            handler_id = self.handlers_map.pop(handler_name)["id"]
            self.remove(handler_id)

        def add_logger(self: EnhancedLogger, logger_name: str, logger_config: dict) -> None:
            """Add a new logger configuration with specified handlers."""
            _configure_mapping(
                logger_name,
                logger_config,
                self.loggers_map,
                self.handlers_map,
                validate_handler=True
            )
        
        def get_logger(self: EnhancedLogger, logger_name: str) -> EnhancedLogger:
            """Get a logger by name."""
            assert logger_name in self.loggers_map, \
                f"Logger {logger_name} does not exist!"
            return cast(EnhancedLogger, _logger.bind(logger_name=logger_name))

        def update_logger(self: EnhancedLogger, logger_name: str, logger_config: dict) -> None:
            """Update a logger by name and configurations.
            
            Args:
                logger_name: Name of the logger to update
                logger_config: New configuration for the logger
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
                _update_handler_mapping(
                    handler_name=handler_name,
                    handler_params=handler_params if handler_params else {},
                    logger_name=logger_name,
                    handlers_map=self.handlers_map
                )

        def remove_logger(self: EnhancedLogger, logger_name: str) -> None:
            """Remove a logger by name."""
            assert logger_name in self.loggers_map, \
                f"Logger {logger_name} does not exist!"
            
            # Remove all handlers associated with this logger
            # for handler_name, handler_info in self.handlers_map.items():
            #     if logger_name in handler_info.get("loggers", {}):
            #         self.remove_handler(handler_name)
            
            # Remove the logger from the loggers map
            self.loggers_map.pop(logger_name)

        # Add property accessors for type hints
        @property
        def handlers_map(self: EnhancedLogger) -> Dict[str, dict]:
            """Get the handlers mapping."""
            return self._patched_assets["handlers_map"]
            
        @property
        def loggers_map(self: EnhancedLogger) -> Dict[str, dict]:
            """Get the loggers mapping."""
            return self._patched_assets["loggers_map"]

        # Add methods to logger
        setattr(_logger.__class__, "init_with_config", init_with_config)
        setattr(_logger.__class__, "add_handler", add_handler)
        setattr(_logger.__class__, "remove_handler", remove_handler)
        setattr(_logger.__class__, "add_logger", add_logger)
        setattr(_logger.__class__, "get_logger", get_logger)
        setattr(_logger.__class__, "update_logger", update_logger)
        setattr(_logger.__class__, "remove_logger", remove_logger)

        setattr(_logger.__class__, "handlers_map", handlers_map)
        setattr(_logger.__class__, "loggers_map", loggers_map)

# Re-export the enhanced logger
monkey_patch()

logger = cast(EnhancedLogger, _logger)
