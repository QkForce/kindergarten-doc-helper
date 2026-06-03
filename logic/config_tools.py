from config.metrics_schema import METRICS_SCHEMA


def get_age_group_data(age_group_id):
    return METRICS_SCHEMA[age_group_id]


def get_all_metric_codes(age_group_id):
    return [
        metric_code
        for subjects in METRICS_SCHEMA[age_group_id].values()
        for metrics in subjects.values()
        for metric_code in metrics.keys()
    ]
