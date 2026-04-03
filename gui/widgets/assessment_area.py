from PySide6.QtWidgets import (
    QFrame,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from gui.widgets.score_toggle import ScoreToggle, ScoreButtonType
from gui.widgets.assessment.domain_block import DomainBlock
from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths
from gui.utils.icon_utils import get_svg_pixmap
from logic.assessment_tools import bulk_update, get_common_score_type


class AssessmentArea(QFrame):
    on_score_updated = Signal(str, dict)  # child_name, score_dict

    def __init__(self):
        super().__init__()
        self.child_name = ""
        self.score_dict = {}
        self.domain_blocks = {}
        self.is_expanded = False
        self.setObjectName("assessment_area")

        self.child_name_lbl = QLabel()
        self.child_name_lbl.setObjectName("child_name_lbl")

        self.expand_btn = QPushButton()
        self.expand_btn.setFixedSize(32, 32)
        self.expand_btn.clicked.connect(self.handle_expand)
        self.expand_btn.setObjectName("expand_btn")
        expand_icon = get_svg_pixmap(IconPaths.EXPAND, AppColors.BTN_ICON_TEXT, 16)
        self.expand_btn.setIcon(QIcon(expand_icon))

        score_toggle_lbl = QLabel("Жаппай бағалау:")
        score_toggle_lbl.setObjectName("score_toggle_lbl")
        self.score_toggle = ScoreToggle(
            btn_type=ScoreButtonType.BASE, size=20, spacing=2
        )
        self.score_toggle.scoreChanged.connect(self.on_bulk_score)
        score_toggle_layout = QHBoxLayout()
        score_toggle_layout.addWidget(score_toggle_lbl)
        score_toggle_layout.addWidget(self.score_toggle)
        score_toggle_frame = QFrame()
        score_toggle_frame.setObjectName("bulk_score_toggle_frame")
        score_toggle_frame.setLayout(score_toggle_layout)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.child_name_lbl, alignment=Qt.AlignTop)
        header_layout.addSpacing(10)
        header_layout.addWidget(self.expand_btn, alignment=Qt.AlignCenter)
        header_layout.addStretch()
        header_layout.addWidget(score_toggle_frame)
        header_frame = QFrame()
        header_frame.setObjectName("assessment_header")
        header_frame.setLayout(header_layout)

        # Create a ScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create a custom widget for your content
        self.scroll_content = QWidget()
        self.body_layout = QVBoxLayout(self.scroll_content)
        self.body_layout.setAlignment(Qt.AlignTop)

        # Setting content to ScrollArea
        self.scroll_area.setWidget(self.scroll_content)

        # Add to main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(header_frame)
        layout.addWidget(self.scroll_area)

    def _clear_domain_blocks(self):
        while self.body_layout.count():
            item = self.body_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
            del item
        self.domain_blocks.clear()

    def handle_expand(self):
        self.is_expanded = not self.is_expanded
        expand_icon = get_svg_pixmap(
            IconPaths.EXPAND if self.is_expanded else IconPaths.COLLAPSE,
            AppColors.BTN_ICON_TEXT,
            16,
        )
        self.expand_btn.setIcon(QIcon(expand_icon))

    def on_bulk_score(self, score):
        bulk_update(self.score_dict, score)
        for dn, domain_block in self.domain_blocks.items():
            domain_block.applyData(self.score_dict[dn])
        self.on_score_updated.emit(self.child_name, self.score_dict)

    def handle_child_update(self, dn, subjects):
        # Update self.score_togle state
        self.score_dict[dn] = subjects
        cmn_score = get_common_score_type(self.score_dict)
        self.score_toggle.set_score(cmn_score)
        # Send signal to parent
        self.on_score_updated.emit(self.child_name, self.score_dict)

    def applyChildData(self, child_name, score_dict):
        if not child_name or not score_dict:
            return

        self.child_name = child_name
        self.score_dict = score_dict
        self.child_name_lbl.setText(self.child_name)

        self._clear_domain_blocks()
        for domain_name, subjects in self.score_dict.items():
            domain_block = DomainBlock(domain_name, subjects)
            domain_block.on_score_updated.connect(self.handle_child_update)
            self.domain_blocks[domain_name] = domain_block
            self.body_layout.addWidget(domain_block)
        self.body_layout.addStretch()

        cmn_score = get_common_score_type(self.score_dict)
        self.score_toggle.set_score(cmn_score)
