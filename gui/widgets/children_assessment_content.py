from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt


class ChildrenAssessmentWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        self.selector = QFrame()
        # self.selector.childSelected.connect(self.load_child_scores)

        self.matrix_area = QFrame()

        layout.addWidget(self.selector)
        layout.addWidget(self.matrix_area, 1)

        self.setContentsMargins(0, 0, 0, 0)

    def set_data(self, children_names):
        print("Setting children names in selector:", children_names)
        # self.selector.set_data(children_names)

    def load_child_scores(self, name):
        pass
