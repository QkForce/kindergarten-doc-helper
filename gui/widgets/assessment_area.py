from PySide6.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal

from gui.widgets.score_toggle import ScoreToggle


class AssessmentArea(QScrollArea):
    on_score_updated = Signal(str, dict)

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        self.child_name = QLabel()
        self.child_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.score_toggle = ScoreToggle(size=20, spacing=2)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.child_name, stretch=1)
        header_layout.addWidget(self.score_toggle)

        main_layout = QVBoxLayout()

        layout.addLayout(header_layout)
        layout.addLayout(main_layout, stretch=1)
        layout.addStretch(1)

    def updateChild(self, child_name, scoring_dict):
        self.child_name.setText(f"{child_name} үшін бағалау матрицасы жүктелуде...")
