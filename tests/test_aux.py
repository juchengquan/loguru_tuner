import os
import tempfile
import shutil
from loguru import logger
from src.logger import init_loguru_with_config

def test_setup_loguru_from_config_basic():
    # Create a minimal config file
    config_yaml = '''
formatters:
  simple: "<level>{message}</level>"
handlers:
  console:
    sink: ext://sys.stderr
    format: simple
    level: DEBUG
loggers:
  root:
    handlers:
      console:
    '''
    temp_dir = tempfile.mkdtemp()
    config_path = os.path.join(temp_dir, "test_config.yaml")
    with open(config_path, "w") as f:
        f.write(config_yaml)
    try:
        init_loguru_with_config(config_path)
        logger.info("Test message")
    finally:
        shutil.rmtree(temp_dir)
