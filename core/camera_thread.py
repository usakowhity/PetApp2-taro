# core/camera_thread.py
import threading
import time
from core.expression_detector import ExpressionDetector


class CameraThread:
    """
    ExpressionDetector をバックグラウンドで動かし、
    笑顔検知イベントを controller に渡す。
    """

    def __init__(self, controller):
        self.controller = controller
        self.running = False
        self.detector = ExpressionDetector()

    def start(self):
        if self.running:
            return
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self.running:
            event = self.detector.detect()

            if event == "smile":
                self.controller.latest_camera_event = "smile"

            time.sleep(0.05)

    def stop(self):
        self.running = False
        self.detector.stop()
