import random
from typing import Dict, List


def prepare_child_grow_card_data(child: Dict, age_group_data: Dict) -> Dict:
    card = {"fullname": child["name"]}
    for domain, subjects in age_group_data.items():
        candidates = [
            m["transformed"]
            for metrics in subjects.values()
            for code, m in metrics.items()
            if child.get(code) in (2, 3)
        ]
        card[domain] = random.choice(candidates) if candidates else ""
    return card


def prepare_all_children_grow_card_data(
    children_data: List[Dict], age_group_data: Dict
) -> List[Dict]:
    return [
        prepare_child_grow_card_data(child, age_group_data) for child in children_data
    ]
