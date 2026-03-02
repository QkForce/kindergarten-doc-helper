from PySide6.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal


class AssessmentArea(QScrollArea):
    on_score_updated = Signal(str, dict)

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        self.child_name = QLabel()
        self.child_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.child_name)

        main_layout = QVBoxLayout()

        layout.addLayout(header_layout)
        layout.addLayout(main_layout, stretch=1)
        layout.addStretch(1)

    def updateChild(self, child_name, scoring_dict):
        self.child_name.setText(f"{child_name} үшін бағалау матрицасы жүктелуде...")
