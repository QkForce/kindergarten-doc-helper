import random
from typing import Dict, List


def prepare_child_metrics(
    child_data: Dict, age_group_data: Dict[str, Dict[str, Dict]]
) -> Dict[str, Dict]:
    child_metrics = {}
    for metric_group in age_group_data.keys():
        child_metric = {}
        for metric_code, data in age_group_data[metric_group].items():
            child_metric[metric_code] = {
                "description": data["original"],
                "transformed_description": data["transformed"],
                "rate": child_data.get(metric_code, None),
            }
        child_metrics[metric_group] = child_metric
    return child_metrics


def get_transformed_description(metric_group_data: Dict[str, Dict]) -> str:
    transformed_descriptions = [
        metric_data["transformed_description"]
        for metric_data in metric_group_data.values()
        if metric_data["rate"] in [2, 3]
    ]
    transformed_descriptions_length = len(transformed_descriptions)
    if transformed_descriptions_length > 0:
        return transformed_descriptions[
            random.randint(0, transformed_descriptions_length - 1)
        ]
    return ""


def prepare_child_grow_card_data(
    child_data: Dict, age_group_data: Dict[str, Dict[str, Dict]]
):
    child_metrics = prepare_child_metrics(child_data, age_group_data)
    child_card_data = {"fullname": child_data["name"]}
    for metric_group in age_group_data.keys():
        transformed_description = get_transformed_description(
            child_metrics[metric_group]
        )
        child_card_data[metric_group] = transformed_description
    return child_card_data


def prepare_all_children_grow_card_data(
    children_data: List[Dict], age_group_data: Dict[str, Dict[str, Dict]]
) -> List[Dict[str, str]]:
    all_children_card_data_list = []
    for child_data in children_data:
        child_card_data = prepare_child_grow_card_data(child_data, age_group_data)
        all_children_card_data_list.append(child_card_data)
    return all_children_card_data_list
