import pyaudio
import numpy as np
import importlib

whisper = importlib.import_module("whisper")


class WhisperTinyEngine:
    def __init__(self, device_index=None, rate=16000, chunk=4800):
        self.rate = rate
        self.chunk = chunk

        self.model = whisper.load_model("tiny")

        self.pa = pyaudio.PyAudio()

        # ★ デバイス自動選択
        if device_index is None:
            try:
                device_index = self.pa.get_default_input_device_info().get("index", 0)
                print("[WhisperTiny] Using default input device:", device_index)
            except Exception as e:
                print("[WhisperTiny] Could not get default device:", e)
                device_index = 0

        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            input_device_index=device_index
        )

    def record_chunk(self):
        try:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
        except Exception as e:
            print("[WhisperTiny] read error:", e)
            return None

        audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

        # ★ 無音フィルタを緩める
        if np.abs(audio).mean() < 0.0008:
            return None

        return audio

    def transcribe(self, audio):
        try:
            result = self.model.transcribe(
                audio,
                fp16=False,
                language="ja",
                temperature=0.2,
                no_speech_threshold=0.5,
                condition_on_previous_text=False
            )
            return result.get("text", "").strip()
        except Exception as e:
            print("[WhisperTiny] transcribe error:", e)
            return ""

