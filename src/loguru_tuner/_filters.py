from loguru import logger

def filter_by_name(record: dict, logger_setting: dict) -> bool:
    return record["extra"].get("logger_name") == logger_setting.get("logger_name", "")

def filter_by_level(record: dict, logger_setting: dict) -> bool:
    return record["level"].no >= logger.level(logger_setting.get("level", "DEBUG").upper()).no
