# play/play_manager.py

import os
from pathlib import Path
os.environ["IMAGEIO_FFMPEG_EXE"] = str(Path(__file__).resolve().parent.parent / "ffmpeg" / "ffmpeg.exe")

from moviepy.editor import VideoFileClip
import pygame
import sys

import json
import time
import datetime


class PlayManager:
    """
    PetApp2 Play Mode 中核クラス（音声コマンド対応版）

    - generated/ 内の画像(png/jpg)・動画(mp4)を状態コードごとに再生
    - WhisperListener → CommandParser → latest_voice_command を監視して状態遷移
    """

    def __init__(self, controller):
        pygame.init()

        self.controller = controller  # WhisperListener がここにいる

        # 画面
        self.screen_size = (600, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.setCaption("PetApp2 - Play Mode")

        # 状態定義・エイリアス・ペット情報
        self.states = self.load_states()
        self.alias = self.load_alias()
        self.pet_info = self.load_pet_info()
        self.magic_word = self.pet_info.get("magic_word", None)

        # 初期状態は n1（必須）
        self.current_state = "n1"

        # 動画再生用
        self.current_clip = None
        self.current_clip_iter = None
        self.video_end_callback = None

        # タイマー
        self.last_stimulus_time = time.time()
        self.smile_cooldown_until = 0.0

        # 初回再生
        self.play_media_for_state(self.current_state)

    # ============================================================
    # 外部 JSON 読み込み
    # ============================================================
    def load_states(self):
        path = Path("data/states.json")
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    def load_alias(self):
        path = Path("data/states_alias.json")
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return data.get("states", {})
        return {}

    def load_pet_info(self):
        path = Path("data/pet_info.json")
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"name": "Unknown", "species": "Unknown"}

    # ============================================================
    # p1 / p12 の代用処理
    # ============================================================
    def resolve_play_state(self, state_code: str):
        if self.get_media_path(state_code):
            return state_code

        if state_code in ("p1", "p12"):
            if self.get_media_path("p2"):
                return "p2"

        return None

    # ============================================================
    # 状態遷移
    # ============================================================
    def change_state(self, new_state: str):
        resolved = self.resolve_play_state(new_state)
        if not resolved:
            print(f"[WARN] 状態 {new_state} に対応する素材がありません")
            return

        print(f"[STATE] {self.current_state} → {resolved}")
        self.current_state = resolved
        self.play_media_for_state(resolved)
        self.last_stimulus_time = time.time()

    # ============================================================
    # generated/ から素材を探す
    # ============================================================
    def get_media_path(self, state_code: str):
        base = os.path.join("generated", state_code)

        if os.path.exists(base + ".mp4"):
            return base + ".mp4"

        for ext in [".png", ".jpg", ".jpeg"]:
            path = base + ext
            if os.path.exists(path):
                return path

        return None

    # ============================================================
    # メディア再生
    # ============================================================
    def play_media_for_state(self, state_code: str):
        path = self.get_media_path(state_code)
        if not path:
            print(f"[WARN] {state_code} の素材が見つかりません")
            return

        self.current_clip = None
        self.current_clip_iter = None
        self.video_end_callback = None

        if path.endswith(".mp4"):
            self.play_video(path)
        else:
            self.play_image(path)

    # ============================================================
    # 画像再生
    # ============================================================
    def play_image(self, path: str):
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, self.screen_size)

        self.screen.fill((0, 0, 0))
        self.screen.blit(img, (0, 0))
        pygame.display.update()

        if self.current_state != "n1":
            pygame.time.set_timer(pygame.USEREVENT + 1, 4000, loops=1)
            self.video_end_callback = self.return_to_n1

    # ============================================================
    # 動画再生
    # ============================================================
    def play_video(self, path: str):
        print(f"[VIDEO] 再生: {path}")

        clip = VideoFileClip(path)
        clip = clip.resize(height=600)

        self.current_clip = clip
        self.current_clip_iter = clip.iter_frames(fps=clip.fps, dtype="uint8")

        if self.current_state != "n1":
            self.video_end_callback = self.return_to_n1

    # ============================================================
    # n1 に戻る
    # ============================================================
    def return_to_n1(self):
        if self.current_state in ("p1", "p2"):
            self.smile_cooldown_until = time.time() + 3.0

        self.current_state = "n1"
        self.play_media_for_state("n1")
        self.last_stimulus_time = time.time()

    # ============================================================
    # メインループ（音声コマンド対応）
    # ============================================================
    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            now = time.time()

            # WhisperListener → latest_voice_command を監視
            if self.controller.latest_voice_command:
                cmd = self.controller.latest_voice_command
                self.controller.latest_voice_command = None

                print(f"[VOICE CMD] 受信: {cmd}")
                self.change_state(cmd)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT + 1:
                    if self.video_end_callback:
                        cb = self.video_end_callback
                        self.video_end_callback = None
                        cb()

            if self.current_state == "n1":
                if now - self.last_stimulus_time >= 15.0:
                    self.change_state("n3")
                    self.last_stimulus_time = now

            if self.current_clip_iter:
                try:
                    frame = next(self.current_clip_iter)
                    surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

                    self.screen.fill((0, 0, 0))
                    x = (600 - surf.get_width()) // 2
                    self.screen.blit(surf, (x, 0))
                    pygame.display.update()

                except StopIteration:
                    self.current_clip_iter = None
                    if self.video_end_callback:
                        cb = self.video_end_callback
                        self.video_end_callback = None
                        cb()

            clock.tick(60)

        pygame.quit()
