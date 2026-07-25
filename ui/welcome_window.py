# ui/welcome_window.py
import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class WelcomeWindow(QWidget):
    """
    Welcome画面（ミミ版・PetApp2 共通）
    - ペットと遊ぶ（旧：Playモードへ）
    - ペット情報を編集（StepEditMenu）
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Welcome")
        self.setFixedSize(600, 600)

        # 画面中央に配置
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2
        )

        self._build_ui()

    # ---------------------------------------------------------
    # UI 構築
    # ---------------------------------------------------------
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # ---------------------------------------------------------
        # ★ hero.png のパス（正しい位置）
        # ---------------------------------------------------------
        base_dir = os.path.dirname(os.path.abspath(__file__))  # ui/
        root_dir = os.path.dirname(base_dir)                   # PetApp2/
        hero_path = os.path.join(root_dir, "assets", "ui", "hero.png")

        # ---------------------------------------------------------
        # ★ hero画像
        # ---------------------------------------------------------
        if os.path.exists(hero_path):
            hero_label = QLabel()
            pix = QPixmap(hero_path)
            pix = pix.scaledToWidth(300, Qt.SmoothTransformation)
            hero_label.setPixmap(pix)
            hero_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(hero_label)
        else:
            print("[WelcomeWindow] hero.png が見つかりません:", hero_path)

        # タイトル
        title = QLabel("ようこそ！")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(title)

        # ★ Playモードへ → ペットと遊ぶ
        btn_play = QPushButton("ペットと遊ぶ")
        btn_play.setStyleSheet("font-size: 24px; padding: 14px;")
        btn_play.clicked.connect(self.controller.show_play)
        layout.addWidget(btn_play)

        # ペット情報を編集
        btn_edit = QPushButton("ペット情報を編集")
        btn_edit.setStyleSheet("font-size: 24px; padding: 14px;")
        btn_edit.clicked.connect(self.controller.show_stepEditMenu)
        layout.addWidget(btn_edit)

        layout.addStretch()

    # ---------------------------------------------------------
    def showEvent(self, event):
        super().showEvent(event)

