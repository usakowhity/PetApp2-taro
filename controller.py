import jaconv
import json
import os
import webbrowser
import difflib
from PySide6.QtCore import QObject, Signal

# =========================================================
#  パス・外部データ読み込み
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Controller] JSON load error {path}: {e}")
        return {}


STATE_META_JA = load_json(os.path.join(DATA_DIR, "states.json"))
STATE_META_EN = load_json(os.path.join(DATA_DIR, "states-en.json"))

# states.json が空でも壊れないようにフォールバック
if STATE_META_JA:
    STATE_LIST = list(STATE_META_JA.keys())
else:
    STATE_LIST = [
        "n1", "n2", "n3",
        "p1", "p2", "p3", "p4", "p5", "p6",
        "p7", "p8", "p9", "p10", "p11", "p12"
    ]

from data.breeds import (
    DOG_BREEDS,
    CAT_BREEDS,
    RABBIT_BREEDS,
    BREED_DICT_JA_EN,
)

SPECIES_EN = {
    "犬": "dog",
    "猫": "cat",
    "ウサギ": "rabbit",
}


# =========================================================
#  Controller 本体
# =========================================================

class Controller(QObject):
    face_signal = Signal()
    voice_signal = Signal(str)

    # WhisperListener.detect_state が参照する
    STATE_COMMANDS = {
        "n1": [],
        "n2": ["おすわり", "お座り", "すわれ", "すわって", "まて", "待て"],
        "n3": ["ねんね", "寝んね", "ねて", "おやすみ"],
        "p1": ["あそんで", "遊んで", "あそぼう", "遊ぼう", "おさんぽ", "さんぽ", "散歩", "いこう", "いくよ"],
        "p2": ["かわいい", "可愛い", "おりこう", "お利口", "よし"],
        "p3": ["ふせ", "伏せ"],
        "p4": ["おて", "お手", "て"],
        "p5": ["ごはん", "ご飯", "おいしい", "美味しい", "おやつ"],
        "p6": ["みず", "水", "おみず"],
        "p7": ["トイレ", "おしっこ", "シー"],
        "p8": ["もってこい", "持ってこい", "おいで"],
        "p9": ["ハウス", "おうち", "お家"],
        "p10": ["ちん", "たっち", "タッチ"],
        "p11": ["おふろ", "お風呂", "きれいきれい"],
        "p12": [],
    }

    BREED_DICT = BREED_DICT_JA_EN
    BREED_DICT_BY_SPECIES = {
        "犬": DOG_BREEDS,
        "猫": CAT_BREEDS,
        "ウサギ": RABBIT_BREEDS,
    }

    def __init__(self):
        super().__init__()
        self.window = None
        self.pet_profile = {}
        self.media = {}
        self.whisper = None
        self.face_detector = None
        self.is_playing = False

        self.BASE_DIR = BASE_DIR
        self.DATA_DIR = DATA_DIR
        self.GENERATED_DIR = GENERATED_DIR
        self.assets_dir = os.path.join(BASE_DIR, "assets")
        self.generated_dir = self.GENERATED_DIR

        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.GENERATED_DIR, exist_ok=True)

        self.load_profile()
        self.scan_generated_folder()
        self.face_signal.connect(self.on_face_detected)

    # ---------------------------------------------------------
    # プロファイル保存・読み込み
    # ---------------------------------------------------------
    def save_profile(self):
        path = os.path.join(self.DATA_DIR, "pet_profile.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.pet_profile, f, ensure_ascii=False, indent=2)
            print("[Controller] pet_profile saved:", self.pet_profile)
        except Exception as e:
            print("[Controller] pet_profile 保存エラー:", e)

    def load_profile(self):
        path = os.path.join(self.DATA_DIR, "pet_profile.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.pet_profile = json.load(f)
                print("[Controller] pet_profile loaded:", self.pet_profile)
            except Exception as e:
                print("[Controller] pet_profile 読み込みエラー:", e)
                self.pet_profile = {}
        else:
            print("[Controller] pet_profile.json not found")

        self.prepare_voice_commands()

    # ---------------------------------------------------------
    # generated フォルダスキャン
    # ---------------------------------------------------------
    def scan_generated_folder(self):
        folder = self.GENERATED_DIR
        if not os.path.exists(folder):
            print("[Controller] generated フォルダなし")
            return

        updated = {}
        for state in STATE_LIST:
            for ext in [".png", ".jpg", ".mp4"]:
                path = os.path.join(folder, f"{state}{ext}")
                if os.path.exists(path):
                    updated[state] = path
                    break
        self.media = updated
        print("[Controller] generated フォルダをスキャン:", updated)

    # ---------------------------------------------------------
    # 全状態のプロンプト生成
    # ---------------------------------------------------------
    def generate_all_prompts(self):
        print("[Controller] 全プロンプト生成開始")

        prompt_dir = os.path.join(self.generated_dir, "prompts")
        os.makedirs(prompt_dir, exist_ok=True)

        for state in STATE_LIST:
            try:
                text = self.build_prompt_for_state(state)
                file_path = os.path.join(prompt_dir, f"{state}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"[Controller] プロンプト保存: {file_path}")
            except Exception as e:
                print(f"[Controller] プロンプト生成失敗 {state}: {e}")

        print("[Controller] 全プロンプト生成完了")

    # ---------------------------------------------------------
    # 1状態のプロンプト生成（states.json / breeds.py 反映）
    # ---------------------------------------------------------
    def build_prompt_for_state(self, state: str) -> str:
        profile = self.pet_profile

        name = profile.get("name") or "this pet"
        species = profile.get("species", "ペット")
        breed = profile.get("breed", "")
        species_en = SPECIES_EN.get(species, species)
        breed_en = self.BREED_DICT.get(breed, "")

        meta_ja = STATE_META_JA.get(state, {})
        meta_en = STATE_META_EN.get(state, {})

        base_desc_ja = meta_ja.get("description", "")
        base_desc_en = meta_en.get("description", "")

        # ---------------------------------------------------------
        # 日本語 intro（重複しない）
        # ---------------------------------------------------------
        if breed:
            intro_ja = f"{breed}の{name}が、"
        else:
            intro_ja = f"{species}の{name}が、"

        # ---------------------------------------------------------
        # 英語 intro（重複しない）
        # ---------------------------------------------------------
        if breed_en:
            intro_en = f"A detailed, high-quality illustration of a {breed_en} named {name}, "
        else:
            intro_en = f"A detailed, high-quality illustration of a {species_en} named {name}, "

        # ---------------------------------------------------------
        # 日本語：プロフィール詳細（任意項目）
        # ---------------------------------------------------------
        detail_ja_parts = []
        if profile.get("color_free"):
            detail_ja_parts.append(profile["color_free"])
        if profile.get("fur_length"):
            detail_ja_parts.append(profile["fur_length"])
        if profile.get("ear_free"):
            detail_ja_parts.append(f"耳は「{profile['ear_free']}」")
        if profile.get("tail_free"):
            detail_ja_parts.append(f"しっぽは「{profile['tail_free']}」")
        if profile.get("pattern_free"):
            detail_ja_parts.append(f"模様は「{profile['pattern_free']}」")

        detail_ja = "、".join(detail_ja_parts)
        if detail_ja:
            detail_ja += "、"

        # ---------------------------------------------------------
        # p12（魔法のことば）
        # ---------------------------------------------------------
        if state == "p12":
            action = profile.get("magic_action_free", "").strip()

            if action:
                jp = f"{intro_ja}{detail_ja}飼い主の魔法のことばに反応して、「{action}」している様子。"
            else:
                jp = f"{intro_ja}{detail_ja}飼い主の魔法のことばに反応して、特別な仕草を見せる様子。"

            en = (
                f"{intro_en}"
                "showing a special gesture in response to the owner's magic word. "
                "Natural colors, soft lighting, cute and expressive, clean background."
            )

            return f"【Japanese Description】\n{jp}\n\n【English Prompt】\n{en}"

        # ---------------------------------------------------------
        # p2（喜び） species-specific（states-en.json の description_xxx を使用）
        # ---------------------------------------------------------
        if state == "p2":
            if species == "犬":
                detail_en = meta_en.get("description_dog", base_desc_en)
            elif species == "猫":
                detail_en = meta_en.get("description_cat", base_desc_en)
            elif species == "ウサギ":
                detail_en = meta_en.get("description_rabbit", base_desc_en)
            else:
                detail_en = base_desc_en

            jp = f"{intro_ja}{detail_ja}{base_desc_ja}"
            en = (
                f"{intro_en}"
                f"showing the following behavior: {detail_en} "
                "Natural colors, soft lighting, cute and expressive, clean background."
            )

            return f"【Japanese Description】\n{jp}\n\n【English Prompt】\n{en}"

        # ---------------------------------------------------------
        # その他の状態（n1〜n3、p1〜p12）
        # ---------------------------------------------------------
        jp = f"{intro_ja}{detail_ja}{base_desc_ja}"
        en = (
            f"{intro_en}"
            f"showing the following state: {base_desc_en} "
            "Natural colors, soft lighting, cute and expressive."
        )

        return f"【Japanese Description】\n{jp}\n\n【English Prompt】\n{en}"


    # ---------------------------------------------------------
    # 音声コマンド準備
    # ---------------------------------------------------------
    def generate_alias_variations(self, name):
        variations = set()

        # 元の名前
        variations.add(name)

        # ひらがな・カタカナ
        try:
            hira = jaconv.kata2hira(jaconv.z2h(name))
        except Exception:
            hira = name
        try:
            kata = jaconv.hira2kata(hira)
        except Exception:
            kata = name

        variations.add(hira)
        variations.add(kata)

        # 語尾バリエーション
        tails = ["", "ね", "よ", "だよ", "ちゃん", "さん", "くん", "ー", "っ"]
        for t in tails:
            variations.add(hira + t)
            variations.add(kata + t)

        # ローマ字
        try:
            romaji = jaconv.kana2alphabet(hira)
            variations.add(romaji)
            variations.add(romaji + "!")
        except Exception:
            pass

        return list(variations)

    def prepare_voice_commands(self):
        alias = self.pet_profile.get("name", "").strip()
        if alias:
            if alias not in self.STATE_COMMANDS["p2"]:
                self.STATE_COMMANDS["p2"].append(alias)
            variations = self.generate_alias_variations(alias)
            for v in variations:
                if v and v not in self.STATE_COMMANDS["p2"]:
                    self.STATE_COMMANDS["p2"].append(v)

        magic = self.pet_profile.get("magic_word", "").strip()
        if magic:
            if magic not in self.STATE_COMMANDS["p12"]:
                self.STATE_COMMANDS["p12"].append(magic)

    # ---------------------------------------------------------
    # WhisperListener からのコールバック
    # ---------------------------------------------------------
    def on_voice_recognized(self, text: str):
        # WhisperListener から正規化済みテキストが渡ってくる
        print(f"[Controller] Whisper recognized: {text}")

        # ここで将来的に「学習」や alias.json 更新をしてもよい
        # 今はログのみ

    def on_voice_command(self, state):
        # PlayWindow からの接続用（voice_signal）と
        # 直接 window メソッド呼び出しの両方をサポート
        try:
            self.voice_signal.emit(state)
        except Exception as e:
            print("[Controller] voice_signal emit error:", e)

        if hasattr(self.window, "on_voice_detected"):
            try:
                self.window.on_voice_detected(state)
            except Exception as e:
                print("[Controller] on_voice_detected 呼び出しエラー:", e)

    # ---------------------------------------------------------
    # 顔検出
    # ---------------------------------------------------------
    def on_face_detected(self):
        if hasattr(self.window, "on_face_detected"):
            try:
                self.window.on_face_detected()
            except Exception as e:
                print("[Controller] on_face_detected -> window handler error:", e)

    def request_face_detect(self):
        self.face_signal.emit()

    # ---------------------------------------------------------
    # Whisper / FaceDetector 起動
    # ---------------------------------------------------------
    def start_voice(self):
        try:
            import importlib
            wt = importlib.import_module("voice.whisper_tiny_engine")
            wl = importlib.import_module("voice.whisper_listener")
        except Exception as e:
            print("[Controller] Whisper モジュール読み込みエラー:", e)
            return

        if hasattr(wt, "WhisperTinyEngine"):
            engine = wt.WhisperTinyEngine()
            try:
                self.whisper = wl.WhisperListener(self, engine)
                self.whisper.daemon = True
                self.whisper.start()
            except Exception as e:
                print("[Controller] WhisperListener 起動エラー:", e)
        else:
            print("[Controller] WhisperTinyEngine クラスが見つかりません")

    def start_face_detection(self):
        try:
            from voice.face_detector import FaceDetector
            self.face_detector = FaceDetector(self)
            self.face_detector.daemon = True
            self.face_detector.start()
        except Exception as e:
            print("[Controller] 顔検出モジュール読み込みエラー:", e)

    def stop_face_detection(self):
        if self.face_detector:
            try:
                self.face_detector.stop()
            except Exception:
                pass
            self.face_detector = None

    # ---------------------------------------------------------
    # 画面遷移（window.close() を徹底）
    # ---------------------------------------------------------
    def _switch_window(self, win):
        if self.window:
            try:
                self.window.close()
            except Exception:
                pass
        win.show()
        self.window = win

    def show_welcome(self):
        try:
            from ui.welcome_window import WelcomeWindow
        except Exception as e:
            print("[Controller] WelcomeWindow 読み込みエラー:", e)
            return

        win = WelcomeWindow(self)
        self._switch_window(win)
        print("[Controller] WelcomeWindow 起動完了")

    def show_stepEditMenu(self):
        try:
            from ui.step_edit_menu import StepEditMenu
        except Exception as e:
            print("[Controller] StepEditMenu 読み込みエラー:", e)
            return

        win = StepEditMenu(self)
        self._switch_window(win)
        print("[Controller] StepEditMenu 起動完了")

    def show_stepB2(self):
        # 既存プロジェクトでの命名に合わせて複数候補を試す
        tried = []
        try:
            from ui.step_b2_breed_window import StepB2BreedWindow
            tried.append("ui.step_b2_breed_window.StepB2BreedWindow")
            win = StepB2BreedWindow(self)
            self._switch_window(win)
            print("★★ StepB2BreedWindow が表示された ★★")
            return
        except Exception as e:
            tried.append(f"step_b2_breed_window import error: {e}")

        try:
            from ui.stepB_2_breed import StepB2BreedWindow
            tried.append("ui.stepB_2_breed.StepB2BreedWindow")
            win = StepB2BreedWindow(self)
            self._switch_window(win)
            print("★★ StepB2BreedWindow (stepB_2_breed) が表示された ★★")
            return
        except Exception as e:
            tried.append(f"stepB_2_breed import error: {e}")

        print("[Controller] show_stepB2: どの StepB2 ウィンドウも読み込めませんでした。試行:", tried)

    def show_stepAllPromptsView(self):
        try:
            from ui.step_all_prompts_view import StepAllPromptsView
        except Exception as e:
            print("[Controller] StepAllPromptsView 読み込みエラー:", e)
            return

        self.scan_generated_folder()
        win = StepAllPromptsView(self)
        self._switch_window(win)
        print("[Controller] StepAllPromptsView 起動完了")

    def show_stepMediaView(self):
        try:
            from ui.step_media_view import StepMediaView
        except Exception as e:
            print("[Controller] StepMediaView 読み込みエラー:", e)
            return

        self.scan_generated_folder()
        win = StepMediaView(self)
        self._switch_window(win)
        print("[Controller] StepMediaView 起動完了")

    def show_stepAIGuideForMedia(self):
        try:
            from ui.step_ai_guide_for_media import StepAIGuideForMedia
        except Exception as e:
            print("[Controller] StepAIGuideForMedia 読み込みエラー:", e)
            return

        win = StepAIGuideForMedia(self)
        self._switch_window(win)
        print("[Controller] StepAIGuideForMedia 起動完了")

    def show_play(self):
        try:
            from ui.play_window import PlayWindow
        except Exception as e:
            print("[Controller] PlayWindow 読み込みエラー:", e)
            return

        self.prepare_voice_commands()

        play_window = PlayWindow(self)
        self._switch_window(play_window)

        # 音声認識開始
        self.start_voice()

        # 顔検出開始
        try:
            self.start_face_detection()
        except Exception as e:
            print("[Controller] 顔検出なし:", e)

        print("[Controller] PlayWindow 起動完了")

    # ---------------------------------------------------------
    # URL を開く
    # ---------------------------------------------------------
    def open_url(self, url: str):
        webbrowser.open(url)

    # ---------------------------------------------------------
    # アプリ起動
    # ---------------------------------------------------------
    def run(self):
        import sys
        from PySide6.QtWidgets import QApplication

        app = QApplication(sys.argv)
        try:
            self.show_welcome()
        except Exception as e:
            print("[Controller] show_welcome 呼び出しエラー:", e)
        sys.exit(app.exec())
