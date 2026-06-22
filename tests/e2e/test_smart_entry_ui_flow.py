from gui.pages.smart_entry_page import SmartEntryPage
import gui.steps.step_child_assessment as step2_module
import gui.steps.common.step_file_export as step4_module
from tests.e2e.helpers import mock_ui_dialogs, sync_worker, init_test_page
from tests.e2e.test_config import smart_entry_cfg as conf
from tests.e2e.step_assertions import (
    assert_step_monitoring_config,
    assert_step_child_assessment,
    assert_step_file_export,
)


@mock_ui_dialogs
def test_smart_entry_ui_flow(qtbot, monkeypatch, tmp_path):
    output_path = tmp_path / "smart_entry_output.xlsx"
    monkeypatch.setattr(step2_module, "start_worker_task", sync_worker)
    monkeypatch.setattr(step4_module, "start_worker_task", sync_worker)

    assert conf.xlsx_path.exists(), f"Мониторинг файлы жоқ: {conf.xlsx_path}"

    page = init_test_page(
        qtbot,
        SmartEntryPage,
        [
            "gui/resources/style/global.qss",
            "gui/resources/style/style.qss",
            "gui/resources/style/step1.qss",
        ],
        conf,
        on_finish=lambda *args, **kwargs: None,
    )

    assert_step_monitoring_config(
        qtbot, monkeypatch, page, conf.xlsx_path, conf.sheet_idx, conf.group_idx
    )

    assert_step_child_assessment(
        qtbot,
        monkeypatch,
        page,
    )

    assert_step_file_export(
        qtbot,
        monkeypatch,
        page.get_step(2),
        output_path,
        conf.out_dir,
        conf.out_file_name,
    )
