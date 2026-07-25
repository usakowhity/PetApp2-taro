# voice/face_detector.py

import threading
import time
import cv2
from PySide6.QtCore import QObject, Signal


class FaceBridge(QObject):
    """
    UIスレッドに安全に顔検出イベントを渡すためのブリッジ
    """
    face_signal = Signal()


class FaceDetector(threading.Thread):
    """
    顔検出 → p1 を Controller に通知するスレッド（完全スレッド安全版）
    """

    def __init__(self, controller, device_index=0):
        super().__init__()
        self.controller = controller
        self.running = True

        # UIスレッドに渡すためのブリッジ
        self.bridge = FaceBridge()
        self.bridge.face_signal.connect(self.controller.on_face_detected)

        # カメラ
        self.cap = cv2.VideoCapture(device_index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print("[FaceDetector] カメラを開けませんでした")

        # HaarCascade
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        # クールダウン（連続検出防止）
        self.last_detect = 0
        self.cooldown = 5.0

        self.daemon = True

    # ---------------------------------------------------------
    def run(self):
        print("[FaceDetector] スレッド開始")

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.05)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(80, 80)
            )

            if len(faces) > 0:

                # ★ 動画再生中は顔検出を無視（p1 暴走防止）
                if getattr(self.controller, "is_playing", False):
                    time.sleep(0.05)
                    continue

                now = time.time()
                if now - self.last_detect > self.cooldown:
                    print("[FaceDetector] 顔検出 → p1")
                    self.last_detect = now

                    # ★ UIスレッドに安全に渡す
                    self.bridge.face_signal.emit()

            time.sleep(0.05)

        print("[FaceDetector] スレッド終了")

    # ---------------------------------------------------------
    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
        print("[FaceDetector] 停止要求")
