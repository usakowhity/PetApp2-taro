# ui/stepC_materials.py

import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout,
    QFileDialog, QMessageBox, QScrollArea
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

STATE_CODES = [
    "n1", "n2", "n3",
    "p1", "p2", "p3", "p4", "p5", "p6",
    "p7", "p8", "p9", "p10", "p11", "p12"
]


class StepC_Materials(QWidget):
    """
    StepC：素材登録画面（サムネイル表示＋未登録警告＋AI生成誘導）
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("StepC：素材登録")
        self.setGeometry(200, 200, 900, 700)

        main = QVBoxLayout()
        main.setContentsMargins(20, 20, 20, 20)

        title = QLabel("代表画像（n1）")
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        main.addWidget(title)

        self.n1_thumb = QLabel()
        self.n1_thumb.setFixedSize(200, 200)
        self.n1_thumb.setAlignment(Qt.AlignCenter)
        main.addWidget(self.n1_thumb)

        btn_n1 = QPushButton("n1 を登録 / 変更")
        btn_n1.clicked.connect(lambda: self.register_image("n1"))
        main.addWidget(btn_n1)

        self.n1_msg = QLabel()
        self.n1_msg.setStyleSheet("font-size: 18px; color: #cc3333;")
        main.addWidget(self.n1_msg)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        self.grid = QGridLayout(inner)
        self.grid.setSpacing(15)
        scroll.setWidget(inner)
        main.addWidget(scroll)

        btn_ai = QPushButton("AI生成へ（不足素材を補う）")
        btn_ai.clicked.connect(self.go_ai)
        btn_ai.setStyleSheet("font-size: 22px; padding: 10px;")
        main.addWidget(btn_ai)

        btn_play = QPushButton("Play Mode へ")
        btn_play.clicked.connect(self.go_play)
        btn_play.setStyleSheet("font-size: 22px; padding: 10px;")
        main.addWidget(btn_play)

        self.setLayout(main)

        self.refresh()

    def get_media_path(self, code):
        base = os.path.join("generated", code)
        if os.path.exists(base + ".mp4"):
            return base + ".mp4"
        for ext in [".png", ".jpg", ".jpeg"]:
            path = base + ext
            if os.path.exists(path):
                return path
        return None

    def refresh(self):
        n1_path = self.get_media_path("n1")
        if n1_path:
            pix = QPixmap(n1_path).scaled(200, 200, Qt.KeepAspectRatio)
            self.n1_thumb.setPixmap(pix)
            self.n1_msg.setText("この画像を基準に他の状態を生成できます")
        else:
            self.n1_thumb.setPixmap(QPixmap())
            self.n1_msg.setText("n1 が未登録です（AI生成の品質が低下します）")

        for i, code in enumerate(STATE_CODES):
            row = i // 5
            col = i % 5

            box = QVBoxLayout()

            label = QLabel(code)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 18px; font-weight: bold;")
            box.addWidget(label)

            thumb = QLabel()
            thumb.setFixedSize(120, 120)
            thumb.setAlignment(Qt.AlignCenter)

            path = self.get_media_path(code)
            if path:
                pix = QPixmap(path).scaled(120, 120, Qt.KeepAspectRatio)
                thumb.setPixmap(pix)
            else:
                thumb.setText("× 未登録")
                thumb.setStyleSheet("color: #cc3333; font-size: 16px;")

            box.addWidget(thumb)

            btn = QPushButton("登録 / 変更")
            btn.clicked.connect(lambda _, c=code: self.register_image(c))
            box.addWidget(btn)

            if code == "p2" and not path:
                warn = QLabel("★ 推奨：喜び動画を登録")
                warn.setStyleSheet("color: #cc3333; font-size: 14px;")
                box.addWidget(warn)

            self.grid.addLayout(box, row, col)

    def register_image(self, code):
        file, _ = QFileDialog.getOpenFileName(
            self, f"{code} の画像を選択", "", "Images (*.png *.jpg *.jpeg)"
        )
        if not file:
            return

        ext = os.path.splitext(file)[1]
        dst = os.path.join("generated", f"{code}{ext}")

        os.makedirs("generated", exist_ok=True)
        import shutil
        shutil.copy(file, dst)

        self.refresh()

    # ---------------------------------------------------------
    # AI生成あり → StepPromptConfirm（プロンプト生成）
    # ---------------------------------------------------------
    def go_ai(self):
        self.close()
        self.controller.show_step_prompt_confirm()

    # ---------------------------------------------------------
    # Play Mode へ
    # ---------------------------------------------------------
    def go_play(self):
        if not self.get_media_path("n1"):
            QMessageBox.warning(self, "エラー", "n1 が無いと Play Mode に進めません")
            return

        self.controller.show_play()
