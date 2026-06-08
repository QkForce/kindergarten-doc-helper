from gui.dialogs.name_dialog import NameDialog
from gui.widgets.settings.simple_list_item_widget import SimpleListItemWidget


class AgeGroupListItemWidget(SimpleListItemWidget):
    def create_edit_dialog(self):
        return NameDialog(self.name, "ЖАС ТОБЫН ӨЗГЕРТУ", self)
