from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QButtonGroup
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon

from gui.constants.colors import AppColors
from gui.utils.icon_utils import get_svg_pixmap


class SegmentedControl(QFrame):
    on_option_changed = Signal(int)  # id of the selected option (0-based index)

    def __init__(
        self,
        options: list[tuple[str, str | None]],
        default_index: int = 0,
        parent=None,
    ):
        """
        options format: [("btn_label", "icon/path.svg"), ...]
        """
        super().__init__(parent)
        self.setObjectName("segmented_control")

        self._buttons: list[QPushButton] = []
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)

        self.setup_ui(options)
        self.set_selected_index(default_index)

    def setup_ui(self, options: list[tuple[str, str | None]]):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(4)

        for idx, (title, icon_path) in enumerate(options):
            btn = QPushButton(f" {title}", self)
            btn.setObjectName("segment_button")
            btn.setCheckable(True)
            btn.setFlat(True)
            if icon_path:
                pixmap = get_svg_pixmap(icon_path, AppColors.PRIMARY, 14)
                btn.setIcon(QIcon(pixmap))

            self._group.addButton(btn, idx)
            layout.addWidget(btn)
            self._buttons.append(btn)
        self._group.idClicked.connect(self.on_option_changed.emit)

    def set_selected_index(self, index: int):
        if 0 <= index < len(self._buttons):
            self._buttons[index].setChecked(True)

    def selected_index(self) -> int:
        return self._group.checkedId()
