from PySide6.QtCore import Qt

from gui.dialogs.name_dialog import NameDialog
from gui.widgets.settings.simple_list_item_widget import SimpleListItemWidget


class AgeGroupListItemWidget(SimpleListItemWidget):
    def create_edit_dialog(self):
        dialog = NameDialog(self.name, "ЖАС ТОБЫН ӨЗГЕРТУ")
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        return dialog
