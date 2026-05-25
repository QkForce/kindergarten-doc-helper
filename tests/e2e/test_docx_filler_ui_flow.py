import shutil
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication

from gui.pages.filler_page import FillerPage
import gui.steps.common.step_children_scores as step2_module
import gui.steps.common.step_file_export as step4_module
from tests.e2e.helpers import mock_file_dialog, wait_until_visible, load_stylesheets
from tests.e2e.test_config import filler_cfg as conf


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

    # --- CHEATING UI DIALOGS ---
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: None)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: None)
    monkeypatch.setattr(QMessageBox, "critical", lambda *args, **kwargs: None)

    # =========================================================================
    # STEP-1: Select xlsx file
    # =========================================================================
    step1 = page.get_step(0)
    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", mock_file_dialog(conf.xlsx_path)
    )
    QTest.mouseClick(step1.file_select_widget.btn_browse, Qt.LeftButton)

    qtbot.waitUntil(lambda: step1.combo_sheet.count() > 0, timeout=15000)
    step1.combo_sheet.setCurrentIndex(conf.sheet_idx)
    step1.combo_group.setCurrentIndex(conf.group_idx)

    assert page.btn_next.isEnabled(), "STEP-1: 'Келесі' батырмасы белсенді емес!"
    QTest.mouseClick(page.btn_next, Qt.LeftButton)
    QApplication.processEvents()

    # =========================================================================
    # STEP-2: Load children scores
    # =========================================================================
    step2 = page.get_step(1)
    assert step2 is not None, "STEP-2 виджеті табылмады"

    qtbot.waitUntil(lambda: step2.isVisible(), timeout=5000)
    QApplication.processEvents()

    monkeypatch.setattr(step2_module, "start_worker_task", sync_worker)
    step2.run_auto_load()

    check_step2_visible = wait_until_visible(lambda: step2.content_widget.isVisible())
    qtbot.waitUntil(check_step2_visible, timeout=15000)

    assert page.btn_next.isEnabled(), "STEP-2: 'Келесі' батырмасы белсенді емес!"
    QTest.mouseClick(page.btn_next, Qt.LeftButton)
    QApplication.processEvents()

    # =========================================================================
    # STEP-3: Select docx template
    # =========================================================================
    step3 = page.get_step(2)
    assert step3 is not None, "STEP-3 виджеті табылмады"
    qtbot.waitUntil(lambda: step3.isVisible(), timeout=5000)

    step3.combo_control_types.setCurrentIndex(conf.control_type_idx)

    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", mock_file_dialog(conf.temp_path)
    )
    QTest.mouseClick(step3.file_select_widget.btn_browse, Qt.LeftButton)
    QApplication.processEvents()

    qtbot.waitUntil(lambda: page.btn_next.isEnabled(), timeout=5000)
    assert (
        page.btn_next.isEnabled()
    ), "STEP-3: Даму картасы файлы таңдалмады немесе 'Келесі' батырмасы бұғаттаулы!"

    QTest.mouseClick(page.btn_next, Qt.LeftButton)
    QApplication.processEvents()

    # =========================================================================
    # STEP-4: Export and Save result
    # =========================================================================
    step4 = page.get_step(3)
    assert step4 is not None, "STEP-4 виджеті табылмады"

    qtbot.waitUntil(lambda: step4.isVisible(), timeout=5000)
    QApplication.processEvents()

    monkeypatch.setattr(step4_module, "start_worker_task", sync_worker)
    step4.run_auto_load()

    check_step4_ready = wait_until_visible(lambda: step4.btn_save.isVisible())
    qtbot.waitUntil(check_step4_ready, timeout=15000)
    assert not any(
        str(x).strip() for x in step4.last_error
    ), f"STEP-4: Экспорт қатемен аяқталған: {step4.last_error}"
    assert step4.result_file is not None, "STEP-4: result_file айнымалысы бос!"

    monkeypatch.setattr(QFileDialog, "getSaveFileName", mock_file_dialog(output_path))
    QTest.mouseClick(step4.btn_save, Qt.LeftButton)
    QApplication.processEvents()

    # Check the result
    qtbot.waitUntil(lambda: output_path.exists(), timeout=5000)
    assert output_path.stat().st_size > 0

    conf.out_dir.mkdir(parents=True, exist_ok=True)
    destination = conf.out_dir / "docx_filler_result.docx"
    shutil.copy(output_path, destination)
    print(f"\n📁 The test result is saved to this direction: {destination}")
