# ui/state_reference_window.py
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QScrollArea
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import json
from pathlib import Path


class StateReferenceWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("状態一覧（デモサムネイル付き）")
        self.setMinimumSize(900, 700)

        main_layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(16)

        json_path = Path(__file__).resolve().parent.parent / "assets" / "states.json"
        demo_dir = Path(__file__).resolve().parent.parent / "assets" / "demo"

        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                states = json.load(f)
        else:
            states = {}

        row, col = 0, 0
        for key, info in states.items():
            img_path = demo_dir / f"{key}.png"
            pixmap = QPixmap(str(img_path)) if img_path.exists() else QPixmap()
            thumb = QLabel()
            if not pixmap.isNull():
                thumb.setPixmap(pixmap.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                thumb.setText("[No Image]")
                thumb.setAlignment(Qt.AlignCenter)
                thumb.setFixedSize(160, 160)

            name_label = QLabel(f"<b>{info['name']}</b>（{key}）")
            desc_label = QLabel(info["description"])
            desc_label.setWordWrap(True)
            desc_label.setFixedWidth(260)

            cell = QVBoxLayout()
            cell.addWidget(thumb, alignment=Qt.AlignCenter)
            cell.addWidget(name_label)
            cell.addWidget(desc_label)

            cell_widget = QWidget()
            cell_widget.setLayout(cell)
            grid.addWidget(cell_widget, row, col)

            col += 1
            if col >= 3:
                col = 0
                row += 1

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        next_btn = QPushButton("次へ（generated登録へ）")
        next_btn.clicked.connect(self.go_next)
        main_layout.addWidget(next_btn, alignment=Qt.AlignRight)

        self.setLayout(main_layout)

    def go_next(self):
        self.close()
        self.controller.show_generated_register()
