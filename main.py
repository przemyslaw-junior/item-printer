import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from config_loader import Config
from printer.zebra_printer import ZebraPrinter
from utils.validators import is_valid_item, is_valid_quantity


class CustomTable(QTableWidget):

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            row = self.currentRow()
            col = self.currentColumn()
            # przechodzenie Enter-em
            if col == 0:  # kolumna Item
                self.setCurrentCell(row, 1)
            else:  # kolumna Qty
                if row == self.rowCount() - 1:  # ostatni wiersz
                    self.insertRow(self.rowCount())
                self.setCurrentCell(row + 1, 0)
        else:
            super().keyPressEvent(event)


class LabelPrintApp(QWidget):

    def __init__(self, printer):
        super().__init__()
        self.printer = printer
        self.setWindowTitle("Item Printer")

        # parametry okna
        self.base_width = 500
        self.row_height = 30
        self.max_rows_display = 10
        self.header_height = 100
        self.setMinimumWidth(self.base_width)

        # layout główny
        self.layout = QVBoxLayout()

        self.item_table = CustomTable(1, 2)
        self.item_table.setHorizontalHeaderLabels(["Item", "Qty"])
        self.item_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.item_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.layout.addWidget(self.item_table)
        
        self.item_table.model().rowsInserted.connect(self.adjust_window_height)
        self.item_table.model().rowsRemoved.connect(self.adjust_window_height)

        self.item_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: lightgray; font-weight: bold; }"
        )

        # przyciski
        button_layout = QHBoxLayout()

        add_row_btn = QPushButton("Dodaj wiersz")
        add_row_btn.clicked.connect(self.add_new_row)
        button_layout.addWidget(add_row_btn)

        remove_row_btn = QPushButton("Usuń zaznaczony")
        remove_row_btn.clicked.connect(self.remove_selected_row)
        button_layout.addWidget(remove_row_btn)

        clear_all_btn = QPushButton("Usuń wszystkie")
        clear_all_btn.clicked.connect(self.clear_all_rows)
        button_layout.addWidget(clear_all_btn)

        print_btn = QPushButton("Drukuj")
        print_btn.clicked.connect(self.handle_print)
        button_layout.addWidget(print_btn)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        # dynamiczna wysokość
        self.adjust_window_height()

    def adjust_window_height(self):
        rows = self.item_table.rowCount()
        visible_rows = min(rows, self.max_rows_display)
        new_height = self.header_height + (visible_rows * self.row_height)
        self.setFixedHeight(new_height)

    def add_new_row(self):
        self.item_table.insertRow(self.item_table.rowCount())
        self.adjust_window_height()

    def remove_selected_row(self):
        selected_rows = set(index.row() for index in self.item_table.selectedIndexes())
        if not selected_rows:
            self.show_message("Najpierw zaznacz wiersz do usunięcia.")
            return
        for row in sorted(selected_rows, reverse=True):
            if self.item_table.rowCount() > 1:
                self.item_table.removeRow(row)
            else:
                self.show_message("Nie możesz usunąć wszystkich wierszy.")
                return
        self.adjust_window_height()

    def clear_all_rows(self):
        reply = QMessageBox.question(
            self, "Potwierdzenie", "Czy na pewno chcesz usunąć wszystkie wiersze?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.item_table.setRowCount(1)
            self.item_table.setItem(0, 0, QTableWidgetItem(""))
            self.item_table.setItem(0, 1, QTableWidgetItem(""))
            self.adjust_window_height()

    def handle_print(self):
        for row in range(self.item_table.rowCount()):
            item_cell = self.item_table.item(row, 0)
            qty_cell = self.item_table.item(row, 1)
            if not item_cell or not qty_cell:
                continue
            item_text = item_cell.text().strip()
            qty_text = qty_cell.text().strip()
            if not is_valid_item(item_text):
                self.show_message(f"Błędny Item w wierszu {row+1}")
                return
            if not is_valid_quantity(qty_text):
                self.show_message(f"Błędna ilość w wierszu {row+1}")
                return
            self.printer.print_label(item_text, int(qty_text))
        self.show_message("Wydruk zakończony!", info=True)

    def show_message(self, message, info=False):
        msg = QMessageBox()
        msg.setWindowTitle("Informacja" if info else "Błąd")
        msg.setText(message)
        msg.exec_()


if __name__ == "__main__":
    config = Config()
    printer = ZebraPrinter(config.printer_ip, config.printer_port, config.font_size)
    app = QApplication(sys.argv)
    window = LabelPrintApp(printer)
    window.show()
    sys.exit(app.exec_())
