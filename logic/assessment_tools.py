from config.metrics_schema_new import METRICS_SCHEMA


def set_score(score_dict, domain=None, subject=None, metric=None, score=None):
    for d_key, subjects in score_dict.items():
        if not domain or d_key == domain:
            for s_key, metrics in subjects.items():
                if not subject or s_key == subject:
                    for m_key in metrics:
                        if not metric or m_key == metric:
                            metrics[m_key] = score


def create_default_scoring_dict(age_group):
    scoring_dict = {
        domain: {
            subject: {metric: None for metric in metrics}
            for subject, metrics in subjects.items()
        }
        for domain, subjects in METRICS_SCHEMA[age_group].items()
    }
    return scoring_dict
