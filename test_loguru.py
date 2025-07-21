"""Test script for loguru configuration."""
# from src.lobubu import logger  # , monkey_patch
from loguru_tuner import logger

if __name__ == "__main__":
    # Set up enhanced logger functionality
    # monkey_patch()
    
    # Initialize logger with config
    logger.init_with_config("./config/logger_config.yaml")

    # Test different logger bindings
    logger_a = logger.get_logger("logger_a")
    logger_a.debug("Logging DEBUG - NOT LOGGED")
    logger_a.info("Logging INFO - LOGGED")
    logger_a.warning("Logging WARN - LOGGED")
    logger_a.error("Logging ERROR - LOGGED")
    logger_a.critical("Logging DEBUG - NOT LOGGED")

    logger_b = logger.get_logger("logger_b")
    logger_b.debug("Logging DEBUG - NOT LOGGED")
    logger_b.info("Logging INFO - LOGGED")
    logger_b.warning("Logging WARN - LOGGED")
    logger_b.error("Logging ERROR - LOGGED")
    # logger_b.parse() # TODO
    # exit(0)
    logger_root = logger.get_logger("root")
    logger_root.debug("Logging DEBUG - LOGGED")
    logger_root.info("Logging INFO - LOGGED")
    logger_root.warning("Logging WARN - LOGGED")
    logger_root.error("Logging ERROR - LOGGED")
    logger_root.critical("Logging CRITICAL - LOGGED")


    # Test root logger
    logger.info("Logging INFO by root")
    logger.debug("Logging DEBUG by root")
    logger.warning("Logging WARN by root")
    logger.error("Logging ERROR by root")
    logger.critical("Logging CRITICAL by root")

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
    print("\nFinal configuration:")
    print("Handlers:", logger.handlers_map)
    print("Loggers:", logger.loggers_map)

