# ui/step_prompt_confirm.py

import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices


class StepPromptConfirmWindow(QWidget):
    """
    StepPromptConfirm：プロンプト統合版
    - 全状態 n1〜p12 のプロンプトを controller.build_prompt_for_state() で生成
    - プロンプト閲覧
    - AIサイトで開く
    - プロンプト保存
    - StepC_media へ遷移
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("プロンプト確認（統合版）")
        self.setMinimumSize(1400, 900)

        # controller から states.json を読み込んだメタ情報を取得
        self.states_meta = controller._states_cache if hasattr(controller, "_states_cache") else None
        if self.states_meta is None:
            # 初回は build_prompt_for_state() 内で states.json が読み込まれる
            controller.build_prompt_for_state("n1")
            self.states_meta = controller._states_cache

        # UI 構築
        self._build_ui()

        # 初期表示
        self.list_states.setCurrentRow(0)
        self.on_state_selected(0)

    # ---------------------------------------------------------
    # UI 構築
    # ---------------------------------------------------------
    def _build_ui(self):
        layout = QHBoxLayout(self)

        # 左：状態一覧
        self.list_states = QListWidget()
        for sid, meta in self.states_meta.items():
            label = meta.get("name", sid)
            item = QListWidgetItem(f"{sid}：{label}")
            self.list_states.addItem(item)
        self.list_states.currentRowChanged.connect(self.on_state_selected)
        layout.addWidget(self.list_states, 1)

        # 右側
        right = QVBoxLayout()

        self.txt_prompt = QTextEdit()
        self.txt_prompt.setReadOnly(True)
        self.txt_prompt.setStyleSheet("font-size: 14pt;")
        right.addWidget(self.txt_prompt, 8)

        # ボタン行
        btn_row = QHBoxLayout()

        btn_open = QPushButton("AIサイトで開く")
        btn_open.clicked.connect(self.open_ai_site)
        btn_row.addWidget(btn_open)

        btn_save = QPushButton("このプロンプトを保存")
        btn_save.clicked.connect(self.save_prompt)
        btn_row.addWidget(btn_save)

        btn_all = QPushButton("全プロンプト一括保存")
        btn_all.clicked.connect(self.save_all_prompts)
        btn_row.addWidget(btn_all)

        right.addLayout(btn_row)

        # 次へ（StepC_media）
        btn_next = QPushButton("次へ（素材確認へ）")
        btn_next.setStyleSheet("font-size: 18pt; min-height: 50px;")
        btn_next.clicked.connect(self.go_next)
        right.addWidget(btn_next)

        layout.addLayout(right, 3)

    # ---------------------------------------------------------
    # 状態選択
    # ---------------------------------------------------------
    def on_state_selected(self, row):
        if row < 0:
            return

        sid = list(self.states_meta.keys())[row]

        # ★ controller に統一されたプロンプト生成を依頼
        prompt_ja, prompt_en = self.controller.build_prompt_for_state(sid)

        # 日本語プロンプトを表示
        self.txt_prompt.setText(prompt_ja)

        # 保存用に保持
        self.current_sid = sid
        self.current_prompt = prompt_ja

    # ---------------------------------------------------------
    def open_ai_site(self):
        if not hasattr(self, "current_prompt"):
            return
        url = "https://www.bing.com/images/create?q=" + QUrl.toPercentEncoding(self.current_prompt).data().decode()
        QDesktopServices.openUrl(QUrl(url))

    # ---------------------------------------------------------
    def save_prompt(self):
        sid = self.current_sid
        prompt = self.current_prompt

        out_dir = os.path.join(self.controller.GENERATED_DIR, "prompts")
        os.makedirs(out_dir, exist_ok=True)

        path = os.path.join(out_dir, f"{sid}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(prompt)

        QMessageBox.information(self, "保存完了", f"{sid}.txt を保存しました")

    # ---------------------------------------------------------
    def save_all_prompts(self):
        out_dir = os.path.join(self.controller.GENERATED_DIR, "prompts")
        os.makedirs(out_dir, exist_ok=True)

        for sid in self.states_meta.keys():
            prompt_ja, _ = self.controller.build_prompt_for_state(sid)
            path = os.path.join(out_dir, f"{sid}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(prompt_ja)

        QMessageBox.information(self, "保存完了", "全プロンプトを保存しました")

    # ---------------------------------------------------------
    def go_next(self):
        self.controller.show_stepC_media()
        self.close()

