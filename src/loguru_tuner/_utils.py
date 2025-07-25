from typing import Protocol, Any, get_type_hints
import ast
import inspect
import types
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


def create_protocol_from_class(cls, protocol_name=None):
    protocol_name = protocol_name or f"{cls.__name__}Protocol"
    namespace = {}

    # Collect __init__ parameter type hints
    try:
        init_hints = get_type_hints(cls.__init__)
    except Exception:
        init_hints = {}

    # Use AST to find `self.x = ...` attributes
    attributes = {}
    try:
        source = inspect.getsource(cls)
        tree = ast.parse(source)

        class_def = next(node for node in tree.body if isinstance(node, ast.ClassDef))
        init_def = next(
            (f for f in class_def.body if isinstance(f, ast.FunctionDef) and f.name == "__init__"),
            None,
        )
        if init_def:
            for stmt in ast.walk(init_def):
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        if (
                            isinstance(target, ast.Attribute)
                            and isinstance(target.value, ast.Name)
                            and target.value.id == "self"
                        ):
                            attr_name = target.attr
                            # Try to map it to a parameter hint, fallback to Any
                            attr_type = init_hints.get(attr_name, Any)
                            attributes[attr_name] = attr_type
    except Exception as e:
        print(f"[Warning] Could not parse class attributes: {e}")

    # Add attributes to namespace
    namespace.update(attributes)

    # Add public methods to namespace
    for name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
        if name.startswith("_") and name != "__init__":
            continue
        namespace[name] = func

    # Create the Protocol class dynamically
    protocol_cls = types.new_class(
        protocol_name,
        (Protocol,),
        exec_body=lambda ns: ns.update(namespace)
    )
    return protocol_cls

