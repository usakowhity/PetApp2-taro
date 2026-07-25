# core/expression_detector.py

import cv2
import time
import os


class ExpressionDetector:
    """
    DesktopPetApp 用：笑顔検出（イベント返却型）

    - detect() を呼ぶと 1 フレーム処理
    - 笑顔を検出したら "smile" を返す
    - それ以外は None を返す
    - PlayWindow / AppController と完全互換
    """

    def __init__(self, camera_index=0):
        self.camera_index = camera_index

        # HaarCascade のパス
        base = "data"
        self.face_cascade_path = os.path.join(base, "haarcascade_frontalface_default.xml")
        self.smile_cascade_path = os.path.join(base, "haarcascade_smile.xml")

        # カスケード読み込み
        self.face_cascade = cv2.CascadeClassifier(self.face_cascade_path)
        self.smile_cascade = cv2.CascadeClassifier(self.smile_cascade_path)

        # カメラ
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print("[Camera] カメラが開けませんでした")

        # クールダウン（連続反応防止）
        self.smile_cooldown = 2.0
        self.last_smile_time = 0.0

    # ------------------------------------------------------------
    # 1フレーム処理してイベント返却
    # ------------------------------------------------------------
    def detect(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 顔検出
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(80, 80)
        )

        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]

            # 笑顔検出
            smiles = self.smile_cascade.detectMultiScale(
                face_roi,
                scaleFactor=1.7,
                minNeighbors=20,
                minSize=(30, 30)
            )

            if len(smiles) > 0:
                now = time.time()

                # クールダウン中なら無視
                if now - self.last_smile_time < self.smile_cooldown:
                    return None

                self.last_smile_time = now
                return "smile"

        return None

    # ------------------------------------------------------------
    # 停止処理
    # ------------------------------------------------------------
    def stop(self):
        if self.cap.isOpened():
            self.cap.release()
