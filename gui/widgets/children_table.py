from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QHeaderView,
)
from PySide6.QtCore import Qt


class ChildrenTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("children_table_widget")
        self.layout = QVBoxLayout(self)
        self.children_table = QTableWidget()
        self.children_table.verticalHeader().hide()
        self.children_table.setShowGrid(False)

        sub_title = QLabel("Табылған балалар тізімі:")
        sub_title.setProperty("lbl-level", "h3")

        self.layout.addWidget(sub_title)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.children_table)

    def set_data(self, children):
        self.children_table.clear()
        self.children_table.setRowCount(len(children))
        self.children_table.setColumnCount(2)
        self.children_table.setHorizontalHeaderLabels(["Реттік нөмері", "Аты-жөні"])
        for i, name in enumerate(children):
            self.children_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.children_table.setItem(i, 1, QTableWidgetItem(name))
        horizontal_header = self.children_table.horizontalHeader()
        horizontal_header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        horizontal_header.setStretchLastSection(True)
        horizontal_header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

    # def paintEvent(self, event):
    #     # This is essential for applying QSS to a bare QWidget subclass
    #     opt = QStyleOption()
    #     opt.initFrom(self)
    #     painter = QPainter(self)
    #     self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
    #     # Call the base paintEvent to ensure any child widgets are also painted
    #     super().paintEvent(event)
