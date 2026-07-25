import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QHBoxLayout
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget


class StepMediaView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("画像/動画を変更・追加")
        self.setMinimumSize(1000, 800)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("状態ごとの画像/動画")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26pt; font-weight: bold;")
        layout.addWidget(title)

        body = QHBoxLayout()
        layout.addLayout(body)

        # 左：状態一覧
        self.list_states = QListWidget()
        self.list_states.setStyleSheet("font-size: 18pt;")
        body.addWidget(self.list_states, 1)

        # 右：プレビュー
        right = QVBoxLayout()
        body.addLayout(right, 2)

        # 画像プレビュー用
        self.preview_image = QLabel()
        self.preview_image.setAlignment(Qt.AlignCenter)
        self.preview_image.setMinimumSize(320, 320)
        self.preview_image.setStyleSheet("border: 1px solid #ccc; background: #fafafa;")

        # 動画プレビュー用
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(320, 320)
        self.video_widget.hide()

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video_widget)

        right.addWidget(self.preview_image)
        right.addWidget(self.video_widget)

        # ボタン
        btn_row = QHBoxLayout()
        right.addLayout(btn_row)

        btn_open_folder = QPushButton("generated フォルダを開く")
        btn_open_folder.setStyleSheet("font-size: 20pt; padding: 8px;")
        btn_open_folder.clicked.connect(self.on_open_folder)
        btn_row.addWidget(btn_open_folder)

        btn_back = QPushButton("編集メニューに戻る")
        btn_back.setStyleSheet("font-size: 20pt; padding: 8px;")
        btn_back.clicked.connect(self.on_back)
        btn_row.addWidget(btn_back)

        # 状態一覧を表示
        self.populate_states()
        self.list_states.currentItemChanged.connect(self.on_state_changed)

    def populate_states(self):
        self.list_states.clear()

        # ★ Controller.media を使う
        for state in sorted(self.controller.media.keys()):
            self.list_states.addItem(QListWidgetItem(state))

        if self.list_states.count() > 0:
            self.list_states.setCurrentRow(0)

    def on_state_changed(self, current, _prev):
        if not current:
            return

        state = current.text()
        path = self.controller.media.get(state)

        # まず動画を止める
        self.player.stop()
        self.video_widget.hide()
        self.preview_image.show()

        if not path or not os.path.exists(path):
            self.preview_image.setPixmap(QPixmap())
            self.preview_image.setText("画像/動画がありません")
            return

        # ★ 動画の場合
        if path.lower().endswith(".mp4"):
            self.preview_image.hide()
            self.video_widget.show()

            self.player.setSource(QUrl.fromLocalFile(path))
            self.player.play()
            return

        # ★ 画像の場合
        pix = QPixmap(path)
        if not pix.isNull():
            scaled = pix.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview_image.setPixmap(scaled)
            self.preview_image.setText("")
        else:
            self.preview_image.setPixmap(QPixmap())
            self.preview_image.setText("画像が読み込めません")

    def on_open_folder(self):
        folder = self.controller.GENERATED_DIR
        if os.path.exists(folder):
            import subprocess
            subprocess.Popen(f'explorer "{folder}"')

    def on_back(self):
        self.close()
        self.controller.show_stepEditMenu()

