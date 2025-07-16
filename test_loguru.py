"""Test script for loguru configuration."""
# from src.lobubu import logger  # , monkey_patch
from loguru_tuner import logger

if __name__ == "__main__":
    # Set up enhanced logger functionality
    # monkey_patch()
    
    # Initialize logger with config
    logger.init_with_config("./config/logger_config.yaml")

    # Test different logger bindings
    logger.get_logger("logger_a").info("Logging INFO by logger_a - NOT LOGGED")
    logger.get_logger("logger_b").error("Logging ERROR by logger_b - NOT LOGGED")
    logger.get_logger(logger_name="logger_a").info("Logging INFO by logger_a - LOGGED")
    logger.get_logger(logger_name="logger_a").error("Logging ERROR by logger_a - LOGGED")
    logger.get_logger(logger_name="logger_b").error("Logging ERROR by logger_b - NOT LOGGED")
    logger.get_logger(logger_name="root").warning("Logging WARN by root - LOGGED")
    logger.info("Logging INFO by root")

    # Test handler management
    logger.remove_handler("console")
    # print("Handlers after removal:", logger.handlers_map)
    
    # Add handler back with new configuration
    logger.add_handler(
        "console",
        {
            "sink": "ext://sys.stderr",
            "level": "DEBUG",
            "format": (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> {name} | "
                "<level>{level: <8}</level> | {extra[logger_name]} |"
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            )
        }
    )

    # Test adding new logger
    logger.add_logger(
        "logger_c",
        {
            "handlers": {
                "console": {
                    "level": "INFO"
                }
            }
        }
    )

    # Test new logger configuration
    logger.info("Logging INFO by root - NOT LOGGED")
    logger.bind(logger_name="logger_c").error("Logging ERROR by root - LOGGED")
    # remove logger_c to clean up
    logger.remove_logger("logger_c")
    # Test logger_c again:
    try:
        logger.get_logger("logger_c").info("Logging INFO by logger_c - NOT LOGGED")
    except Exception as e:
        print(f"Expected error: {e}")
    # Print final configuration state
    # print("\nFinal configuration:")
    # print("Handlers:", logger.handlers_map)