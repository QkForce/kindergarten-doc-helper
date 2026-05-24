import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication

from gui.pages.generator_page import GeneratorPage
import gui.steps.common.step_children_scores as step2_module
import gui.steps.common.step_file_export as step4_module
from tests.e2e.helpers import mock_file_dialog, wait_until_visible


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


def test_docx_generator_ui_flow(qtbot, monkeypatch, tmp_path):
    excel_path = Path(os.getenv("TEST_UIE2E_DOCXGEN_XLSX_PATH"))
    template_path = Path(os.getenv("TEST_UIE2E_DOCXGEN_TEMP_PATH"))
    output_path = tmp_path / "generated_docx_output.docx"

    assert excel_path.exists(), f"Мониторинг файлы жоқ: {excel_path}"
    assert template_path.exists(), f"Шаблон жоқ: {template_path}"

    page = GeneratorPage(on_finish=lambda: None)
    qtbot.addWidget(page)
    page.show()
    qtbot.waitExposed(page)

    # --- CHEATING UI DIALOGS ---
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: None)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: None)
    monkeypatch.setattr(QMessageBox, "critical", lambda *args, **kwargs: None)

    # =========================================================================
    # STEP-1: Select xlsx file
    # =========================================================================
    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_file_dialog(excel_path))
    step1 = page.get_step(0)
    QTest.mouseClick(step1.file_select_widget.btn_browse, Qt.LeftButton)

    qtbot.waitUntil(lambda: step1.combo_sheet.count() > 0, timeout=15000)
    step1.combo_sheet.setCurrentIndex(int(os.getenv("TEST_UIE2E_DOCXGEN_SHEET_IDX")))
    step1.combo_group.setCurrentIndex(int(os.getenv("TEST_UIE2E_DOCXGEN_AGEGROUP_IDX")))

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
    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_file_dialog(template_path))
    step3 = page.get_step(2)
    assert step3 is not None, "STEP-3 виджеті табылмады"
    qtbot.waitUntil(lambda: step3.isVisible(), timeout=5000)

    QTest.mouseClick(step3.file_select_widget.btn_browse, Qt.LeftButton)
    QApplication.processEvents()

    qtbot.wait(500)
    assert (
        page.btn_next.isEnabled()
    ), "STEP-3: Шаблон таңдалмады немесе 'Келесі' батырмасы бұғаттаулы!"

    QTest.mouseClick(page.btn_next, Qt.LeftButton)
    QApplication.processEvents()

    # =========================================================================
    # STEP-4: Export and Save result
    # =========================================================================
    monkeypatch.setattr(QFileDialog, "getSaveFileName", mock_file_dialog(output_path))
    step4 = page.get_step(3)
    assert step4 is not None, "STEP-4 виджеті табылмады"

    qtbot.waitUntil(lambda: step4.isVisible(), timeout=5000)
    QApplication.processEvents()

    monkeypatch.setattr(step4_module, "start_worker_task", sync_worker)
    step4.run_auto_load()

    check_step4_ready = wait_until_visible(lambda: step4.btn_save.isVisible())
    qtbot.waitUntil(check_step4_ready, timeout=15000)

    QTest.mouseClick(step4.btn_save, Qt.LeftButton)
    QApplication.processEvents()

    # Check the result
    qtbot.waitUntil(lambda: output_path.exists(), timeout=5000)
    assert output_path.stat().st_size > 0
