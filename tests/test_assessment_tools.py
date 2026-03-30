from unittest.mock import patch

from gui.widgets.items.child_item import AssessmentStatus
from logic.assessment_tools import (
    bulk_update,
    create_default_scoring_dict,
    create_source_scoring_dict,
    get_assessment_status,
    set_metrics_score,
    set_subjects_score,
)

# create_default_scoring_dict / create_source_scoring_dict үшін шағын схема (нақты METRICS_SCHEMA үлкен)
_MINIMAL_METRICS_SCHEMA = {
    "test_age": {
        "domain_a": {
            "subj_1": {
                "code-a": {"original": "a", "transformed": "A"},
                "code-b": {"original": "b", "transformed": "B"},
            },
        },
    },
}


def test_bulk_update():
    domains = {
        "domain1": {
            "subject1": {
                "metric1": 1,
                "metric2": 2,
            },
            "subject2": {
                "metric3": 1,
                "metric4": 2,
            },
        },
        "domain2": {
            "subject3": {
                "metric5": 1,
                "metric6": 2,
            },
            "subject4": {
                "metric7": 1,
                "metric8": 2,
            },
        },
    }
    score = 3
    bulk_update(domains, score)
    expected_domains = {
        "domain1": {
            "subject1": {"metric1": 3, "metric2": 3},
            "subject2": {"metric3": 3, "metric4": 3},
        },
        "domain2": {
            "subject3": {"metric5": 3, "metric6": 3},
            "subject4": {"metric7": 3, "metric8": 3},
        },
    }
    assert domains == expected_domains


def test_set_subjects_score():
    subjects = {
        "subject1": {"metric1": 1, "metric2": 2},
        "subject2": {"metric3": 1, "metric4": 2},
    }
    score = 3
    set_subjects_score(subjects, score)
    expected_subjects = {
        "subject1": {"metric1": 3, "metric2": 3},
        "subject2": {"metric3": 3, "metric4": 3},
    }
    assert subjects == expected_subjects


def test_set_metrics_score():
    metrics = {"metric1": 1, "metric2": 2}
    score = 3
    set_metrics_score(metrics, score)
    expected_metrics = {"metric1": 3, "metric2": 3}
    assert metrics == expected_metrics


def test_get_assessment_status_not_started():
    score_dict = {
        "d1": {"s1": {"m1": 0, "m2": 0}},
    }
    assert get_assessment_status(score_dict) == AssessmentStatus.NOT_STARTED


def test_get_assessment_status_in_progress():
    score_dict = {
        "d1": {"s1": {"m1": 1, "m2": 0}},
    }
    assert get_assessment_status(score_dict) == AssessmentStatus.IN_PROGRESS


def test_get_assessment_status_completed():
    score_dict = {
        "d1": {"s1": {"m1": 1, "m2": 2}},
        "d2": {"s2": {"m3": 3}},
    }
    assert get_assessment_status(score_dict) == AssessmentStatus.COMPLETED


@patch("logic.assessment_tools.METRICS_SCHEMA", _MINIMAL_METRICS_SCHEMA)
def test_create_default_scoring_dict():
    result = create_default_scoring_dict("test_age")
    assert result == {
        "domain_a": {
            "subj_1": {"code-a": 0, "code-b": 0},
        },
    }


@patch("logic.assessment_tools.METRICS_SCHEMA", _MINIMAL_METRICS_SCHEMA)
def test_create_source_scoring_dict():
    scores = [
        {
            "name": "Бала 1",
            "code-a": 2,
            # code-b жоқ — 0 болуы керек
        },
    ]
    result = create_source_scoring_dict("test_age", scores)
    assert result == {
        "Бала 1": {
            "domain_a": {
                "subj_1": {"code-a": 2, "code-b": 0},
            },
        },
    }


@patch("logic.assessment_tools.METRICS_SCHEMA", _MINIMAL_METRICS_SCHEMA)
def test_create_source_scoring_dict_multiple_children():
    scores = [
        {"name": "A", "code-a": 1},
        {"name": "B", "code-b": 3},
    ]
    result = create_source_scoring_dict("test_age", scores)
    assert result["A"]["domain_a"]["subj_1"] == {"code-a": 1, "code-b": 0}
    assert result["B"]["domain_a"]["subj_1"] == {"code-a": 0, "code-b": 3}
