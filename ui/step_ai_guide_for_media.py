# ui/step_ai_guide_for_media.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
)
from PySide6.QtCore import Qt


class StepAIGuideForMedia(QWidget):
    """
    AI生成ガイド画面
    - Gemini / Copilot / Pika の使い方
    - Pika は英語プロンプト推奨（Google翻訳ボタンの説明付き）
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    # ---------------------------------------------------------
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # スクロール可能にする
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        inner = QVBoxLayout(container)
        inner.setSpacing(25)

        # -----------------------------------------------------
        # タイトル
        # -----------------------------------------------------
        title = QLabel("AI生成ガイド")
        title.setStyleSheet("font-size: 32pt; font-weight: bold;")
        inner.addWidget(title)

        # -----------------------------------------------------
        # Gemini
        # -----------------------------------------------------
        gem_title = QLabel("■ Gemini（静止画生成）")
        gem_title.setStyleSheet("font-size: 26pt; font-weight: bold;")
        inner.addWidget(gem_title)

        gem_desc = QLabel(
            "Google Gemini は日本語プロンプトを高精度に理解できます。\n"
            "そのまま日本語のプロンプトを貼り付けて生成してください。\n"
            "特に犬・猫などの動物の描写に強く、安定した品質が得られます。"
        )
        gem_desc.setStyleSheet("font-size: 20pt;")
        gem_desc.setWordWrap(True)
        inner.addWidget(gem_desc)

        # -----------------------------------------------------
        # Copilot
        # -----------------------------------------------------
        cop_title = QLabel("■ Copilot（静止画生成）")
        cop_title.setStyleSheet("font-size: 26pt; font-weight: bold;")
        inner.addWidget(cop_title)

        cop_desc = QLabel(
            "Microsoft Copilot も日本語プロンプトをそのまま理解できます。\n"
            "Gemini と同様に、日本語のまま貼り付けて問題ありません。\n"
            "柔らかい雰囲気のイラストや自然な色合いの描写が得意です。"
        )
        cop_desc.setStyleSheet("font-size: 20pt;")
        cop_desc.setWordWrap(True)
        inner.addWidget(cop_desc)

        # -----------------------------------------------------
        # Pika
        # -----------------------------------------------------
        pika_title = QLabel("■ Pika（動画生成）")
        pika_title.setStyleSheet("font-size: 26pt; font-weight: bold;")
        inner.addWidget(pika_title)

        pika_desc = QLabel(
            "Pika は高品質な動画生成が可能です。\n"
            "ただし、Pika は **英語プロンプトの方が安定して動作します**。\n"
            "日本語プロンプトでも生成できますが、意図が正確に伝わらない場合があります。\n\n"
            "必要に応じて、プロンプト一覧画面の下部にある\n"
            "『Google翻訳（日本語→英語）』ボタンを押して英訳してから\n"
            "Pika に貼り付けてください。"
        )
        pika_desc.setStyleSheet("font-size: 20pt;")
        pika_desc.setWordWrap(True)
        inner.addWidget(pika_desc)

        # -----------------------------------------------------
        # 戻るボタン
        # -----------------------------------------------------
        btn_back = QPushButton("戻る")
        btn_back.setStyleSheet("font-size: 22pt; padding: 10px; margin-top: 20px;")
        btn_back.clicked.connect(self.controller.show_stepAllPromptsView)
        inner.addWidget(btn_back)

        inner.addStretch()
