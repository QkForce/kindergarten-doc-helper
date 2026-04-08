from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal

from gui.widgets.feature_card import FeatureCard
from gui.constants.icons import IconPaths
from gui.constants.strings import AppStrings


class HubPage(QFrame):
    # Send navigation signals to MainWindow
    generator_requested = Signal()
    template_requested = Signal()
    entry_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("hub_page")

        # 1. Header
        logo_btn = QPushButton("K")
        logo_btn.setObjectName("breadcrumb_logo")
        logo_btn.setFixedSize(32, 32)

        logo_lbl = QLabel("KinderDoc")
        logo_lbl.setObjectName("logo_lbl")

        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_frame.setContentsMargins(0, 10, 0, 10)
        header_layout = QHBoxLayout(header_frame)
        header_layout.addWidget(logo_btn)
        header_layout.addWidget(logo_lbl, 0, Qt.AlignVCenter)

        title = QLabel(AppStrings.HUB_TITLE)
        title.setObjectName("hub_main_title")

        subtitle = QLabel(AppStrings.HUB_SUBTITLE)
        subtitle.setObjectName("hub_subtitle")

        # 2. Cards Grid
        self.card_gen = FeatureCard(
            AppStrings.CARD_GEN_TITLE,
            AppStrings.CARD_GEN_DESC,
            IconPaths.FEATURE_DOCX_GENERATOR,
        )
        self.card_tpl = FeatureCard(
            AppStrings.CARD_TPL_TITLE,
            AppStrings.CARD_TPL_DESC,
            IconPaths.FEATURE_TEMPLATE_FILLER,
        )
        self.card_entry = FeatureCard(
            AppStrings.CARD_ENTRY_TITLE,
            AppStrings.CARD_ENTRY_DESC,
            IconPaths.FEATURE_ENTRY_XLSX,
        )

        cards_layout = QHBoxLayout()
        cards_layout.setContentsMargins(10, 20, 10, 20)
        cards_layout.addWidget(self.card_gen)
        cards_layout.addWidget(self.card_tpl)
        cards_layout.addWidget(self.card_entry)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 0, 10, 10)
        main_layout.addWidget(header_frame)
        main_layout.setSpacing(20)
        main_layout.addWidget(title, 0, Qt.AlignCenter)
        main_layout.addWidget(subtitle, 0, Qt.AlignCenter)
        main_layout.addSpacing(20)
        main_layout.addLayout(cards_layout, 0)
        main_layout.addStretch()

        # Connect card clicks to signals that MainWindow will listen to for navigation
        self.card_gen.clicked.connect(self.generator_requested.emit)
        self.card_tpl.clicked.connect(self.template_requested.emit)
        self.card_entry.clicked.connect(self.entry_requested.emit)
