# ui/pet_register_window.py
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QFormLayout
)


class PetRegisterWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("ペット登録")
        self.setMinimumSize(600, 420)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("ペットの基本情報を入力してください"))

        form = QFormLayout()

        self.species_box = QComboBox()
        self.species_box.addItems(["犬", "猫", "うさぎ"])
        form.addRow("種別", self.species_box)

        self.breed_box = QLineEdit()
        self.breed_box.setPlaceholderText("品種（詳細は次画面で選択可）")
        form.addRow("品種（任意）", self.breed_box)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("名前")
        form.addRow("名前", self.name_edit)

        self.magic_word_edit = QLineEdit()
        self.magic_word_edit.setPlaceholderText("魔法の言葉（任意）")
        form.addRow("魔法の言葉", self.magic_word_edit)

        layout.addLayout(form)

        next_btn = QPushButton("次へ（状態説明へ）")
        next_btn.clicked.connect(self.go_next)
        layout.addWidget(next_btn)

        self.setLayout(layout)

    def go_next(self):
        # Optionally store basic info in controller or a model
        # For now, just proceed
        self.close()
        self.controller.show_state_reference()
