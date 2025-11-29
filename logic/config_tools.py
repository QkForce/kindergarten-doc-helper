from config import (
    metrics_mapping_early_age,
    metrics_mapping_junior,
    metrics_mapping_middle,
    metrics_mapping_senior,
    metrics_mapping_preschool,
    metrics_groups_early_age,
    metrics_groups_junior,
    metrics_groups_middle,
    metrics_groups_senior,
    metrics_groups_preschool,
)

GROUPS = {
    "early_age": {
        "metrics_mapping": metrics_mapping_early_age.MAPPING,
        "metrics_groups": metrics_groups_early_age.METRICS_GROUPS,
    },
    "junior": {
        "metrics_mapping": metrics_mapping_junior.MAPPING,
        "metrics_groups": metrics_groups_junior.METRICS_GROUPS,
    },
    "middle": {
        "metrics_mapping": metrics_mapping_middle.MAPPING,
        "metrics_groups": metrics_groups_middle.METRICS_GROUPS,
    },
    "senior": {
        "metrics_mapping": metrics_mapping_senior.MAPPING,
        "metrics_groups": metrics_groups_senior.METRICS_GROUPS,
    },
    "preschool": {
        "metrics_mapping": metrics_mapping_preschool.MAPPING,
        "metrics_groups": metrics_groups_preschool.METRICS_GROUPS,
    },
}


def get_group_metrics_mapping(group_type):
    return GROUPS[group_type]["metrics_mapping"]


def get_group_metrics_groups(group_type):
    return GROUPS[group_type]["metrics_groups"]
