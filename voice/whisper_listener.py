# voice/whisper_listener.py

import threading
import time
import numpy as np
import jaconv
import difflib
from PySide6.QtCore import Signal, QObject


class WhisperBridge(QObject):
    """
    UIスレッドに安全に状態を渡すためのブリッジ
    """
    voice_signal = Signal(str)


class WhisperListener(threading.Thread):
    """
    WhisperTinyEngine 専用リスナー（静音版・スレッド安全版）
    """

    def __init__(self, controller, engine):
        super().__init__()
        self.controller = controller
        self.engine = engine
        self.running = True

        # 0.3秒 × 4 = 約1.2秒の音声バッファ
        self.buffer = []
        self.buffer_size = 4

        # ログ制御
        self.debug_match = False
        self.debug_p2 = False

        # ★ UIスレッドに渡すためのブリッジ
        self.bridge = WhisperBridge()
        self.bridge.voice_signal.connect(self.controller.on_voice_command)

        self.daemon = True

    # ---------------------------------------------------------
    # スレッド本体
    # ---------------------------------------------------------
    def run(self):
        print("[WhisperListener] スレッド開始")

        while self.running:
            audio = self.engine.record_chunk()

            if audio is None:
                time.sleep(0.05)
                continue

            self.buffer.append(audio)

            if len(self.buffer) < self.buffer_size:
                continue

            merged = np.concatenate(self.buffer)
            self.buffer.clear()

            text = self.engine.transcribe(merged)

            # ★ Whisper が返した生テキストを必ずログに出す
            print("[WhisperListener] raw:", text)

            if not text:
                continue

            # ★ 正規化
            norm = jaconv.kata2hira(jaconv.z2h(text)).strip()

            # ★ まず Controller に “生テキスト” を渡す（自動学習用）
            try:
                self.controller.on_voice_recognized(norm)
            except Exception as e:
                print("[WhisperListener] on_voice_recognized error:", e)

            # ★ ここから従来の状態判定
            if len(norm) >= 20:
                continue

            state = self.detect_state(norm)

            if state:
                # ★ UIスレッドに安全に渡す
                self.bridge.voice_signal.emit(state)

    # ---------------------------------------------------------
    # STATE_COMMANDS に基づく状態判定
    # ---------------------------------------------------------
    def detect_state(self, text):
        cmds = self.controller.STATE_COMMANDS

        def similar(a, b):
            return difflib.SequenceMatcher(None, a, b).ratio()

        # p2 最優先
        if "p2" in cmds:
            for w in cmds["p2"]:
                if not w:
                    continue

                if w == text:
                    return "p2"
                if w in text:
                    return "p2"
                if similar(w, text) >= 0.6:
                    return "p2"

        # その他
        for state, words in cmds.items():
            if state == "p2":
                continue

            for w in words:
                if not w:
                    continue

                if w == text:
                    return state
                if w in text:
                    return state
                if similar(w, text) >= 0.5:
                    return state

        return None

    # ---------------------------------------------------------
    def stop(self):
        self.running = False
        print("[WhisperListener] 停止要求")

