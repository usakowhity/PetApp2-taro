# ui/step_state_intro.py
import os
import json
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea,
    QListWidget, QListWidgetItem, QTextEdit, QPushButton
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class StepStateIntroWindow(QWidget):
    """
    状態一覧（サムネイル + 説明）
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.dirname(base_dir)
        self.data_dir = os.path.join(self.root_dir, "data")
        self.assets_dir = os.path.join(self.root_dir, "assets")

        self.setWindowTitle("状態一覧")
        self.setMinimumSize(1100, 900)

        self.states_meta = []
        self._load_states_meta()
        self._build_ui()

    # ---------------------------------------------------------
    def _load_states_meta(self):
        path = os.path.join(self.data_dir, "states.json")
        if not os.path.exists(path):
            print("[StepStateIntro] states.json が見つかりません:", path)
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            self.states_meta = [
                {
                    "id": sid,
                    "name": meta.get("name", sid),
                    "description": meta.get("description", ""),
                    "thumbnail": meta.get("thumbnail", "")
                }
                for sid, meta in data.items()
            ]
        else:
            self.states_meta = data

    # ---------------------------------------------------------
    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(20, 20, 20, 20)
        main.setSpacing(20)

        # タイトル
        title = QLabel("状態一覧（サムネイル + 説明）")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        main.addWidget(title)

        # 中央2カラム
        center = QHBoxLayout()
        center.setSpacing(20)

        # 左：状態リスト
        self.list_states = QListWidget()
        self.list_states.setStyleSheet("font-size: 20px;")
        for meta in self.states_meta:
            item = QListWidgetItem(f"{meta['id']} : {meta['name']}")
            item.setData(Qt.UserRole, meta["id"])
            self.list_states.addItem(item)
        self.list_states.currentItemChanged.connect(self.on_state_changed)
        center.addWidget(self.list_states, 1)

        # 右：サムネイル + 説明
        right = QVBoxLayout()
        right.setSpacing(20)

        self.thumb_label = QLabel()
        self.thumb_label.setAlignment(Qt.AlignCenter)
        self.thumb_label.setFixedHeight(300)
        right.addWidget(self.thumb_label)

        self.txt_desc = QTextEdit()
        self.txt_desc.setReadOnly(True)
        self.txt_desc.setStyleSheet("font-size: 20px;")
        right.addWidget(self.txt_desc, 1)

        center.addLayout(right, 2)

        main.addLayout(center)

        # ---------------------------------------------------------
        # ★ 次へ（StepB4）ボタン追加
        # ---------------------------------------------------------
        btn_next = QPushButton("次へ（StepB4：魔法のことば）")
        btn_next.setStyleSheet("font-size: 22px; padding: 12px;")
        btn_next.clicked.connect(self.go_next)
        main.addWidget(btn_next)

        if self.list_states.count() > 0:
            self.list_states.setCurrentRow(0)

    # ---------------------------------------------------------
    def on_state_changed(self, current, previous):
        if not current:
            self.txt_desc.clear()
            self.thumb_label.clear()
            return

        sid = current.data(Qt.UserRole)
        meta = next((m for m in self.states_meta if m["id"] == sid), None)
        if not meta:
            return

        # --- サムネイル表示 ---
        thumb_path = os.path.join(self.assets_dir, meta.get("thumbnail", ""))
        if os.path.exists(thumb_path):
            pix = QPixmap(thumb_path).scaledToWidth(280, Qt.SmoothTransformation)
            self.thumb_label.setPixmap(pix)
        else:
            self.thumb_label.setText("サムネイルなし")

        # --- 説明表示 ---
        text = (
            f"状態ID：{meta['id']}\n"
            f"状態名：{meta['name']}\n\n"
            f"{meta['description']}"
        )
        self.txt_desc.setPlainText(text)

    # ---------------------------------------------------------
    # ★ StepB4 へ遷移
    # ---------------------------------------------------------
    def go_next(self):
        self.close()
        self.controller.show_stepB4()

