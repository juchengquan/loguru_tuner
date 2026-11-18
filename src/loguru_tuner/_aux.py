"""
Enhanced loguru logger with support for logger and handler mappings.
"""
import sys  # noqa: F401 - when refraction, DO NOT REMOVE!  
from typing import Dict, cast, Any, List, Callable
# from loguru_tuner._types import EnhancedLogger
# from loguru import logger as _logger
# from loguru_tuner._utils import load_config, add_formatter_to_handlers, ensure_root_logger
# from loguru_tuner._filters import filter_by_name, filter_by_level


def _combined_filter(record: dict, logger, handler_name: str, filter_funcs: list = []) -> bool:
    """Filter records based on handler and logger configurations."""
    binded_loggers_info = logger.handlers_map[handler_name].get("loggers", {})

    return any(
        all(func(record, _logger_config) for func in filter_funcs)
        for _, _logger_config in binded_loggers_info.items()
    )

def create_loguru_filter(logger, handler_name: str, filter_functions: List[Callable]):
    """Create a loguru filter function for the given handler."""
    def loguru_filter(record):
        return _combined_filter(
            record,
            logger=logger,
            handler_name=handler_name,
            filter_funcs=filter_functions   # [filter_by_name, filter_by_level]
        )
    return loguru_filter

def handle_external_sink(sink_config: Any) -> Any:
    """Process external sink configuration.
    
    Args:
        sink_config: The sink configuration value, which might be a string like "ext://sys.stderr"
        
    Returns:
        The processed sink value (e.g., sys.stderr for "ext://sys.stderr")
    """
    if isinstance(sink_config, str) and sink_config.startswith("ext://"):
        return eval(sink_config.replace("ext://", ""))
    return sink_config

def update_handler_mapping(handler_name: str, handler_params: dict, logger_name: str, handlers_map: dict) -> None:
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

def configure_mapping(
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
        update_handler_mapping(
            handler_name=handler_name,
            handler_params=handler_params if handler_params else {},
            logger_name=logger_name,
            handlers_map=handlers_map,
        )
