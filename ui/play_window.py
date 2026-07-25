# ui/play_window.py

import time
import os
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
from PySide6.QtMultimediaWidgets import QVideoWidget


class PlayWindow(QWidget):

    IMAGE_RETURN_MS = 4000
    IDLE_SECONDS = 15
    SMILE_COOLDOWN_SECONDS = 3

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Play モード")
        self.setMinimumSize(900, 700)

        self.current_state = "n1"
        self.last_stimulus_time = time.time()
        self.smile_cooldown_until = 0.0
        self.controller.is_playing = False

        # タイマー
        self.return_timer = QTimer(self)
        self.return_timer.setSingleShot(True)
        self.return_timer.timeout.connect(self.return_to_n1)

        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self.check_idle)
        self.idle_timer.start(1000)

        # UI
        layout = QVBoxLayout(self)

        self.label_state = QLabel("状態：n1")
        self.label_state.setAlignment(Qt.AlignCenter)
        self.label_state.setStyleSheet("font-size: 24pt; font-weight: bold;")
        layout.addWidget(self.label_state)

        # 画像表示
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(800, 500)
        layout.addWidget(self.image_label)

        # 動画表示
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(800, 500)
        self.video_widget.hide()
        layout.addWidget(self.video_widget)

        # プレイヤー
        self.player = QMediaPlayer(self)
        self.audio = QAudioOutput(self)
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video_widget)

        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player.errorOccurred.connect(self.on_player_error)

        self._orig_pixmap = None

        # 共通サウンド
        self.sound_effect = QSoundEffect(self)
        self.sound_effect.setVolume(1.0)

        # ★ Controller の voice_signal を受け取る
        self.controller.voice_signal.connect(self.on_voice_detected)

        self.change_state("n1")

    # -------------------------
    # 外部イベント
    # -------------------------
    def on_voice_detected(self, state):
        self.last_stimulus_time = time.time()
        self.change_state(state)

    def on_face_detected(self):
        now = time.time()
        if now < self.smile_cooldown_until:
            return

        self.last_stimulus_time = now
        if self.current_state == "n1":
            self.change_state("p1")

    # -------------------------
    # 状態遷移
    # -------------------------
    def change_state(self, new_state):

        if new_state == self.current_state:
            return

        # p1/p12 の解決
        if new_state in ("p1", "p12") and new_state not in self.controller.media:
            if "p2" in self.controller.media:
                new_state = "p2"

        if new_state not in self.controller.media and new_state != "n1":
            return

        self.current_state = new_state
        self.update_state_display()
        self.play_media_for_state(new_state)

    # -------------------------
    # 無刺激チェック
    # -------------------------
    def check_idle(self):
        if self.current_state != "n1":
            return
        if time.time() - self.last_stimulus_time >= self.IDLE_SECONDS:
            self.change_state("n3")
            self.last_stimulus_time = time.time()

    # -------------------------
    # 表示更新
    # -------------------------
    def update_state_display(self):
        self.label_state.setText(f"状態：{self.current_state}")

    # -------------------------
    # メディア再生
    # -------------------------
    def play_media_for_state(self, state_code):

        self.return_timer.stop()
        try:
            self.player.stop()
        except:
            pass

        media_path = self.controller.media.get(state_code)

        # -------------------------
        # 動画
        # -------------------------
        if media_path and media_path.lower().endswith(".mp4"):

            self.controller.is_playing = True

            self.image_label.hide()
            self.video_widget.show()

            from PySide6.QtMultimedia import QMediaPlayer as _QMP
            if state_code == "n1":
                self.player.setLoops(_QMP.Loops.Infinite)
            else:
                self.player.setLoops(1)

            self.player.setSource(QUrl.fromLocalFile(media_path))
            self.player.play()

            # ★ p2 のときだけ鳴き声を鳴らす
            if state_code == "p2":
                species = self.controller.pet_profile.get("species", "")
                sound_path = None

                if species == "犬":
                    sound_path = os.path.join(self.controller.assets_dir, "common_sounds", "dog_bark.wav")
                elif species == "猫":
                    sound_path = os.path.join(self.controller.assets_dir, "common_sounds", "cat_meow.wav")
                elif species == "ウサギ":
                    sound_path = os.path.join(self.controller.assets_dir, "common_sounds", "rabbit_sound.wav")

                if sound_path and os.path.exists(sound_path):
                    self.sound_effect.setSource(QUrl.fromLocalFile(sound_path))
                    self.sound_effect.play()

            return

        # -------------------------
        # 静止画
        # -------------------------
        self.controller.is_playing = False
        self.video_widget.hide()
        self.image_label.show()

        if not media_path or not os.path.exists(media_path):
            self.image_label.setText("画像がありません")
            return

        pix = QPixmap(media_path)
        self._orig_pixmap = pix
        self._rescale_pixmap()

        if state_code != "n1":
            self.return_timer.start(self.IMAGE_RETURN_MS)

    # -------------------------
    # 動画終了
    # -------------------------
    def on_media_status_changed(self, status):
        from PySide6.QtMultimedia import QMediaPlayer as _QMP
        if status == _QMP.EndOfMedia and self.current_state != "n1":
            self.controller.is_playing = False
            self.return_to_n1()

    def on_player_error(self, error, error_string):
        self.controller.is_playing = False
        self.return_to_n1()

    # -------------------------
    # n1 に戻る
    # -------------------------
    def return_to_n1(self):
        if self.current_state in ("p1", "p2"):
            self.smile_cooldown_until = time.time() + self.SMILE_COOLDOWN_SECONDS

        self.current_state = "n1"
        self.last_stimulus_time = time.time()
        self.update_state_display()
        self.play_media_for_state("n1")

    # -------------------------
    # リサイズ
    # -------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._rescale_pixmap()

    def _rescale_pixmap(self):
        if not self._orig_pixmap:
            return
        w = self.image_label.width()
        h = self.image_label.height()
        scaled = self._orig_pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled)
