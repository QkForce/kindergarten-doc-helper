from config.metrics_schema_new import METRICS_SCHEMA


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
    score_types = set()
    for subjects in score_dict.values():
        for metrics in subjects.values():
            for score in metrics:
                if score is not None:
                    score_types.add(score)
    return score_types.pop() if len(score_types) == 1 else 0


def get_domain_score_type(subjects):
    score_types = set()
    for metrics in subjects.values():
        for score in metrics.values():
            if score is not None:
                score_types.add(score)
    return score_types.pop() if len(score_types) == 1 else 0


def get_subject_score_type(metrics):
    score_types = set()
    for score in metrics.values():
        if score is not None:
            score_types.add(score)
    return score_types.pop() if len(score_types) == 1 else 0


def create_default_scoring_dict(age_group):
    scoring_dict = {
        domain: {
            subject: {metric: None for metric in metrics}
            for subject, metrics in subjects.items()
        }
        for domain, subjects in METRICS_SCHEMA[age_group].items()
    }
    return scoring_dict
