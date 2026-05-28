import shutil

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QFileDialog, QApplication

from tests.e2e.helpers import mock_file_dialog, wait_until_visible


def assert_step_file_select(qtbot, monkeypatch, page, xlsx_path, sheet_idx, group_idx):
    step1 = page.get_step(0)
    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_file_dialog(xlsx_path))
    QTest.mouseClick(step1.file_select_widget.btn_browse, Qt.LeftButton)

    qtbot.waitUntil(lambda: step1.combo_sheet.count() > 0, timeout=15000)
    step1.combo_sheet.setCurrentIndex(sheet_idx)
    step1.combo_group.setCurrentIndex(group_idx)

    assert (
        page.btn_next.isEnabled()
    ), "step_file_select: 'Келесі' батырмасы белсенді емес!"
    QTest.mouseClick(page.btn_next, Qt.LeftButton)
    QApplication.processEvents()


def assert_step_children_scores(qtbot, monkeypatch, page, step_module, sync_worker):
    step2 = page.get_step(1)
    assert step2 is not None, "step_children_scores виджеті табылмады"

    qtbot.waitUntil(lambda: step2.isVisible(), timeout=5000)
    QApplication.processEvents()

    monkeypatch.setattr(step_module, "start_worker_task", sync_worker)
    step2.run_auto_load()

    check_step2_visible = wait_until_visible(lambda: step2.content_widget.isVisible())
    qtbot.waitUntil(check_step2_visible, timeout=15000)

    assert (
        page.btn_next.isEnabled()
    ), "step_children_scores: 'Келесі' батырмасы белсенді емес!"
    QTest.mouseClick(page.btn_next, Qt.LeftButton)
    QApplication.processEvents()


def assert_step_fill_setup(qtbot, monkeypatch, page, control_type_idx, temp_path):
    step3 = page.get_step(2)
    assert step3 is not None, "step_fill_setup виджеті табылмады"
    qtbot.waitUntil(lambda: step3.isVisible(), timeout=5000)

    step3.combo_control_types.setCurrentIndex(control_type_idx)

    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_file_dialog(temp_path))
    QTest.mouseClick(step3.file_select_widget.btn_browse, Qt.LeftButton)
    QApplication.processEvents()

    qtbot.waitUntil(lambda: page.btn_next.isEnabled(), timeout=5000)
    assert (
        page.btn_next.isEnabled()
    ), "step_fill_setup: Даму картасы файлы таңдалмады немесе 'Келесі' батырмасы бұғаттаулы!"

    QTest.mouseClick(page.btn_next, Qt.LeftButton)
    QApplication.processEvents()


def assert_step_docx_template(qtbot, monkeypatch, page, temp_path):
    step3 = page.get_step(2)
    assert step3 is not None, "step_docx_template виджеті табылмады"
    qtbot.waitUntil(lambda: step3.isVisible(), timeout=5000)

    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_file_dialog(temp_path))
    QTest.mouseClick(step3.file_select_widget.btn_browse, Qt.LeftButton)
    QApplication.processEvents()

    qtbot.waitUntil(lambda: page.btn_next.isEnabled(), timeout=5000)
    assert (
        page.btn_next.isEnabled()
    ), "step_docx_template: Шаблон таңдалмады немесе 'Келесі' батырмасы бұғаттаулы!"

    QTest.mouseClick(page.btn_next, Qt.LeftButton)
    QApplication.processEvents()


def assert_step_file_export(
    qtbot,
    monkeypatch,
    step,
    step_module,
    sync_worker,
    output_path,
    out_dir,
    result_file_name: str,
):
    assert step is not None, "step_file_export виджеті табылмады"

    qtbot.waitUntil(lambda: step.isVisible(), timeout=5000)
    QApplication.processEvents()

    monkeypatch.setattr(step_module, "start_worker_task", sync_worker)
    step.run_auto_load()

    check_step_ready = wait_until_visible(lambda: step.btn_save.isVisible())
    qtbot.waitUntil(check_step_ready, timeout=15000)
    assert not any(
        str(x).strip() for x in step.last_error
    ), f"step_file_export: Экспорт қатемен аяқталған: {step.last_error}"
    assert step.result_file is not None, "step_file_export: result_file айнымалысы бос!"

    monkeypatch.setattr(QFileDialog, "getSaveFileName", mock_file_dialog(output_path))
    QTest.mouseClick(step.btn_save, Qt.LeftButton)
    QApplication.processEvents()

    # Check the result
    qtbot.waitUntil(lambda: output_path.exists(), timeout=5000)
    assert output_path.stat().st_size > 0

    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / result_file_name
    shutil.copy(output_path, destination)
    print(f"\n📁 The test result is saved to this direction: {destination}")
