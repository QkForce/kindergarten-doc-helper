from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QAbstractItemView,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths
from gui.utils.icon_utils import get_svg_pixmap
from gui.widgets.reorderable_table_widget import ReorderableTableWidget
from gui.widgets.ui.context_badge_group import BadgeButton, ContextBadgeGroup
from gui.utils.string_utils import get_sort_key, get_date_sort_key


class SortChildrenContent(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("sort_children_content")
        self.group_name = ""
        self.academic_year = ""
        self.original_students = []
        self.current_students = []

        # HEADER
        sub_title = QLabel("Балалар тізімі:")
        sub_title.setProperty("lbl-level", "h3")
        self.group_name_btn = BadgeButton(IconPaths.USERS, " Топ: ", "")
        self.academic_year_btn = BadgeButton(IconPaths.CALENDAR, " Оқу жылы: ", "")
        context_badge_group = ContextBadgeGroup(
            [self.group_name_btn, self.academic_year_btn], parent=self
        )

        header_layout = QHBoxLayout()
        header_layout.addWidget(sub_title)
        header_layout.addStretch()
        header_layout.addWidget(context_badge_group)

        # TABLE CONTROL BAR
        sort_table_label = QLabel("Кестені сұрыптау: ")
        sort_table_label.setProperty("lbl-level", "h3")

        sort_by_names_btn = QPushButton(" Бала есімімен")
        sort_by_names_btn.setProperty("btn-size", "small")
        sort_by_names_btn.setProperty("btn-type", "outline")
        arrow_up_down_pixmap = get_svg_pixmap(
            IconPaths.ARROW_UP_DOWN, AppColors.PRIMARY, 16
        )
        sort_by_names_btn.setIcon(QIcon(arrow_up_down_pixmap))

        sort_by_birthdate_btn = QPushButton(" Туған күнімен")
        sort_by_birthdate_btn.setProperty("btn-size", "small")
        sort_by_birthdate_btn.setProperty("btn-type", "outline")
        calendar_pixmap = get_svg_pixmap(IconPaths.CALENDAR, AppColors.PRIMARY, 16)
        sort_by_birthdate_btn.setIcon(QIcon(calendar_pixmap))

        return_first_ordering_btn = QPushButton(" Бастапқы реттілікке қайтару")
        return_first_ordering_btn.setProperty("btn-size", "small")
        return_first_ordering_btn.setProperty("btn-type", "outline")
        rotate_pixmap = get_svg_pixmap(IconPaths.ROTATE, AppColors.PRIMARY, 16)
        return_first_ordering_btn.setIcon(QIcon(rotate_pixmap))

        table_operations_bar_frame = QFrame()
        table_operations_bar_frame.setObjectName("table_operations_bar_frame")
        table_operations_bar_layout = QHBoxLayout(table_operations_bar_frame)
        table_operations_bar_layout.setContentsMargins(10, 10, 10, 10)
        table_operations_bar_layout.setSpacing(20)
        table_operations_bar_layout.addWidget(sort_table_label)
        table_operations_bar_layout.addWidget(sort_by_names_btn)
        table_operations_bar_layout.addWidget(sort_by_birthdate_btn)
        table_operations_bar_layout.addStretch(1)
        table_operations_bar_layout.addWidget(return_first_ordering_btn)

        # TABLE
        self.table = ReorderableTableWidget()
        self.table.setShowGrid(False)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setCornerButtonEnabled(False)
        self.table.setDragEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.setDropIndicatorShown(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setDragDropMode(QAbstractItemView.InternalMove)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                "Баланың аты-жөні",
                "Туған күні",
                "Бастапқы (X-XII)",
                "Аралық (II-IV)",
                "Қорытынды (VI-VIII)",
            ]
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        layout.addLayout(header_layout)
        layout.addWidget(table_operations_bar_frame)
        layout.addWidget(self.table)

        sort_by_names_btn.clicked.connect(self._sort_by_fullname)
        sort_by_birthdate_btn.clicked.connect(self._sort_by_birthdate)

    def _sort_by_fullname(self):
        self.current_students.sort(key=lambda x: get_sort_key(x.get("fullname", "")))
        self._refresh_table_ui()

    def _sort_by_birthdate(self):
        self.current_students.sort(
            key=lambda x: get_date_sort_key(x.get("birth_date", ""))
        )
        self._refresh_table_ui()

    def set_table_item(self, row, child_dict):
        assessments = child_dict.get("assessments", [])
        start_assessments = [
            next(iter(a["criterion"]), "") for a in assessments if len(a["start"]) > 1
        ]
        mid_assessments = [
            next(iter(a["criterion"]), "") for a in assessments if len(a["mid"]) > 1
        ]
        end_assessments = [
            next(iter(a["criterion"]), "") for a in assessments if len(a["end"]) > 1
        ]

        fullname_item = QTableWidgetItem(str(str(child_dict.get("fullname", ""))))
        fullname_item.setData(100, child_dict)
        birth_date_item = QTableWidgetItem(str(child_dict.get("birth_date", "")))
        start_assessments_item = QTableWidgetItem(", ".join(start_assessments))
        mid_assessments_item = QTableWidgetItem(", ".join(mid_assessments))
        end_assessments_item = QTableWidgetItem(", ".join(end_assessments))

        self.table.setItem(row, 0, fullname_item)
        self.table.setItem(row, 1, birth_date_item)
        self.table.setItem(row, 2, start_assessments_item)
        self.table.setItem(row, 3, mid_assessments_item)
        self.table.setItem(row, 4, end_assessments_item)

    def _refresh_table_ui(self):
        self.table.setRowCount(len(self.current_students))
        for row, child in enumerate(self.current_students):
            self.set_table_item(row, child)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.setColumnWidth(0, 260)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        for i in range(2, self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

    def applyData(self, academic_year: str, group_name: str, students_cards: list):
        self.academic_year = academic_year
        self.group_name = group_name
        if not self.original_students:
            self.original_students = list(students_cards)
        self.current_students = list(students_cards)

        self.group_name_btn.setText(group_name)
        self.academic_year_btn.setText(academic_year[0:11])

        self._refresh_table_ui()
