import json
import os


def load_metrics_schema():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "metrics_schema.json")

    if not os.path.exists(json_path):
        return {}

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

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


METRICS_SCHEMA = load_metrics_schema()
