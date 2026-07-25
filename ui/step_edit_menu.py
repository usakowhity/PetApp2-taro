from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt


class StepEditMenu(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("編集メニュー")
        self.setMinimumSize(900, 700)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("ペット情報・画像/動画・プロンプトの編集")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28pt; font-weight: bold;")
        layout.addWidget(title)

        # プロフィール編集
        btn_profile = QPushButton("プロフィールを編集")
        btn_profile.setStyleSheet("font-size: 22pt; padding: 12px;")
        btn_profile.clicked.connect(self.on_edit_profile)
        layout.addWidget(btn_profile)

        # （魔法のことば編集ボタンは廃止）

        # 全プロンプト確認（StepAllPromptsView へ）
        btn_prompts = QPushButton("（全）プロンプトを確認する")
        btn_prompts.setStyleSheet("font-size: 22pt; padding: 12px;")
        btn_prompts.clicked.connect(self.on_view_prompts)
        layout.addWidget(btn_prompts)

        # 画像/動画編集
        btn_media = QPushButton("画像/動画を変更・追加")
        btn_media.setStyleSheet("font-size: 22pt; padding: 12px;")
        btn_media.clicked.connect(self.on_edit_media)
        layout.addWidget(btn_media)

        # ようこそ！画面に戻る
        btn_back = QPushButton("ようこそ！画面に戻る")
        btn_back.setStyleSheet("font-size: 22pt; padding: 12px;")
        btn_back.clicked.connect(self.on_back)
        layout.addWidget(btn_back)

    # ---------------------------------------------------------
    def on_edit_profile(self):
        self.close()
        self.controller.show_stepB2()

    def on_view_prompts(self):
        self.close()
        self.controller.show_stepAllPromptsView()

    def on_edit_media(self):
        self.close()
        self.controller.show_stepMediaView()

    def on_back(self):
        self.close()
        self.controller.show_welcome()

