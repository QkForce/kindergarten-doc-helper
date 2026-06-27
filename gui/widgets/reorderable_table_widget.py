from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtGui import QDropEvent
from PySide6.QtCore import Qt


class ReorderableTableWidget(QTableWidget):
    def dropEvent(self, event: QDropEvent):
        # Only accept elements dragged from this table
        if not event.isAccepted() and event.source() == self:
            source_row = self.currentRow()

            # Define the drop location
            drop_pos = event.position().toPoint()
            target_row = self.rowAt(drop_pos.y())

            # If dropped to the bottom of the table (in an empty space)
            if target_row == -1:
                target_row = self.rowCount()

            # If dropped to its own location
            if source_row == target_row:
                event.ignore()
                return

            # 1. Read data (text and hidden Data)
            row_data = []
            for col in range(self.columnCount()):
                item = self.item(source_row, col)
                text = item.text() if item else ""
                data_100 = item.data(100) if item else None
                row_data.append({"text": text, "data_100": data_100})

            # 2. ADD NEW ROW (Mathematical precision)
            insert_row = target_row
            # If dragged down, it should fall BELOW the selected row
            if source_row < target_row:
                insert_row += 1

            self.insertRow(insert_row)

            # 3. Fill the new row
            for col, cell in enumerate(row_data):
                new_item = QTableWidgetItem(cell["text"])
                if cell["data_100"] is not None:
                    new_item.setData(100, cell["data_100"])
                self.setItem(insert_row, col, new_item)

            # 4. DELETE OLD ROW
            delete_row = source_row
            # If the new row is added above the old row,
            # the index of the old row is shifted down by 1
            if insert_row <= source_row:
                delete_row += 1

            self.removeRow(delete_row)

            # 5. Selecting the new row (Selection)
            new_selection_row = (
                insert_row if insert_row <= source_row else insert_row - 1
            )
            self.setCurrentCell(new_selection_row, 0)

            # MOST IMPORTANT STEP:
            # Strictly prevent Qt from deleting it on its own PROHIBITION
            event.setDropAction(Qt.IgnoreAction)
            event.accept()
        else:
            super().dropEvent(event)
