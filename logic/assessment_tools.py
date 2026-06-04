from config.metrics_schema import get_age_group_data
from logic.types import AssessmentStatus


def bulk_update(domains, score):
    for dom_id, dom in domains.items():
        for sub_id, sub in dom["subjects"].items():
            for met_id, met in sub["metrics"].items():
                domains[dom_id]["subjects"][sub_id]["metrics"][met_id] = {
                    "score": score,
                    "id": met_id,
                    "code": met["code"],
                    "description": met["description"],
                    "criteria": met["criteria"],
                }


def set_subjects_score(subjects, score):
    for sub_id, sub in subjects.items():
        for met_id, met in sub["metrics"].items():
            subjects[sub_id]["metrics"][met_id] = {
                "score": score,
                "id": met_id,
                "code": met["code"],
                "description": met["description"],
                "criteria": met["criteria"],
            }


def set_metrics_score(metrics, score):
    for met_id, met in metrics.items():
        metrics[met_id] = {
            "score": score,
            "id": met_id,
            "code": met["code"],
            "description": met["description"],
            "criteria": met["criteria"],
        }


def get_child_common_score_type(score_dict):
    score_types = set(
        [
            metric["score"]
            for dom in score_dict.values()
            for sub in dom["subjects"].values()
            for metric in sub["metrics"].values()
        ]
    )
    return score_types.pop() if len(score_types) == 1 else 0


def get_domain_score_type(subjects):
    score_types = set(
        [
            metric["score"]
            for sub in subjects.values()
            for metric in sub["metrics"].values()
        ]
    )
    return score_types.pop() if len(score_types) == 1 else 0


def get_subject_score_type(metrics):
    score_types = set(metric["score"] for metric in metrics.values())
    return score_types.pop() if len(score_types) == 1 else 0


def get_assessment_status(score_dict) -> AssessmentStatus:
    total_metrics = 0
    scored_metrics = 0

    for dom in score_dict.values():
        for sub in dom["subjects"].values():
            for metric in sub["metrics"].values():
                total_metrics += 1
                if metric["score"] != 0:
                    scored_metrics += 1

    if scored_metrics == 0:
        return AssessmentStatus.NOT_STARTED
    elif scored_metrics < total_metrics:
        return AssessmentStatus.IN_PROGRESS
    else:
        return AssessmentStatus.COMPLETED


def get_children_assessment_status(children_scores: list) -> AssessmentStatus:
    any_scored = False
    any_incomplete = False

    for child_scores in children_scores.values():
        for dom in child_scores.values():
            for sub in dom["subjects"].values():
                for metric in sub["metrics"].values():
                    score = metric["score"]
                    if score and score > 0:
                        any_scored = True
                    else:
                        any_incomplete = True
                    if any_scored and any_incomplete:
                        return AssessmentStatus.IN_PROGRESS

    if not any_scored:
        return AssessmentStatus.NOT_STARTED
    if not any_incomplete:
        return AssessmentStatus.COMPLETED
    return AssessmentStatus.IN_PROGRESS


def create_source_scoring_dict(age_group_id, scores):
    scoring_dict = {}
    target_age = get_age_group_data(age_group_id)
    if not target_age:
        return scoring_dict

    for item in scores:
        name_child = item["name"]
        scoring_dict[name_child] = {}
        for domain in target_age.get("domains", []):
            dom_id = domain["id"]
            scoring_dict[name_child][dom_id] = {
                "name": domain.get("name", dom_id),
                "subjects": {},
            }
            for subject in domain.get("subjects", []):
                sub_id = subject["id"]
                scoring_dict[name_child][dom_id]["subjects"][sub_id] = {
                    "name": subject.get("name", sub_id),
                    "metrics": {},
                }
                for metric in subject.get("metrics", []):
                    met_id = metric.get("id", metric["code"])
                    score = item.get(metric["code"], 0)
                    scoring_dict[name_child][dom_id]["subjects"][sub_id]["metrics"][
                        met_id
                    ] = {
                        "code": metric["code"],
                        "score": score,
                        "description": metric.get("original", ""),
                        "criteria": metric.get("criteria", []),
                    }
    return scoring_dict
