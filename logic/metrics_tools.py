import random
from config.config import GROUP_CONF, MARKERS_BY_TYPE

METRICS_GROUPS = GROUP_CONF["metrics_groups"]


def group_child_metrics_by_type(child_data, metrics_by_type):
    grouped_metrics = []
    for metric_code in metrics_by_type:
        metric = {
            "metric_code": metric_code,
            "description": GROUP_CONF["metrics_mapping"][metric_code]["original"],
            "transformed_description": GROUP_CONF["metrics_mapping"][metric_code][
                "transformed"
            ],
            "rate": child_data.get(metric_code, None),
        }
        grouped_metrics.append(metric)
    return grouped_metrics


def prepare_child_common_metrics(child_data):
    common_metrics = {}
    for metric_type, metrics_list in METRICS_GROUPS.items():
        common_metrics[metric_type] = group_child_metrics_by_type(
            child_data, metrics_list
        )
    return common_metrics


def get_transformed_description(child_metrics_group):
    transformed_descriptions = [
        metric["transformed_description"]
        for metric in child_metrics_group
        if metric["rate"] in [2, 3]
    ]
    transformed_descriptions_length = len(transformed_descriptions)
    if transformed_descriptions_length > 0:
        return transformed_descriptions[
            random.randint(0, transformed_descriptions_length - 1)
        ]
    return ""


def prepare_child_grow_card_data(child_data):
    child_common_metrics = prepare_child_common_metrics(child_data)
    child_card_data = {"fullname": child_data["name"]}
    for metric_type, marker in MARKERS_BY_TYPE.items():
        transformed_description = get_transformed_description(
            child_common_metrics[metric_type]
        )
        child_card_data[marker] = transformed_description
    return child_card_data


def prepare_all_children_grow_card_data(children_data):
    all_children_common_metrics = []
    for child_data in children_data:
        child_grow_card_data = prepare_child_grow_card_data(child_data)
        all_children_common_metrics.append(child_grow_card_data)
    return all_children_common_metrics
