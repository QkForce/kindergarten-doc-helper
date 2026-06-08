from gui.dialogs.domain_dialog import DomainDialog
from gui.widgets.settings.simple_list_item_widget import SimpleListItemWidget


class DomainListItemWidget(SimpleListItemWidget):
    def __init__(
        self, id, name, placeholder_key, obj_name, on_edit, on_delete, parent=None
    ):
        super().__init__(id, name, obj_name, on_edit, on_delete, parent)
        self.placeholder_key = placeholder_key

    def create_edit_dialog(self):
        return DomainDialog(self.name, self.placeholder_key, "БАҒЫТТЫ ӨЗГЕРТУ", self)

    def updateData(self, data):
        self.name = data["name"]
        self.placeholder_key = data["placeholder_key"]
        self.label.setText(self.name)
