import os
import yaml
from dotenv import load_dotenv
from shared.paths import env_config_path


def load_config():
    load_dotenv()
    env = os.getenv("ENV", "dev").lower()
    config_path = env_config_path(env)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {os.path.abspath(config_path)}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
