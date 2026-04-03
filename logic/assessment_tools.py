from config.metrics_schema import METRICS_SCHEMA
from logic.types import AssessmentStatus


def bulk_update(domains, score):
    for dn, subjects in domains.items():
        for sn, metrics in subjects.items():
            for mn in metrics.keys():
                domains[dn][sn][mn] = score


def set_subjects_score(subjects, score):
    for sn, metrics in subjects.items():
        for mn in metrics.keys():
            subjects[sn][mn] = score


def set_metrics_score(metrics, score):
    for mn in metrics.keys():
        metrics[mn] = score


def get_common_score_type(score_dict):
    score_types = set(
        [
            score
            for subjects in score_dict.values()
            for metrics in subjects.values()
            for score in metrics.values()
        ]
    )
    return score_types.pop() if len(score_types) == 1 else 0


def get_domain_score_type(subjects):
    score_types = set(
        [score for metrics in subjects.values() for score in metrics.values()]
    )
    return score_types.pop() if len(score_types) == 1 else 0


def get_subject_score_type(metrics):
    score_types = set(metrics.values())
    return score_types.pop() if len(score_types) == 1 else 0


def get_assessment_status(score_dict) -> AssessmentStatus:
    total_metrics = 0
    scored_metrics = 0

    for subjects in score_dict.values():
        for metrics in subjects.values():
            for score in metrics.values():
                total_metrics += 1
                if score != 0:
                    scored_metrics += 1

    if scored_metrics == 0:
        return AssessmentStatus.NOT_STARTED
    elif scored_metrics < total_metrics:
        return AssessmentStatus.IN_PROGRESS
    else:
        return AssessmentStatus.COMPLETED


def create_default_scoring_dict(age_group):
    scoring_dict = {
        domain: {
            subject: {metric: 0 for metric in metrics}
            for subject, metrics in subjects.items()
        }
        for domain, subjects in METRICS_SCHEMA[age_group].items()
    }
    return scoring_dict


def create_source_scoring_dict(age_group, scores):
    # scores = [{"name": "Child 1", "code-1": 2, "code-2": 3}, ...]
    scoring_dict = {}
    for item in scores:
        name = item["name"]
        scoring_dict[name] = {}
        for dn, subjects in METRICS_SCHEMA[age_group].items():
            scoring_dict[name][dn] = {}
            for sn, metrics in subjects.items():
                scoring_dict[name][dn][sn] = {}
                for code in metrics.keys():
                    score = item.get(code, 0)
                    scoring_dict[name][dn][sn][code] = score
    return scoring_dict
