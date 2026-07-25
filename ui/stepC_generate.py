# ui/stepC_generate.py

import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QListWidget, QListWidgetItem,
    QVBoxLayout, QHBoxLayout, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt


class StepCGenerateWindow(QWidget):
    """
    StepC：AI生成プロンプトの生成画面
    - missing_states のみ生成
    - all_states=True の場合は全状態を生成
    - n1 はプロンプトのみ or 写真アップロード整形の説明付き
    - p2 は動画プロンプト（species-specific）
    """

    def __init__(self, controller, missing_states=None, all_states=False):
        super().__init__()
        self.controller = controller
        self.missing_states = missing_states or []
        self.all_states = all_states

        self.setWindowTitle("AI生成プロンプト生成（StepC-Generate）")
        self.setMinimumSize(900, 900)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # タイトル
        title = QLabel("AI生成プロンプト生成")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        # 説明文
        desc = QLabel(
            "この画面では、AI生成に必要なプロンプトを自動生成します。\n\n"
            "● 手持ち素材がある場合 → そのまま登録してOK\n"
            "● 不足分だけ AI で生成したい場合 → 下のリストから生成\n"
            "● 手持ち素材が無い場合 → 全状態をAI生成できます\n\n"
            "生成されたプロンプトは generated/prompts/*.txt に保存され、\n"
            "StepPromptConfirm で確認・コピーできます。"
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 18px;")
        layout.addWidget(desc)

        # 対象リスト
        self.state_list = QListWidget()
        layout.addWidget(self.state_list)

        self._populate_states()

        # ボタン群
        btn_row = QHBoxLayout()

        btn_generate = QPushButton("選択した状態のプロンプトを生成")
        btn_generate.clicked.connect(self.generate_selected)
        btn_row.addWidget(btn_generate)

        btn_generate_all = QPushButton("表示されている全状態を生成")
        btn_generate_all.clicked.connect(self.generate_all)
        btn_row.addWidget(btn_generate_all)

        layout.addLayout(btn_row)

        btn_confirm = QPushButton("プロンプト一覧を確認（StepPromptConfirm）")
        btn_confirm.clicked.connect(self.go_prompt_confirm)
        layout.addWidget(btn_confirm)

        btn_back = QPushButton("戻る（素材管理へ）")
        btn_back.clicked.connect(self.go_back)
        layout.addWidget(btn_back)

        scroll.setWidget(container)
        main = QVBoxLayout(self)
        main.addWidget(scroll)

    # ---------------------------------------------------------
    # 対象状態リストを表示
    # ---------------------------------------------------------
    def _populate_states(self):
        self.state_list.clear()

        if self.all_states:
            # 全状態を生成
            states = [
                "n1", "n2", "n3",
                "p1", "p2", "p3", "p4", "p5", "p6",
                "p7", "p8", "p9", "p10", "p11", "p12"
            ]
        else:
            # 不足分のみ
            states = self.missing_states

        for s in states:
            item = QListWidgetItem(s)
            self.state_list.addItem(item)

    # ---------------------------------------------------------
    # 選択した状態のみ生成
    # ---------------------------------------------------------
    def generate_selected(self):
        item = self.state_list.currentItem()
        if not item:
            QMessageBox.warning(self, "選択なし", "生成する状態を選択してください。")
            return

        state = item.text()
        self._generate_state(state)

    # ---------------------------------------------------------
    # 全状態を生成
    # ---------------------------------------------------------
    def generate_all(self):
        count = self.state_list.count()
        if count == 0:
            QMessageBox.information(self, "対象なし", "生成対象がありません。")
            return

        for i in range(count):
            state = self.state_list.item(i).text()
            self._generate_state(state)

        QMessageBox.information(self, "完了", "すべてのプロンプトを生成しました。")

    # ---------------------------------------------------------
    # 1状態のプロンプト生成
    # ---------------------------------------------------------
    def _generate_state(self, state_id):
        """
        controller.build_prompt_for_state() を呼ぶだけで
        日本語＋英語プロンプトが generated/prompts/*.txt に保存される。
        """
        try:
            self.controller.build_prompt_for_state(state_id)
        except Exception as e:
            QMessageBox.warning(self, "エラー", f"{state_id} の生成中にエラーが発生しました：\n{e}")
            return

    # ---------------------------------------------------------
    # StepPromptConfirm へ
    # ---------------------------------------------------------
    def go_prompt_confirm(self):
        self.close()
        self.controller.show_stepPromptConfirm()   # ← 修正済み

    # ---------------------------------------------------------
    # 戻る（StepC_media）
    # ---------------------------------------------------------
    def go_back(self):
        self.close()
        self.controller.show_stepC_media()

