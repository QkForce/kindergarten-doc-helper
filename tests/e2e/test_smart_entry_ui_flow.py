from PySide6.QtWidgets import QApplication

from gui.pages.smart_entry_page import SmartEntryPage
import gui.steps.step_child_assessment as step2_module
import gui.steps.common.step_file_export as step4_module
from tests.e2e.helpers import load_stylesheets, mock_ui_dialogs, init_test_page
from tests.e2e.test_config import smart_entry_cfg as conf
from tests.e2e.step_assertions import (
    assert_step_file_select,
    assert_step_child_assessment,
    assert_step_file_export,
)


def sync_worker(task_function, finished_slot, error_slot):
    try:
        print("\n[WORKER] Тапсырма орындалуда...")
        result = task_function()
        print("[WORKER] Тапсырма сәтті аяқталды!")
        finished_slot(result)
    except Exception as exc:
        print(f"\n❌ [CRITICAL WORKER ERROR]: {exc}")
        error_slot(str(exc))
        raise exc


@mock_ui_dialogs
def test_smart_entry_ui_flow(qtbot, monkeypatch, tmp_path):
    output_path = tmp_path / "smart_entry_output.xlsx"

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

    assert_step_file_select(
        qtbot, monkeypatch, page, conf.xlsx_path, conf.sheet_idx, conf.group_idx
    )

    assert_step_child_assessment(
        qtbot,
        monkeypatch,
        page,
        step2_module,
        sync_worker,
    )

    assert_step_file_export(
        qtbot,
        monkeypatch,
        page.get_step(2),
        step4_module,
        sync_worker,
        output_path,
        conf.out_dir,
        conf.out_file_name,
    )
