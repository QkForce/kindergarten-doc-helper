import json
import os
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "config"
CONFIG_FILE = BASE / "metrics_schema.json"


def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        return {"version": "1.0", "age_groups": []}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"version": "1.0", "age_groups": []}


def save_config(data: dict):
    data_copy = {
        **data,
        "version": "1.0",
        "last_updated": datetime.now().isoformat(),
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data_copy, f, ensure_ascii=False, indent=2)
    return CONFIG_FILE


def get_age_group_dict_for_combo() -> dict:
    config = load_config()
    return {ag["id"]: ag["name"] for ag in config["age_groups"]}


def get_age_group_data(age_group_id: str) -> dict:
    config = load_config()
    return next(
        (ag for ag in config["age_groups"] if ag["id"] == age_group_id),
        None,
    )


def get_all_metric_codes(age_group_id: str) -> list:
    age_group = get_age_group_data(age_group_id)
    if not age_group:
        return []
    return [
        met["code"]
        for dom in age_group["domains"]
        for sub in dom["subjects"]
        for met in sub["metrics"]
    ]
