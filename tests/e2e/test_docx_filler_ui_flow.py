from PySide6.QtWidgets import QApplication

from gui.pages.filler_page import FillerPage
import gui.steps.common.step_children_scores as step2_module
import gui.steps.common.step_file_export as step4_module
from tests.e2e.helpers import load_stylesheets, mock_ui_dialogs
from tests.e2e.test_config import filler_cfg as conf
from tests.e2e.step_assertions import (
    assert_step_file_select,
    assert_step_children_scores,
    assert_step_fill_setup,
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
def test_docx_filler_ui_flow(qtbot, monkeypatch, tmp_path):
    output_path = tmp_path / "filled_docx_output.docx"

    assert conf.xlsx_path.exists(), f"Мониторинг файлы жоқ: {conf.xlsx_path}"
    assert conf.temp_path.exists(), f"Шаблон жоқ: {conf.temp_path}"

    page = FillerPage(on_finish=lambda: None)
    qtbot.addWidget(page)
    assert load_stylesheets(
        QApplication.instance(),
        [
            "gui/resources/style/global.qss",
            "gui/resources/style/style.qss",
            "gui/resources/style/step1.qss",
        ],
    )
    page.show()
    qtbot.waitExposed(page)

    assert_step_file_select(
        qtbot, monkeypatch, page, conf.xlsx_path, conf.sheet_idx, conf.group_idx
    )

    assert_step_children_scores(
        qtbot, monkeypatch, page, step2_module, sync_worker=sync_worker
    )

    assert_step_fill_setup(
        qtbot, monkeypatch, page, conf.control_type_idx, conf.temp_path
    )

    assert_step_file_export(
        qtbot,
        monkeypatch,
        page,
        step4_module,
        sync_worker,
        output_path,
        conf.out_dir,
        conf.out_file_name,
    )
