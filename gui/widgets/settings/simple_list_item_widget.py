from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Signal

from gui.constants.icons import IconPaths
from gui.widgets.icon_button import IconButton
from gui.dialogs.name_dialog import NameDialog


class SimpleListItemWidget(QFrame):
    on_edit_signal = Signal(str, str)  # id, new name
    on_delete_signal = Signal(str)  # id

    def __init__(self, id, name, obj_name, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setObjectName(obj_name)
        self.setProperty("selected", "false")
        self.id = id
        self.name = name

        self.label = QLabel(self.name)
        self.label.setWordWrap(True)

        edit_btn = IconButton(IconPaths.EDIT, icon_size=12)
        edit_btn.setProperty("btn-type", "ghost")
        edit_btn.setFixedSize(20, 20)
        edit_btn.clicked.connect(self.start_edit)

        delete_btn = IconButton(IconPaths.TRASH, icon_size=12)
        delete_btn.setProperty("btn-type", "ghost")
        delete_btn.setFixedSize(16, 16)
        delete_btn.clicked.connect(lambda: self.on_delete_signal.emit(self.id))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addSpacing(0)
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)

    def start_edit(self):
        dialog = NameDialog(self.name, "АТАУДЫ ӨЗГЕРТУ", self)
        if dialog.exec() == dialog.Accepted:
            new_name = dialog.getText()
            if new_name:
                self.on_edit_signal.emit(self.id, new_name)

    def updateName(self, name):
        self.name = name
        self.label.setText(self.name)

    def setActive(self, is_active):
        self.setProperty("selected", "true" if is_active else "false")
        self.style().unpolish(self)
        self.style().polish(self)
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        self.update()
