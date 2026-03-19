from config.metrics_schema import METRICS_SCHEMA


def get_age_group_data(age_group):
    return METRICS_SCHEMA[age_group]


def get_all_metric_codes(age_group):
    return [
        metric_code
        for subjects in METRICS_SCHEMA[age_group].values()
        for metrics in subjects.values()
        for metric_code in metrics.keys()
    ]
