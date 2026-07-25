import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QScrollArea, QFrame, QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


STATE_INFO = [
    ("n1", "通常"),
    ("n2", "お座り"),
    ("n3", "寝んね"),
    ("p1", "遊んで"),
    ("p2", "喜び"),
    ("p3", "伏せ"),
    ("p4", "お手"),
    ("p5", "ごはん"),
    ("p6", "お水"),
    ("p7", "トイレ"),
    ("p8", "持ってこい"),
    ("p9", "ハウス"),
    ("p10", "ちん（タッチ）"),
    ("p11", "おふろ"),
    ("p12", "魔法のことば"),
]


class StepRegister(QWidget):
    """
    StepRegister：手持ち画像/動画の登録画面（JSON 保存対応版）
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("手持ち画像・動画の登録")
        self.setMinimumSize(900, 900)

        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- hero.png（絶対パス） ---
        base_dir = os.path.dirname(os.path.abspath(__file__))  # ui/
        root_dir = os.path.dirname(base_dir)                   # PetApp2/
        hero_path = os.path.join(root_dir, "assets", "ui", "hero.png")

        hero = QLabel()
        pixmap = QPixmap(hero_path)
        hero.setPixmap(pixmap.scaledToWidth(240, Qt.SmoothTransformation))
        hero.setAlignment(Qt.AlignCenter)
        layout.addWidget(hero)

        # タイトル
        title = QLabel("手持ち画像・動画の登録")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        desc = QLabel(
            "各状態に対応する画像または動画を登録してください。\n"
            "n1（代表画像/動画）は必ず登録してください。"
        )
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 16px;")
        layout.addWidget(desc)

        # -------------------------
        # スクロール領域
        # -------------------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QFrame()
        inner_layout = QVBoxLayout(inner)
        inner_layout.setSpacing(16)

        # JSON に既に保存されている場合は読み込む
        self.registered_files = self.controller.pet_images.copy()

        for code, name in STATE_INFO:
            row = QHBoxLayout()
            row.setSpacing(10)

            label = QLabel(f"{code}：{name}")
            label.setStyleSheet("font-size: 18px; font-weight: bold; width: 120px;")
            row.addWidget(label)

            # サムネイル
            thumb = QLabel()
            thumb.setFixedSize(120, 90)
            thumb.setAlignment(Qt.AlignCenter)
            thumb.setStyleSheet("border: 1px solid #ccc; font-size: 14px; color: #666;")

            # 既存データがあれば表示
            if code in self.registered_files and os.path.exists(self.registered_files[code]):
                path = self.registered_files[code]
                if path.lower().endswith((".png", ".jpg", ".jpeg")):
                    pix = QPixmap(path).scaled(120, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    thumb.setPixmap(pix)
                else:
                    thumb.setText("動画登録済み")
            else:
                thumb.setText("未登録")

            row.addWidget(thumb)

            # ボタン
            btn_img = QPushButton("画像を選択")
            btn_img.setStyleSheet("font-size: 16px; padding: 6px;")
            btn_img.clicked.connect(lambda _, c=code, t=thumb: self.select_file(c, "image", t))
            row.addWidget(btn_img)

            btn_vid = QPushButton("動画を選択")
            btn_vid.setStyleSheet("font-size: 16px; padding: 6px;")
            btn_vid.clicked.connect(lambda _, c=code, t=thumb: self.select_file(c, "video", t))
            row.addWidget(btn_vid)

            inner_layout.addLayout(row)

        scroll.setWidget(inner)
        layout.addWidget(scroll)

        # -------------------------
        # 次へ
        # -------------------------
        btn_next = QPushButton("次へ（状態ごとの特徴入力へ）")
        btn_next.setStyleSheet("font-size: 20px; padding: 10px; margin-top: 20px;")
        btn_next.clicked.connect(self.go_next)
        layout.addWidget(btn_next)

        self.setLayout(layout)

    # ---------------------------------------------------------
    # ファイル選択
    # ---------------------------------------------------------
    def select_file(self, state_code, file_type, thumb_label):
        dialog = QFileDialog(self)

        if file_type == "image":
            path, _ = dialog.getOpenFileName(self, "画像を選択", "", "画像 (*.png *.jpg *.jpeg)")
        else:
            path, _ = dialog.getOpenFileName(self, "動画を選択", "", "動画 (*.mp4 *.mov *.avi)")

        if not path:
            return

        # JSON 保存用に記録
        self.registered_files[state_code] = path

        # サムネイル更新
        if file_type == "image":
            pix = QPixmap(path).scaled(120, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            thumb_label.setPixmap(pix)
        else:
            thumb_label.setText("動画登録済み")

        print(f"{state_code} に {file_type} 登録: {path}")

    # ---------------------------------------------------------
    # 次へ
    # ---------------------------------------------------------
    def go_next(self):
        # n1 が未登録なら進めない
        if "n1" not in self.registered_files or not os.path.exists(self.registered_files["n1"]):
            print("n1（代表画像/動画）が未登録です")
            return

        # controller に保存
        self.controller.pet_images = self.registered_files

        # JSON 保存
        self.controller.save_profile()

        # 次の画面へ
        self.close()
        self.controller.show_stepB3()

