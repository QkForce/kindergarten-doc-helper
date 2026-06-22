from gui.pages.growform_page import GrowFormPage
import gui.steps.common.step_file_export as step_file_export_module
from tests.e2e.helpers import mock_ui_dialogs, sync_worker, init_test_page
from tests.e2e.test_config import growform_cfg as conf
from tests.e2e.step_assertions import (
    assert_step_file_select,
    assert_step_file_export,
)


@mock_ui_dialogs
def test_growform_ui_flow(qtbot, monkeypatch, tmp_path):
    output_path = tmp_path / "growform_output.docx"
    monkeypatch.setattr(step_file_export_module, "start_worker_task", sync_worker)

    assert (
        conf.grow_card_path.exists()
    ), f"Даму картасы файлы жоқ: {conf.grow_card_path}"

    page = init_test_page(
        qtbot,
        GrowFormPage,
        [
            "gui/resources/style/global.qss",
            "gui/resources/style/style.qss",
            "gui/resources/style/step1.qss",
        ],
        conf,
        on_finish=lambda: None,
    )

    assert_step_file_select(
        qtbot,
        monkeypatch,
        page.get_step(0),
        page,
        conf.grow_card_path,
    )

    assert_step_file_export(
        qtbot,
        monkeypatch,
        page.get_step(1),
        output_path,
        conf.out_dir,
        conf.out_file_name,
    )
