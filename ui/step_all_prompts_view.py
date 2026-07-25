# ui/step_all_prompts_view.py

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QScrollArea, QSizePolicy
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from controller import STATE_LIST, STATE_META_JA


class StepAllPromptsView(QWidget):
    """
    全15状態のプロンプトを一覧表示する画面
    - サムネイル付き
    - Japanese / English 両方表示
    - Gemini / Copilot / Pika / Google翻訳ボタン
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.base_dir = controller.BASE_DIR
        self.prompts_dir = os.path.join(controller.generated_dir, "prompts")
        self.assets_dir = controller.assets_dir

        self.init_ui()

    # ---------------------------------------------------------
    def init_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(15)

        title = QLabel("全プロンプト一覧（15状態）")
        title.setStyleSheet("font-size: 32pt; font-weight: bold;")
        root.addWidget(title)

        # スクロールエリア
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        root.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        inner = QVBoxLayout(container)
        inner.setSpacing(25)

        # 各状態ごとにブロックを作成
        for state in STATE_LIST:
            block = self.create_state_block(state)
            inner.addLayout(block)

        inner.addStretch()

        # 下部ボタン群（AIサイト + ガイド + 編集メニュー）
        bottom = QHBoxLayout()
        bottom.setSpacing(20)
        root.addLayout(bottom)

        btn_gemini = QPushButton("Gemini を開く")
        btn_gemini.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_gemini.clicked.connect(lambda: self.controller.open_url("https://gemini.google.com"))
        bottom.addWidget(btn_gemini)

        btn_copilot = QPushButton("Copilot を開く")
        btn_copilot.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_copilot.clicked.connect(lambda: self.controller.open_url("https://copilot.microsoft.com"))
        bottom.addWidget(btn_copilot)

        btn_pika = QPushButton("Pika を開く")
        btn_pika.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_pika.clicked.connect(lambda: self.controller.open_url("https://pika.art"))
        bottom.addWidget(btn_pika)

        btn_translate = QPushButton("Google翻訳（日本語→英語）")
        btn_translate.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_translate.clicked.connect(
            lambda: self.controller.open_url("https://translate.google.com/?sl=ja&tl=en")
        )
        bottom.addWidget(btn_translate)

        btn_guide = QPushButton("AI生成ガイドを見る")
        btn_guide.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_guide.clicked.connect(self.on_guide)
        root.addWidget(btn_guide)

        btn_back = QPushButton("編集メニューに戻る")
        btn_back.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_back.clicked.connect(self.on_back)
        root.addWidget(btn_back)

    # ---------------------------------------------------------
    def create_state_block(self, state: str):
        """
        1状態分のブロック（サムネイル + 説明 + プロンプト）
        """
        from controller import STATE_META_EN  # 循環import回避のためローカルで

        layout = QVBoxLayout()
        layout.setSpacing(5)

        meta_ja = STATE_META_JA.get(state, {})
        name_ja = meta_ja.get("name", state)

        header = QLabel(f"■ {state} : {name_ja}")
        header.setStyleSheet("font-size: 24pt; font-weight: bold;")
        layout.addWidget(header)

        # 上段：サムネイル + 日本語説明
        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        layout.addLayout(top_row)

        # サムネイル
        thumb_label = QLabel()
        thumb_label.setFixedSize(160, 160)
        thumb_label.setStyleSheet("background-color: #dddddd;")
        thumb_label.setAlignment(Qt.AlignCenter)

        thumb_path = os.path.join(self.assets_dir, "states", f"{state}.png")
        if os.path.exists(thumb_path):
            pix = QPixmap(thumb_path)
            if not pix.isNull():
                thumb_label.setPixmap(pix.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                thumb_label.setText("No Image")
        else:
            thumb_label.setText("No Image")

        top_row.addWidget(thumb_label)

        # 日本語説明
        desc_ja_label = QLabel(meta_ja.get("description", ""))
        desc_ja_label.setStyleSheet("font-size: 18pt;")
        desc_ja_label.setWordWrap(True)
        top_row.addWidget(desc_ja_label, 1)

        # プロンプト読み込み
        jp_text, en_text = self.load_prompt_texts(state)

        # Japanese Description
        lbl_jp = QLabel("【Japanese Description】")
        lbl_jp.setStyleSheet("font-size: 18pt; font-weight: bold; margin-top: 5px;")
        layout.addWidget(lbl_jp)

        txt_jp = QTextEdit()
        txt_jp.setReadOnly(True)
        txt_jp.setStyleSheet("font-size: 16pt;")
        txt_jp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        txt_jp.setMinimumHeight(80)
        txt_jp.setText(jp_text)
        layout.addWidget(txt_jp)

        # English Prompt
        lbl_en = QLabel("【English Prompt】")
        lbl_en.setStyleSheet("font-size: 18pt; font-weight: bold; margin-top: 5px;")
        layout.addWidget(lbl_en)

        txt_en = QTextEdit()
        txt_en.setReadOnly(True)
        txt_en.setStyleSheet("font-size: 16pt;")
        txt_en.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        txt_en.setMinimumHeight(80)
        txt_en.setText(en_text)
        layout.addWidget(txt_en)

        return layout

    # ---------------------------------------------------------
    def load_prompt_texts(self, state: str):
        """
        generated/prompts/{state}.txt から
        Japanese / English を分離して返す
        """
        path = os.path.join(self.prompts_dir, f"{state}.txt")
        if not os.path.exists(path):
            return "", ""

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        parts = text.split("【English Prompt】")
        jp = parts[0].replace("【Japanese Description】", "").strip()
        en = parts[1].strip() if len(parts) > 1 else ""
        return jp, en

    # ---------------------------------------------------------
    def on_guide(self):
        self.controller.show_stepAIGuideForMedia()

    def on_back(self):
        self.controller.show_stepEditMenu()
