import json
import os


def load_legacy_schema(data):
    legacy_schema = {}
    for age_group in data.get("age_groups", []):
        age_key = age_group.get("slug", age_group["id"])
        legacy_schema[age_key] = {}
        for domain in age_group.get("domains", []):
            dom_key = domain.get("slug", domain["id"])
            legacy_schema[age_key][dom_key] = {}
            for subject in domain.get("subjects", []):
                sub_key = subject.get("slug", subject["id"])
                legacy_schema[age_key][dom_key][sub_key] = {}
                for metric in subject.get("metrics", []):
                    code = metric["code"]
                    legacy_schema[age_key][dom_key][sub_key][code] = {
                        "criteria": metric.get("criteria", []),
                        "original": metric.get("original", ""),
                        "transformed": metric.get("transformed", ""),
                    }
    return legacy_schema


def load_metrics_schema_raw():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "metrics_schema.json")
    if not os.path.exists(json_path):
        return {"age_groups": []}
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


_RAW_DATA = load_metrics_schema_raw()

METRICS_SCHEMA = load_legacy_schema(_RAW_DATA)

METRICS_SCHEMA_NEW = _RAW_DATA.get("age_groups", [])

AGE_GROUPS = {age_group["slug"]: age_group["name"] for age_group in METRICS_SCHEMA_NEW}
