from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel

from gui.widgets.score_toggle import ScoreToggle


class DomainBlock(QFrame):
    def __init__(self, domain_name, subjects):
        super().__init__()
        self.domain_name = domain_name
        self.subjects = subjects

        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)

        title = QLabel(self.domain_name)
        score_toggle = ScoreToggle(size=20, spacing=2)

        header_layout = QHBoxLayout()
        header_layout.addWidget(title, stretch=1)
        header_layout.addWidget(score_toggle)

        body_layout = QVBoxLayout()

        layout.addLayout(header_layout)
        layout.addLayout(body_layout, stretch=1)
        layout.addStretch(1)
