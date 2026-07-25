# ui/stepB_5_result.py

import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QTextEdit,
    QVBoxLayout, QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class StepB5_Result(QWidget):
    """
    外部AIで生成した画像/動画を貼り付けて確認する画面
    - プロンプトは controller.build_prompt_for_state() を使用
    """

    def __init__(self, controller, state_code=None, generated_qimage=None):
        super().__init__()
        self.controller = controller
        self.state_code = state_code

        self.setWindowTitle("生成結果の確認")
        self.setGeometry(200, 200, 900, 900)

        self.setStyleSheet("""
            QLabel { font-size: 20px; }
            QTextEdit { font-size: 18px; }
            QPushButton { font-size: 22px; padding: 10px; }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # ---------------------------------------------------------
        # hero.png（上部に表示）
        # ---------------------------------------------------------
        base_dir = os.path.dirname(os.path.abspath(__file__))  # ui/
        root_dir = os.path.dirname(base_dir)                   # PetApp2/
        hero_path = os.path.join(root_dir, "assets", "ui", "hero.png")

        hero = QLabel()
        if os.path.exists(hero_path):
            pixmap = QPixmap(hero_path)
            hero.setPixmap(pixmap.scaledToWidth(220, Qt.SmoothTransformation))
        else:
            hero.setText("hero.png が見つかりません")
        hero.setAlignment(Qt.AlignCenter)
        layout.addWidget(hero)

        # ---------------------------------------------------------
        # タイトル
        # ---------------------------------------------------------
        title = QLabel("生成結果の確認")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        layout.addWidget(title)

        # 状態名
        if state_code:
            lbl_state = QLabel(f"状態: {state_code}")
            lbl_state.setAlignment(Qt.AlignCenter)
            lbl_state.setStyleSheet("font-size: 20px;")
            layout.addWidget(lbl_state)

        # ---------------------------------------------------------
        # プロンプト表示（controller の build_prompt_for_state を使用）
        # ---------------------------------------------------------
        layout.addWidget(QLabel("使用したプロンプト（英語）"))

        self.prompt_box = QTextEdit()
        self.prompt_box.setReadOnly(True)
        layout.addWidget(self.prompt_box)

        if state_code:
            prompt = self.controller.build_prompt_for_state(state_code)
            self.prompt_box.setText(prompt)

        # ---------------------------------------------------------
        # 画像表示
        # ---------------------------------------------------------
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        if generated_qimage:
            pix = QPixmap.fromImage(generated_qimage)
            self.image_label.setPixmap(pix.scaledToWidth(500, Qt.SmoothTransformation))

        # ---------------------------------------------------------
        # 画像/動画読み込み
        # ---------------------------------------------------------
        btn_load = QPushButton("生成した画像/動画を読み込む")
        btn_load.clicked.connect(self.load_media)
        layout.addWidget(btn_load)

        # ---------------------------------------------------------
        # 戻る（素材登録へ）
        # ---------------------------------------------------------
        btn_finish = QPushButton("素材登録へ戻る")
        btn_finish.clicked.connect(self.go_back)
        layout.addWidget(btn_finish)

        self.setLayout(layout)

    # ---------------------------------------------------------
    # 画像/動画読み込み
    # ---------------------------------------------------------
    def load_media(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "生成物を選択", "", "Images/Video (*.png *.jpg *.jpeg *.mp4 *.mov)"
        )
        if not file:
            return

        # 保存
        self.controller.media[self.state_code] = file

        # 表示
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            pix = QPixmap(file)
            self.image_label.setPixmap(pix.scaledToWidth(500, Qt.SmoothTransformation))
        else:
            self.image_label.setText("動画ファイルを読み込みました")

    # ---------------------------------------------------------
    # 戻る（StepC_materials へ）
    # ---------------------------------------------------------
    def go_back(self):
        self.close()
        self.controller.show_stepC_materials()

