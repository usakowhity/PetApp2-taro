
# core/state_manager.py

import time


class StateManager:
    """
    PetApp2 最新仕様版 StateManager（PySide6 PlayWindow 用）

    - n1 のときだけ認識（音声・笑顔）
    - p2〜p12 の再生後は n1 に戻る
    - n1 に戻った直後は 1秒クールタイム
    - PlayWindow 側の play_media() を呼び出す
    - controller.media の素材パスを使用
    """

    def __init__(self, play_media_callback, get_media_path_callback):
        """
        play_media_callback(state_code: str)
            → UI 側で画像/動画を表示する

        get_media_path_callback(state_code: str) -> str | None
            → controller.media から素材パスを返す
        """
        self.play_media = play_media_callback
        self.get_media_path = get_media_path_callback

        # 現在の状態
        self.state = "n1"

        # クールタイム管理
        self.cooldown = False
        self.cooldown_end_time = 0

        # 再生終了後に n1 に戻すためのタイマー
        self.state_end_time = 0

        # 無刺激タイマー（任意）
        self.last_stimulus_time = time.time()

        # ペット情報（PlayWindow がセットする）
        # 例：
        # {
        #   "p2_word": "よしよし",
        #   "p12_word": "ジャンプ",
        #   ...
        # }
        self.pet_info = {}

        # 初回表示
        self.play_media("n1")

    # ============================================================
    # 音声コマンド（WhisperListener → PlayWindow → StateManager）
    # ============================================================
    def handle_voice_command(self, cmd: str):
        if not cmd:
            return

        # n1 以外では無視
        if self.state != "n1":
            return

        # クールタイム中は無視
        if self.cooldown:
            return

        # p12（魔法のことば）
        if "p12_word" in self.pet_info and cmd == self.pet_info["p12_word"]:
            self.change_state("p12")
            return

        # p3〜p11
        for key in ["p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11"]:
            if key in self.pet_info and cmd == self.pet_info[key]:
                self.change_state(key)
                return

        # p2（喜び）
        if "p2_word" in self.pet_info and cmd == self.pet_info["p2_word"]:
            self.change_state("p2")
            return

    # ============================================================
    # 笑顔検知（PlayWindow → StateManager）
    # ============================================================
    def handle_smile(self):
        if self.state == "n1" and not self.cooldown:
            self.change_state("p2")

    # ============================================================
    # 状態遷移
    # ============================================================
    def change_state(self, new_state: str):
        # 素材が無ければ遷移しない
        if not self.get_media_path(new_state):
            print(f"[WARN] {new_state} の素材がありません")
            return

        print(f"[STATE] {self.state} → {new_state}")

        self.state = new_state
        self.last_stimulus_time = time.time()

        # メディア再生
        self.play_media(new_state)

        # 再生終了後に n1 に戻す（2秒後）
        self.state_end_time = time.time() + 2.0

    # ============================================================
    # n1 に戻す
    # ============================================================
    def return_to_n1(self):
        self.state = "n1"
        self.play_media("n1")

        # クールタイム開始（1秒）
        self.cooldown = True
        self.cooldown_end_time = time.time() + 1.0

    # ============================================================
    # 毎フレーム呼び出し（PlayWindow.update_loop）
    # ============================================================
    def update(self):
        now = time.time()

        # クールタイム解除
        if self.cooldown and now >= self.cooldown_end_time:
            self.cooldown = False

        # n1 以外の状態 → 再生終了後に n1 へ
        if self.state != "n1" and now >= self.state_end_time:
            self.return_to_n1()

        # 無刺激タイマー（任意）
        if now - self.last_stimulus_time > 30:
            if self.state != "n1":
                self.return_to_n1()
