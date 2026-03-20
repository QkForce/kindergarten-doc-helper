import random
from typing import Dict, List


def build_grow_card(child: Dict, age_group_data: Dict) -> Dict:
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


def build_all_grow_cards(children_data: List[Dict], age_group_data: Dict) -> List[Dict]:
    return [build_grow_card(child, age_group_data) for child in children_data]
