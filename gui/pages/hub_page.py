from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal
from gui.widgets.feature_card import FeatureCard


class HubPage(QWidget):
    # Send navigation signals to MainWindow
    generator_requested = Signal()
    template_requested = Signal()
    entry_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("hub_page")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 80)

        # 1. Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)

        title = QLabel("KinderDoc Helper")
        title.setObjectName("hub_main_title")

        subtitle = QLabel("Automated document workflows for modern educators.")
        subtitle.setObjectName("hub_subtitle")

        header_layout.addWidget(title, 0, Qt.AlignCenter)
        header_layout.addWidget(subtitle, 0, Qt.AlignCenter)
        main_layout.addLayout(header_layout)

        main_layout.addSpacing(60)

        # 2. Cards Grid
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(25)

        self.card_gen = FeatureCard(
            "Document Generator",
            "Build DOCX files from scratch using XLSX source data.",
            "📄",
        )
        self.card_tpl = FeatureCard(
            "Template Filler",
            "Auto-fill existing Word templates with Excel variables.",
            "✏️",
        )
        self.card_entry = FeatureCard(
            "Smart Entry", "Create student data tables with an intuitive grid.", "📊"
        )

        cards_layout.addWidget(self.card_gen)
        cards_layout.addWidget(self.card_tpl)
        cards_layout.addWidget(self.card_entry)

        main_layout.addLayout(cards_layout)

        # Connect card clicks to signals that MainWindow will listen to for navigation
        self.card_gen.clicked.connect(self.generator_requested.emit)
        self.card_tpl.clicked.connect(self.template_requested.emit)
        self.card_entry.clicked.connect(self.entry_requested.emit)
