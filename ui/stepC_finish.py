# ui/stepC_finish.py

import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt


class StepCFinishWindow(QWidget):
    """
    StepC_finish：素材最終確認画面
    - generated フォルダの状態一覧
    - PlayWindow へ進む前の最終チェック
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("最終確認（StepC_finish）")
        self.setMinimumSize(900, 700)

        layout = QVBoxLayout(self)

        title = QLabel("素材の最終確認")
        title.setStyleSheet("font-size: 20pt; font-weight: bold;")
        layout.addWidget(title)

        desc = QLabel(
            "generated フォルダに保存されている素材の一覧です。\n"
            "すべての状態が揃っているか確認してください。\n"
            "不足している場合は StepPromptConfirm に戻ってプロンプトを確認し、外部AIで生成してください。"
        )
        desc.setStyleSheet("font-size: 12pt;")
        layout.addWidget(desc)

        # 状態一覧
        self.list_states = QListWidget()
        layout.addWidget(self.list_states, 1)

        self.populate_list()

        # ボタン行
        btn_row = QHBoxLayout()
        layout.addLayout(btn_row)

        btn_back = QPushButton("戻る（素材確認へ）")
        btn_back.clicked.connect(self.go_back)
        btn_row.addWidget(btn_back)

        btn_row.addStretch()

        btn_play = QPushButton("Play モードを開始")
        btn_play.setStyleSheet("font-size: 18pt; min-height: 50px;")
        btn_play.clicked.connect(self.go_play)
        btn_row.addWidget(btn_play)

    # ---------------------------------------------------------
    def populate_list(self):
        self.list_states.clear()

        media = self.controller.media
        from controller import STATE_LIST

        for state in STATE_LIST:
            if state in media:
                item = QListWidgetItem(f"{state}：✔ 生成済み")
            else:
                item = QListWidgetItem(f"{state}：✖ 未生成")
                item.setForeground(Qt.gray)
            self.list_states.addItem(item)

    # ---------------------------------------------------------
    def go_back(self):
        self.controller.show_stepC_media()
        self.close()

    # ---------------------------------------------------------
    def go_play(self):
        from controller import STATE_LIST

        missing = [s for s in STATE_LIST if s not in self.controller.media]

        if missing:
            msg = "以下の状態が未生成です：\n" + ", ".join(missing)
            msg += "\n\nそれでも Play モードを開始しますか？"
            reply = QMessageBox.question(self, "未生成の状態があります", msg)
            if reply != QMessageBox.Yes:
                return

        self.controller.show_play()
        self.close()
