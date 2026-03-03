def set_score(score_dict, domain=None, subject=None, metric=None, score=None):
    for d_key, subjects in score_dict.items():
        if not domain or d_key == domain:
            for s_key, metrics in subjects.items():
                if not subject or s_key == subject:
                    for m_key in metrics:
                        if not metric or m_key == metric:
                            metrics[m_key] = score
