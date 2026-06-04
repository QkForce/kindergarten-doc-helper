import random
from typing import Dict, List


def build_grow_card(child: Dict, age_group_data: List[Dict]) -> Dict:
    card = {"fullname": child["name"]}
    for dom in age_group_data["domains"]:
        candidates = [
            met["transformed"]
            for sub in dom["subjects"]
            for met in sub["metrics"]
            if child.get(met["code"]) in (2, 3)
        ]
        dom_id = dom["id"]
        card[dom_id] = random.choice(candidates) if candidates else ""
    return card


def build_all_grow_cards(
    children_data: List[Dict], age_group_data: List[Dict]
) -> List[Dict]:
    return [build_grow_card(child, age_group_data) for child in children_data]
