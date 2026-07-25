# ui/step_prompt_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QSizePolicy
)
from PySide6.QtCore import Qt


class StepPromptView(QWidget):
    """
    プロンプト表示画面（Gemini / Copilot / Pika / Google翻訳）
    """

    def __init__(self, controller, state_key, jp_text, en_text):
        super().__init__()
        self.controller = controller
        self.state_key = state_key
        self.jp_text = jp_text
        self.en_text = en_text

        self.init_ui()

    # ---------------------------------------------------------
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(30)

        # -----------------------------
        # 左側：プロンプト表示
        # -----------------------------
        left = QVBoxLayout()
        layout.addLayout(left, 2)

        lbl_jp = QLabel("【Japanese Description】")
        lbl_jp.setStyleSheet("font-size: 22pt; font-weight: bold;")
        left.addWidget(lbl_jp)

        self.txt_jp = QTextEdit()
        self.txt_jp.setText(self.jp_text)
        self.txt_jp.setStyleSheet("font-size: 18pt;")
        self.txt_jp.setMinimumHeight(250)
        left.addWidget(self.txt_jp)

        lbl_en = QLabel("【English Prompt】")
        lbl_en.setStyleSheet("font-size: 22pt; font-weight: bold; margin-top: 20px;")
        left.addWidget(lbl_en)

        self.txt_en = QTextEdit()
        self.txt_en.setText(self.en_text)
        self.txt_en.setStyleSheet("font-size: 18pt;")
        self.txt_en.setMinimumHeight(250)
        left.addWidget(self.txt_en)

        # -----------------------------
        # 右側：AIサイトボタン
        # -----------------------------
        right = QVBoxLayout()
        layout.addLayout(right, 1)

        # --- AIサイトボタン ---
        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        right.addLayout(btn_row)

        btn_gemini = QPushButton("Gemini を開く")
        btn_gemini.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_gemini.clicked.connect(lambda: self.controller.open_url("https://gemini.google.com"))
        btn_row.addWidget(btn_gemini)

        btn_copilot = QPushButton("Copilot を開く")
        btn_copilot.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_copilot.clicked.connect(lambda: self.controller.open_url("https://copilot.microsoft.com"))
        btn_row.addWidget(btn_copilot)

        btn_pika = QPushButton("Pika を開く")
        btn_pika.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_pika.clicked.connect(lambda: self.controller.open_url("https://pika.art"))
        btn_row.addWidget(btn_pika)

        # --- ★ Google翻訳ボタン（Pika 用） ---
        btn_translate = QPushButton("Google翻訳（日本語→英語）")
        btn_translate.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_translate.clicked.connect(
            lambda: self.controller.open_url("https://translate.google.com/?sl=ja&tl=en")
        )
        right.addWidget(btn_translate)

        # --- AI生成ガイド ---
        btn_guide = QPushButton("AI生成ガイドを見る")
        btn_guide.setStyleSheet("font-size: 22pt; padding: 10px; margin-top: 20px;")
        btn_guide.clicked.connect(self.on_guide)
        right.addWidget(btn_guide)

        # --- 戻る ---
        btn_back = QPushButton("編集メニューに戻る")
        btn_back.setStyleSheet("font-size: 22pt; padding: 10px; margin-top: 20px;")
        btn_back.clicked.connect(self.on_back)
        right.addWidget(btn_back)

        right.addStretch()

    # ---------------------------------------------------------
    def on_guide(self):
        self.controller.show_stepAIGuideForMedia()

    def on_back(self):
        self.controller.show_stepEditMenu()


