from gui.pages.filler_page import FillerPage
import gui.steps.common.step_children_scores as step2_module
import gui.steps.common.step_file_export as step4_module
from tests.e2e.helpers import mock_ui_dialogs, sync_worker, init_test_page
from tests.e2e.test_config import filler_cfg as conf
from tests.e2e.step_assertions import (
    assert_step_monitoring_config,
    assert_step_children_scores,
    assert_step_fill_setup,
    assert_step_file_export,
)


@mock_ui_dialogs
def test_docx_filler_ui_flow(qtbot, monkeypatch, tmp_path):
    output_path = tmp_path / "filled_docx_output.docx"
    monkeypatch.setattr(step2_module, "start_worker_task", sync_worker)
    monkeypatch.setattr(step4_module, "start_worker_task", sync_worker)

    assert conf.xlsx_path.exists(), f"Мониторинг файлы жоқ: {conf.xlsx_path}"
    assert conf.temp_path.exists(), f"Шаблон жоқ: {conf.temp_path}"

    page = init_test_page(
        qtbot,
        FillerPage,
        [
            "gui/resources/style/global.qss",
            "gui/resources/style/style.qss",
            "gui/resources/style/step1.qss",
        ],
        conf,
        on_finish=lambda: None,
    )

    assert_step_monitoring_config(
        qtbot, monkeypatch, page, conf.xlsx_path, conf.sheet_idx, conf.group_idx
    )

    assert_step_children_scores(
        qtbot,
        monkeypatch,
        page,
    )

    assert_step_fill_setup(
        qtbot, monkeypatch, page, conf.control_type_idx, conf.temp_path
    )

    assert_step_file_export(
        qtbot,
        monkeypatch,
        page.get_step(3),
        output_path,
        conf.out_dir,
        conf.out_file_name,
    )
