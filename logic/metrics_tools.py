import random
from config.metrics_groups_senior import METRICS_GROUPS
from config.config import GROUP_CONF


def group_child_metrics_by_type(child_data, metrics_by_type):
    grouped_metrics = []
    for metric in metrics_by_type:
        metric = {
            "metric_code": metric,
            "description": GROUP_CONF["metrics_mapping"][metric]["original"],
            "transformed_description": GROUP_CONF["metrics_mapping"][metric][
                "transformed"
            ],
            "rate": child_data.get(metric, None),
        }
        grouped_metrics.append(metric)
    return grouped_metrics


def prepare_child_common_metrics(child_data):
    common_metrics = {
        "physical": group_child_metrics_by_type(child_data, METRICS_GROUPS["physical"]),
        "communicative": group_child_metrics_by_type(
            child_data, METRICS_GROUPS["communicative"]
        ),
        "cognitive": group_child_metrics_by_type(
            child_data, METRICS_GROUPS["cognitive"]
        ),
        "creativity": group_child_metrics_by_type(
            child_data, METRICS_GROUPS["creativity"]
        ),
        "social": group_child_metrics_by_type(child_data, METRICS_GROUPS["social"]),
    }
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
    fullname = child_data["name"]
    transformed_description_physical = get_transformed_description(
        child_common_metrics["physical"]
    )
    transformed_description_communicative = get_transformed_description(
        child_common_metrics["communicative"]
    )
    transformed_description_cognitive = get_transformed_description(
        child_common_metrics["cognitive"]
    )
    transformed_description_creativity = get_transformed_description(
        child_common_metrics["creativity"]
    )
    transformed_description_social = get_transformed_description(
        child_common_metrics["social"]
    )
    return {
        "fullname": fullname,
        "physical-1": transformed_description_physical,
        "communicative-1": transformed_description_communicative,
        "cognitive-1": transformed_description_cognitive,
        "creativity-1": transformed_description_creativity,
        "social-1": transformed_description_social,
    }


def prepare_all_children_grow_card_data(children_data):
    all_children_common_metrics = []
    for child_data in children_data:
        child_grow_card_data = prepare_child_grow_card_data(child_data)
        all_children_common_metrics.append(child_grow_card_data)
    return all_children_common_metrics
