import json
import os


def load_metrics_schema_raw():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "metrics_schema.json")
    if not os.path.exists(json_path):
        return {"age_groups": []}
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


METRICS_SCHEMA = load_metrics_schema_raw()

AGE_GROUPS = {
    age_group["id"]: age_group["name"] for age_group in METRICS_SCHEMA["age_groups"]
}
