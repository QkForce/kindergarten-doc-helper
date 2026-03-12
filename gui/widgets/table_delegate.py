from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPainter, QPen, QBrush

from gui.constants.colors import AppColors

CELL_WIDTH = 30
CELL_HEIGHT = 30


class ScoreCellDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # UserRole-ден мәнді аламыз (ұпайлар үшін 1,2,3; аты-жөні үшін None болуы мүмкін)
        score = index.data(Qt.UserRole)
        text = str(index.data(Qt.DisplayRole) or "")

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. Горизонталь сызық (Екі кестеге де ортақ)
        line_pen = QPen(QColor(AppColors.BORDER), 0.5)
        painter.setPen(line_pen)
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

        # 2. Мазмұнды салу (Content)
        if isinstance(score, int) and score > 0:
            # Бұл - ҰПАЙЛАР (Шаршы салу логикасы)
            margin = 5
            rect = option.rect.adjusted(margin, margin, -margin, -margin)

            style_map = {
                1: {
                    "bg": AppColors.SOFT_RED_BG,
                    "border": AppColors.SOFT_RED_BORDER,
                    "text": AppColors.SCORE_LOW_TEXT,
                },
                2: {
                    "bg": AppColors.SOFT_YELLOW_BG,
                    "border": AppColors.SOFT_YELLOW_BORDER,
                    "text": AppColors.SCORE_MID_TEXT,
                },
                3: {
                    "bg": AppColors.SOFT_GREEN_BG,
                    "border": AppColors.SOFT_GREEN_BORDER,
                    "text": AppColors.SCORE_HIGH_TEXT,
                },
            }

            style = style_map.get(score)
            if style:
                bg_color = QColor(style["bg"])
                if option.state & QStyle.State_Selected:
                    bg_color = QColor(AppColors.CELL_SELECTED_BG)

                painter.setBrush(QBrush(bg_color))
                painter.setPen(QPen(QColor(style["border"]), 1))
                painter.drawRoundedRect(rect, 4, 4)

                painter.setPen(QColor(style["text"]))
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)
                painter.drawText(rect, Qt.AlignCenter, text)
        else:
            # Бұл - БАЛАЛАРДЫҢ АТЫ-ЖӨНІ (Тек мәтін)
            rect = option.rect.adjusted(
                10, 0, -10, 0
            )  # Сол жақтан аздап шегініс (padding)

            if option.state & QStyle.State_Selected:
                painter.fillRect(option.rect, QColor(AppColors.CELL_SELECTED_BG))

            painter.setPen(QColor(AppColors.TEXT_MAIN))
            painter.drawText(rect, Qt.AlignVCenter | Qt.AlignLeft, text)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(CELL_WIDTH, CELL_HEIGHT)
