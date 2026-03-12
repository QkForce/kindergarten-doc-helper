from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPainter, QPen, QBrush

from gui.constants.colors import AppColors


class ScoreCellDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        score = index.data(Qt.UserRole)
        text = str(index.data(Qt.DisplayRole) or "")

        style_map = {
            1: {
                "bg": AppColors.SOFT_GREEN_BG,
                "border": AppColors.SOFT_GREEN_BORDER,
                "text": AppColors.SCORE_HIGH_TEXT,
            },
            2: {
                "bg": AppColors.SOFT_YELLOW_BG,
                "border": AppColors.SOFT_YELLOW_BORDER,
                "text": AppColors.SCORE_MID_TEXT,
            },
            3: {
                "bg": AppColors.SOFT_RED_BG,
                "border": AppColors.SOFT_RED_BORDER,
                "text": AppColors.SCORE_LOW_TEXT,
            },
        }

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        rect = option.rect.adjusted(3, 3, -3, -3)

        if score in style_map:
            style = style_map[score]

            # 1. Фонды бояу
            bg_color = QColor(style["bg"])
            if option.state & QStyle.State_Selected:
                bg_color = QColor(AppColors.CELL_SELECTED_BG)

            painter.setBrush(QBrush(bg_color))

            # 2. Жиекті (Border) салу
            painter.setPen(QPen(QColor(style["border"]), 1))
            painter.drawRoundedRect(rect, 5, 5)

            # 3. Мәтінді жазу
            painter.setPen(QColor(style["text"]))
            # Қалыңдықты реттеу (қажет болса)
            font = painter.font()
            font.setBold(True)
            painter.setFont(font)

            painter.drawText(rect, Qt.AlignCenter, text)
        else:
            # Баға жоқ болса - стандартты Sidebar фоны
            painter.setBrush(QBrush(QColor(AppColors.SIDEBAR)))
            painter.setPen(QPen(QColor(AppColors.BORDER), 1))
            painter.drawRoundedRect(rect, 5, 5)
            painter.drawText(rect, Qt.AlignCenter, text)

        painter.restore()

        def sizeHint(self, option, index):
            return QSize(45, 45)
