from PySide6.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal


class AssessmentArea(QScrollArea):
    on_score_updated = Signal(str, dict)

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        self.child_name = QLabel("Матрица бағалау интерфейсі әзірленуде.")
        self.child_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.child_name)

    def updateChild(self, child_name, scoring_dict):
        self.child_name.setText(f"{child_name} үшін бағалау матрицасы жүктелуде...")
