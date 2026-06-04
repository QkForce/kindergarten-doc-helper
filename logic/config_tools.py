from config.metrics_schema import METRICS_SCHEMA


def get_age_group_data(age_group_id):
    return next(
        (
            age_group
            for age_group in METRICS_SCHEMA["age_groups"]
            if age_group["id"] == age_group_id
        ),
        None,
    )


def get_all_metric_codes(age_group_id):
    age_group = get_age_group_data(age_group_id)
    if not age_group:
        return []
    return [
        met["code"]
        for dom in age_group["domains"]
        for sub in dom["subjects"]
        for met in sub["metrics"]
    ]
