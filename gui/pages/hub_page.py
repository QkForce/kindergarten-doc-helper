from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from gui.constants.colors import AppColors
from gui.widgets.feature_card import FeatureCard
from gui.widgets.icon_button import IconButton
from gui.constants.icons import IconPaths
from gui.constants.strings import AppStrings
from gui.utils.icon_utils import get_svg_pixmap
from gui.utils.style_utils import apply_shadow
from gui.dialogs.settings_dialog import SettingsDialog
from logic.config_store import load_config, save_config


class HubPage(QFrame):
    # Send navigation signals to MainWindow
    generator_requested = Signal()
    template_requested = Signal()
    entry_requested = Signal()
    monform_requested = Signal()
    growform_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("hub_page")
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        # Header
        logo_btn = QPushButton("K")
        logo_btn.setObjectName("breadcrumb_logo")
        logo_btn.setFixedSize(32, 32)
        apply_shadow(logo_btn, blur_radius=15, offset_y=4)

        logo_lbl = QLabel("KinderDoc")
        logo_lbl.setObjectName("logo_lbl")

        self.settings_btn = IconButton(IconPaths.SETTINGS)
        self.settings_btn.setFixedSize(32, 32)
        self.settings_btn.setObjectName("settings_btn")
        settings_icon = get_svg_pixmap(IconPaths.SETTINGS, AppColors.BTN_ICON_TEXT, 16)
        self.settings_btn.setIcon(QIcon(settings_icon))
        apply_shadow(self.settings_btn, blur_radius=15, offset_y=4)

        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_frame.setContentsMargins(0, 10, 0, 10)
        header_layout = QHBoxLayout(header_frame)
        header_layout.addWidget(logo_btn)
        header_layout.addWidget(logo_lbl, 0, Qt.AlignVCenter)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_btn, 0, Qt.AlignVCenter)

        # Title, subtitle
        title = QLabel(AppStrings.HUB_TITLE)
        title.setObjectName("hub_main_title")

        subtitle = QLabel(AppStrings.HUB_SUBTITLE)
        subtitle.setObjectName("hub_subtitle")

        # Cards Grid
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
        self.card_monform = FeatureCard(
            AppStrings.CARD_MONFORM_TITLE,
            AppStrings.CARD_MONFORM_DESC,
            IconPaths.FEATURE_MONFORM,
        )
        self.card_growform = FeatureCard(
            AppStrings.CARD_GROWFORM_TITLE,
            AppStrings.CARD_GROWFORM_DESC,
            IconPaths.FEATURE_GROWFORM,
        )

        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)
        cards_layout.setContentsMargins(10, 20, 10, 20)
        cards_layout.setAlignment(Qt.AlignCenter)
        cards_layout.addWidget(self.card_gen, 0, 0)
        cards_layout.addWidget(self.card_tpl, 0, 1)
        cards_layout.addWidget(self.card_entry, 0, 2)
        cards_layout.addWidget(self.card_monform, 1, 0)
        cards_layout.addWidget(self.card_growform, 1, 1)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 0, 10, 10)
        main_layout.addWidget(header_frame)
        main_layout.addSpacing(20)
        main_layout.addWidget(title, 0, Qt.AlignCenter)
        main_layout.addWidget(subtitle, 0, Qt.AlignCenter)
        main_layout.addSpacing(20)
        main_layout.addLayout(cards_layout)

    def connect_signals(self):
        self.settings_btn.clicked.connect(self.open_settings)
        # Connect card clicks to signals that MainWindow will listen to for navigation
        self.card_gen.clicked.connect(self.generator_requested.emit)
        self.card_tpl.clicked.connect(self.template_requested.emit)
        self.card_entry.clicked.connect(self.entry_requested.emit)
        self.card_monform.clicked.connect(self.monform_requested.emit)
        self.card_growform.clicked.connect(self.growform_requested.emit)

    def open_settings(self):
        settings = load_config()
        settings_dialog = SettingsDialog(settings=settings, parent=self)
        if settings_dialog.exec() == QDialog.Accepted:
            new_settings = settings_dialog.get_data()
            save_config(new_settings)
