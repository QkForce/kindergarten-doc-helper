from config.metrics_schema import METRICS_SCHEMA


def get_age_group_data(age_group):
    return METRICS_SCHEMA[age_group]


def get_age_group_metrics_mapping(age_group_data):
    return {
        code: metric_data
        for metric_group_data in age_group_data.values()
        for code, metric_data in metric_group_data.items()
    }
