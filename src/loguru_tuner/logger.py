"""
Enhanced loguru logger with support for logger and handler mappings.
"""
import sys  # noqa: F401 - when refraction, DO NOT REMOVE!  
from typing import cast, # Dict 
from loguru import logger as _logger
from loguru_tuner._types import EnhancedLogger

# from loguru_tuner._utils import load_config, add_formatter_to_handlers, ensure_root_logger
# from loguru_tuner._filters import filter_by_name, filter_by_level
# from loguru_tuner._aux import create_loguru_filter, handle_external_sink, update_handler_mapping, configure_mapping


_logger = cast(EnhancedLogger, _logger)


def monkey_patch() -> None:
    """Apply monkey patches to enhance loguru logger with additional functionality."""
    setattr(_logger.__class__, "set_patched_assets", EnhancedLogger.set_patched_assets)
    if not hasattr(_logger, "_patched_assets"):
        _logger.set_patched_assets()
        # setattr(_logger, "_patched_assets", {
        #     "handlers_map": {},
        #     "loggers_map": {}
        # })

        # Add methods to logger
        setattr(_logger.__class__, "init_with_config", EnhancedLogger.init_with_config)
        setattr(_logger.__class__, "add_handler", EnhancedLogger.add_handler)
        setattr(_logger.__class__, "remove_handler", EnhancedLogger.remove_handler)
        setattr(_logger.__class__, "add_logger", EnhancedLogger.add_logger)
        setattr(_logger.__class__, "get_logger", EnhancedLogger.get_logger)

        setattr(_logger.__class__, "update_logger", EnhancedLogger.update_logger)
        setattr(_logger.__class__, "remove_logger", EnhancedLogger.remove_logger)

        # setattr(_logger.__class__, "set_patched_assets", EnhancedLogger.set_patched_assets)
        setattr(_logger.__class__, "handlers_map", EnhancedLogger.handlers_map)
        setattr(_logger.__class__, "loggers_map", EnhancedLogger.loggers_map)

# Re-export the enhanced logger
monkey_patch()

# logger = cast(EnhancedLogger, _logger)
logger = _logger
