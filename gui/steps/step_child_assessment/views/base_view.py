from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Signal


class BaseView(QFrame):
    on_scores_updated = Signal(dict)  # child_name -> score_dict

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("base_view_widget")

    def applyData(self, children_scores):
        raise NotImplementedError("Subclasses must implement applyData method.")
