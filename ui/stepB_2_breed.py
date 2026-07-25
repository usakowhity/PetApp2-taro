from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QPushButton, QScrollArea
)
from PySide6.QtCore import Qt


class StepB2BreedWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.profile = self.controller.pet_profile

        self.setWindowTitle("プロフィールを編集")
        self.setMinimumSize(900, 800)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        scroll.setWidget(container)
        form = QVBoxLayout(container)
        form.setSpacing(8)

        def add_labeled_row(label_text, widget):
            row = QHBoxLayout()
            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-size: 18pt;")
            row.addWidget(lbl, 1)
            row.addWidget(widget, 3)
            form.addLayout(row)

        # 種別
        self.cmb_species = QComboBox()
        self.cmb_species.addItems(["", "犬", "猫", "ウサギ"])
        self.cmb_species.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("種別：", self.cmb_species)

        # 品種
        self.cmb_breed = QComboBox()
        self.cmb_breed.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("品種：", self.cmb_breed)

        # 名前
        self.txt_name = QLineEdit()
        self.txt_name.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("名前：", self.txt_name)

        # 性別
        self.cmb_gender = QComboBox()
        self.cmb_gender.addItems(["", "オス", "メス"])
        self.cmb_gender.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("性別：", self.cmb_gender)

        # 年齢
        self.txt_age = QLineEdit()
        self.txt_age.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("年齢：", self.txt_age)

        # 毛色
        self.cmb_color = QComboBox()
        self.cmb_color.addItems(["", "白", "黒", "茶", "グレー", "その他"])
        self.cmb_color.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("毛色：", self.cmb_color)

        self.txt_color_free = QLineEdit()
        self.txt_color_free.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("毛色（自由記述）：", self.txt_color_free)

        # 毛の長さ
        self.cmb_fur = QComboBox()
        self.cmb_fur.addItems(["", "短毛", "中毛", "長毛"])
        self.cmb_fur.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("毛の長さ：", self.cmb_fur)

        # 耳
        self.cmb_ear = QComboBox()
        self.cmb_ear.addItems(["", "立ち耳", "垂れ耳", "その他"])
        self.cmb_ear.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("耳の形：", self.cmb_ear)

        self.txt_ear_free = QLineEdit()
        self.txt_ear_free.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("耳（自由記述）：", self.txt_ear_free)

        # しっぽ
        self.cmb_tail = QComboBox()
        self.cmb_tail.addItems(["", "短い", "長い", "丸い", "その他"])
        self.cmb_tail.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("しっぽ：", self.cmb_tail)

        self.txt_tail_free = QLineEdit()
        self.txt_tail_free.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("しっぽ（自由記述）：", self.txt_tail_free)

        # 模様
        self.cmb_pattern = QComboBox()
        self.cmb_pattern.addItems(["", "単色", "ぶち", "トラ柄", "手足の先の色が違う", "その他"])
        self.cmb_pattern.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("模様：", self.cmb_pattern)

        self.txt_pattern_free = QLineEdit()
        self.txt_pattern_free.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("模様（自由記述）：", self.txt_pattern_free)

        # メモ
        lbl_memo = QLabel("メモ：")
        lbl_memo.setStyleSheet("font-size: 22pt; font-weight: bold;")
        form.addWidget(lbl_memo)

        self.txt_memo = QTextEdit()
        self.txt_memo.setStyleSheet("font-size: 22pt;")
        form.addWidget(self.txt_memo)

        # 魔法のことば
        self.txt_magic_word = QLineEdit()
        self.txt_magic_word.setStyleSheet("font-size: 20pt; min-height: 45px;")
        add_labeled_row("魔法のことば：", self.txt_magic_word)

        # 魔法のことばに反応したときの仕草
        lbl_magic_action = QLabel("魔法の言葉に反応したときの仕草：")
        lbl_magic_action.setStyleSheet("font-size: 22pt; font-weight: bold;")
        form.addWidget(lbl_magic_action)

        self.txt_magic_action = QTextEdit()
        self.txt_magic_action.setStyleSheet("font-size: 22pt;")
        form.addWidget(self.txt_magic_action)

        main_layout.addWidget(scroll)

        # 下部ボタン
        btn_row = QHBoxLayout()
        btn_back = QPushButton("ようこそ！画面に戻る")
        btn_back.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_back.clicked.connect(self.on_back)
        btn_row.addWidget(btn_back)

        btn_save = QPushButton("保存してプロンプト一覧へ")
        btn_save.setStyleSheet("font-size: 22pt; padding: 10px;")
        btn_save.clicked.connect(self.save_and_next)
        btn_row.addWidget(btn_save)

        main_layout.addLayout(btn_row)

        # 先にシグナルを接続しておく（load_profile_to_ui が種別を設定した後に on_species_changed が動く）
        self.cmb_species.currentTextChanged.connect(self.on_species_changed)

        # 既存プロファイルを UI に反映（これが種別をセットする）
        self.load_profile_to_ui()

        # 種別に応じて品種リストを初期化（load_profile_to_ui で種別がセットされている前提）
        self.on_species_changed(self.cmb_species.currentText())

    def load_profile_to_ui(self):
        p = self.profile

        # 種別は先にセット（on_species_changed は接続済み）
        self.cmb_species.setCurrentText(p.get("species", ""))

        # 品種は on_species_changed 後に設定されるためここでは currentText を保持しておく
        # 名前等は直接反映
        self.txt_name.setText(p.get("name", ""))
        self.cmb_gender.setCurrentText(p.get("gender", ""))
        self.txt_age.setText(p.get("age", ""))

        self.cmb_color.setCurrentText(p.get("color", ""))
        self.txt_color_free.setText(p.get("color_free", ""))

        self.cmb_fur.setCurrentText(p.get("fur_length", ""))

        self.cmb_ear.setCurrentText(p.get("ear", ""))
        self.txt_ear_free.setText(p.get("ear_free", ""))

        self.cmb_tail.setCurrentText(p.get("tail", ""))
        self.txt_tail_free.setText(p.get("tail_free", ""))

        self.cmb_pattern.setCurrentText(p.get("pattern", ""))
        self.txt_pattern_free.setText(p.get("pattern_free", ""))

        self.txt_memo.setPlainText(p.get("memo", ""))

        self.txt_magic_word.setText(p.get("magic_word", ""))
        self.txt_magic_action.setPlainText(p.get("magic_action_free", ""))

        # 品種は種別に応じたリストが作られた後にセットするため、ここでは一時的に保持しておく
        # on_species_changed の最後で currentText を復元する処理がある
        # もし種別が空の場合は品種も空のままにする
        # （on_species_changed が呼ばれた後に self.cmb_breed.setCurrentText が行われる）
        # To ensure breed is restored, set it after a short logical step:
        breed = p.get("breed", "")
        if breed:
            # store as attribute so on_species_changed can restore it
            self._restore_breed_after_species = breed
        else:
            self._restore_breed_after_species = ""

    def on_species_changed(self, species):
        # species は "" もあり得る
        breeds = self.controller.BREED_DICT_BY_SPECIES.get(species, [])
        current = getattr(self, "_restore_breed_after_species", "") or self.cmb_breed.currentText().strip()

        # Build new list: keep an empty item, then ensure current (even if not in breeds) appears first, then add breeds
        self.cmb_breed.clear()
        self.cmb_breed.addItem("")

        # If current is non-empty and not already in breeds, add it so it won't be lost
        added = set()
        if current:
            self.cmb_breed.addItem(current)
            added.add(current)

        for b in breeds:
            if b not in added:
                self.cmb_breed.addItem(b)
                added.add(b)

        # Restore selection
        if current:
            self.cmb_breed.setCurrentText(current)
        else:
            # If profile had no breed, try to set to profile value (may be empty)
            self.cmb_breed.setCurrentText(self.profile.get("breed", ""))

        # clear the temporary restore holder
        self._restore_breed_after_species = ""

    def save_and_next(self):
        p = self.profile

        p["species"] = self.cmb_species.currentText().strip()

        # ★ 重要：品種が空文字の場合は既存の値を上書きしない（誤って消さない）
        new_breed = self.cmb_breed.currentText().strip()
        if new_breed:
            p["breed"] = new_breed
        # else: keep existing p["breed"] as-is

        p["name"] = self.txt_name.text().strip()
        p["gender"] = self.cmb_gender.currentText().strip()
        p["age"] = self.txt_age.text().strip()

        p["color"] = self.cmb_color.currentText().strip()
        p["color_free"] = self.txt_color_free.text().strip()

        p["fur_length"] = self.cmb_fur.currentText().strip()

        p["ear"] = self.cmb_ear.currentText().strip()
        p["ear_free"] = self.txt_ear_free.text().strip()

        p["tail"] = self.cmb_tail.currentText().strip()
        p["tail_free"] = self.txt_tail_free.text().strip()

        p["pattern"] = self.cmb_pattern.currentText().strip()
        p["pattern_free"] = self.txt_pattern_free.text().strip()

        p["memo"] = self.txt_memo.toPlainText().strip()

        p["magic_word"] = self.txt_magic_word.text().strip()
        p["magic_action_free"] = self.txt_magic_action.toPlainText().strip()

        # Persist back to controller and disk
        self.controller.pet_profile = p
        self.controller.save_profile()
        self.controller.prepare_voice_commands()
        self.controller.generate_all_prompts()

        self.close()
        self.controller.show_stepAllPromptsView()

    def on_back(self):
        self.close()
        self.controller.show_welcome()

