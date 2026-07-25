# ui/stepC_media.py

import os
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QListWidget, QListWidgetItem,
    QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem,
    QSizePolicy
)
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import Qt, QUrl


class StepCMediaWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("素材確認（StepC_media）")

        self.current_state = None

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # 左：状態一覧
        self.list_states = QListWidget()
        self.list_states.setMinimumWidth(160)
        main_layout.addWidget(self.list_states)

        # 右：プレビュー
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        self.label_title = QLabel("状態のプレビュー")
        self.label_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        right_layout.addWidget(self.label_title)

        self.preview_label = QLabel("左の一覧から状態を選択してください。")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(400, 300)
        self.preview_label.setStyleSheet("border: 1px solid #ccc;")
        right_layout.addWidget(self.preview_label)

        self.path_label = QLabel("")
        self.path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        right_layout.addWidget(self.path_label)

        # ボタン行
        btn_row = QHBoxLayout()
        right_layout.addLayout(btn_row)

        self.btn_open_video = QPushButton("動画を開く")
        self.btn_open_video.clicked.connect(self.open_video)
        self.btn_open_video.setEnabled(False)
        btn_row.addWidget(self.btn_open_video)

        self.btn_show_prompt = QPushButton("プロンプトを見る")
        self.btn_show_prompt.clicked.connect(self.show_prompt)
        btn_row.addWidget(self.btn_show_prompt)

        btn_row.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 下部ナビゲーション
        nav_row = QHBoxLayout()
        right_layout.addLayout(nav_row)

        self.btn_back = QPushButton("戻る")
        self.btn_back.clicked.connect(self.go_back)
        nav_row.addWidget(self.btn_back)

        nav_row.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.btn_next = QPushButton("次へ（素材チェック完了）")
        self.btn_next.clicked.connect(self.go_next)
        nav_row.addWidget(self.btn_next)

        # 状態一覧の初期化
        self.populate_state_list()
        self.list_states.currentItemChanged.connect(self.on_state_changed)

    # ---------------------------------------------------------
    def populate_state_list(self):
        self.list_states.clear()
        media = self.controller.media

        from controller import STATE_LIST

        for state in STATE_LIST:
            mark = "✔" if state in media else "✖"
            item = QListWidgetItem(f"{state}  {mark}")
            if state not in media:
                item.setForeground(Qt.gray)
            item.setData(Qt.UserRole, state)
            self.list_states.addItem(item)

    # ---------------------------------------------------------
    def on_state_changed(self, current, previous):
        if not current:
            return
        self.current_state = current.data(Qt.UserRole)
        self.update_preview()

    # ---------------------------------------------------------
    def update_preview(self):
        state = self.current_state
        media = self.controller.media
        path = media.get(state)

        if path and os.path.exists(path):
            self.label_title.setText(f"状態 {state} のプレビュー（生成済み）")
            self.path_label.setText(path)

            ext = os.path.splitext(path)[1].lower()
            if ext in [".png", ".jpg", ".jpeg"]:
                pix = QPixmap(path)
                if not pix.isNull():
                    self.preview_label.setPixmap(
                        pix.scaled(
                            self.preview_label.size(),
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation
                        )
                    )
                else:
                    self.preview_label.setText("画像を読み込めませんでした。")
                    self.preview_label.setPixmap(QPixmap())
                self.btn_open_video.setEnabled(False)

            elif ext in [".mp4", ".mov", ".avi", ".mkv"]:
                self.preview_label.setText("動画ファイルです。「動画を開く」を押してください。")
                self.preview_label.setPixmap(QPixmap())
                self.btn_open_video.setEnabled(True)

        else:
            self.label_title.setText(f"状態 {state} のプレビュー（未生成）")
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText(
                "この状態の素材はまだありません。\n"
                "「プロンプトを見る」からプロンプトを確認し、\n"
                "外部AIで生成して generated フォルダに保存してください。"
            )
            self.path_label.setText("")
            self.btn_open_video.setEnabled(False)

    # ---------------------------------------------------------
    def open_video(self):
        state = self.current_state
        path = self.controller.media.get(state)
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    # ---------------------------------------------------------
    def show_prompt(self):
        self.close()
        self.controller.show_stepPromptConfirm()

    # ---------------------------------------------------------
    def go_back(self):
        self.close()
        self.controller.show_stepPromptConfirm()

    # ---------------------------------------------------------
    def go_next(self):
        self.close()
        self.controller.show_stepC_finish()

