import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "config"
CONFIG_FILE = BASE / "metrics_schema.json"


def load_config() -> dict:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_age_group(age_group_id) -> dict:
    config = load_config()
    return config.get(age_group_id, {})


def save_config(data: dict):
    data_copy = {
        **data,
        "version": "1.0",
        "last_updated": datetime.now().isoformat(),
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data_copy, f, ensure_ascii=False, indent=2)
    return CONFIG_FILE


def save_age_group(age_group_id: str, data: dict):
    config = load_config()
    config[age_group_id] = data
    return save_config(config)
