import yaml

def load_config(path: str) -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def deep_update_dict(original_dict: dict, updates: dict) -> dict:
    """Recursively update original_dict with key-value pairs from updates."""
    for key, value in updates.items():
        if (
            isinstance(value, dict)
            and key in original_dict
            and isinstance(original_dict[key], dict)
        ):
            deep_update_dict(original_dict[key], value)
        else:
            original_dict[key] = value
    return original_dict

def ensure_root_logger(config):
    """
    Ensure that the config has a 'root' logger with at least a 'console' handler.
    """
    config.setdefault("loggers", {})
    if "root" not in config.get("handlers", {}):
        config["loggers"]["root"] = {"handlers": {"console": None}}
    return config


def add_formatter_to_handlers(config: dict) -> dict:
    """Ensure each handler has a formatter string set, using formatters if referenced."""
    for _, handler_setting in config.get("handlers", {}).items():
        if "format" not in handler_setting:
            handler_setting["format"] = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        else:
            handler_setting["format"] = config.get("formatters", {}).get(
                handler_setting["format"],
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
            )
    return config
