from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QColor

from gui.widgets.assessment.subject_block import SubjectBlock
from gui.widgets.score_toggle import ScoreToggle


class DomainBlock(QFrame):
    def __init__(self, domain_name, subjects):
        super().__init__()
        self.domain_name = domain_name
        self.subjects = subjects
        self.setObjectName("domain_block")

        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(0)

        title = QLabel(self.domain_name)
        score_toggle = ScoreToggle(size=18, spacing=2)
        score_toggle.setObjectName("domain_score_toggle")

        header_widget = QFrame()
        header_widget.setObjectName("domain_header")
        header_widget.setContentsMargins(0, 0, 0, 0)
        header_layout = QHBoxLayout(header_widget)
        header_layout.addWidget(title, stretch=1)
        header_layout.addWidget(score_toggle)

        body_layout = QVBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        for subject_name in self.subjects.keys():
            body_layout.addWidget(
                SubjectBlock(subject_name, self.subjects[subject_name])
            )

        layout.addWidget(header_widget)
        layout.addLayout(body_layout, stretch=1)
        layout.addStretch(1)

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)
