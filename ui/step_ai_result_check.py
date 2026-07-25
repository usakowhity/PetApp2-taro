# ui/step_ai_result_check.py
import os
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QGridLayout, QVBoxLayout
from PySide6.QtCore import Qt


class StepAIResultCheck(QWidget):
    """
    AI生成素材の確認画面
    - 保存先は generated/ に統一
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("AI生成素材の確認")
        self.setMinimumSize(900, 700)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("AI生成した素材を登録してください")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(12)

        self.states = ["n1", "n2", "n3",
                       "p1", "p2", "p3", "p4", "p5", "p6",
                       "p7", "p8", "p9", "p10", "p11", "p12"]

        self.labels = {}

        row = 0
        col = 0

        for state in self.states:
            lbl = QLabel(f"{state}: 未登録")
            lbl.setStyleSheet("font-size: 18px;")
            self.labels[state] = lbl

            btn = QPushButton("参照")
            btn.clicked.connect(lambda _, s=state: self.select_file(s))

            grid.addWidget(lbl, row, col)
            grid.addWidget(btn, row, col + 1)

            col += 2
            if col >= 4:
                col = 0
                row += 1

        layout.addLayout(grid)

        self.btn_play = QPushButton("遊ぶ（PlayWindow）")
        self.btn_play.setStyleSheet("font-size: 22px; padding: 12px;")
        self.btn_play.setEnabled(False)
        self.btn_play.clicked.connect(self.go_play)
        layout.addWidget(self.btn_play)

        btn_back = QPushButton("戻る")
        btn_back.clicked.connect(self.go_back)
        layout.addWidget(btn_back)

        self.setLayout(layout)

        self.refresh_status()

    def select_file(self, state):
        path, _ = QFileDialog.getOpenFileName(self, f"{state} の素材を選択")
        if not path:
            return

        save_dir = "F:/PetApp2/generated/"
        os.makedirs(save_dir, exist_ok=True)

        ext = os.path.splitext(path)[1]
        save_path = os.path.join(save_dir, f"{state}{ext}")

        with open(path, "rb") as src, open(save_path, "wb") as dst:
            dst.write(src.read())

        self.controller.pet_images[state] = save_path
        self.controller.save_profile()

        self.refresh_status()

    def refresh_status(self):
        all_ok = True

        for state in self.states:
            path = self.controller.pet_images.get(state, "")
            if path and os.path.exists(path):
                self.labels[state].setText(f"{state}: 登録済み")
                self.labels[state].setStyleSheet("color: green; font-size: 18px;")
            else:
                self.labels[state].setText(f"{state}: 未登録")
                self.labels[state].setStyleSheet("color: red; font-size: 18px;")
                all_ok = False

        self.btn_play.setEnabled(all_ok)

    def go_play(self):
        self.close()
        self.controller.show_play_window()

    def go_back(self):
        self.close()
        self.controller.show_step_prompt_confirm()
