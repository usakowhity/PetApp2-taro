# core/prompt_generator.py

class PromptGenerator:
    """
    Centralized prompt generation for all states.
    All outputs are (jp, en) tuples.
    """

    def generate_prompt(
        self,
        state_code: str,
        pet_type: str,
        breed: str,
        name: str,
        color: str,
        ear: str,
        body: str,
        personality: str,
        feature: str,
    ):
        # Dispatch by state_code
        if state_code == "n1":
            return self._generate_n1(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "n2":
            return self._generate_n2(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "n3":
            return self._generate_n3(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "p1":
            return self._generate_p1(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "p2":
            return self._generate_p2(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "p3":
            return self._generate_p3(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "p4":
            return self._generate_p4(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "p5":
            return self._generate_p5(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "p6":
            return self._generate_p6(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "p7":
            return self._generate_p7(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "p8":
            return self._generate_p8(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "p9":
            return self._generate_p9(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "p10":
            return self._generate_p10(pet_type, breed, name, color, ear, body, personality, feature)
        if state_code == "p11":
            return self._generate_p11(pet_type, breed, name, color, ear, body, personality, feature)

        # Fallback
        jp = f"{pet_type}の「{name}」の画像。"
        en = f"An image of a {pet_type} named “{name}”."
        return jp, en

    # -------------------------
    # Neutral states
    # -------------------------
    def _generate_n1(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」が、通常状態で静かに待機している1枚の画像。"
            f"{ear}、{body}、{personality}の特徴を持ち、{feature}が自然に表情や姿勢に現れている。"
            "正面または少し斜めからの構図。背景はシンプル。高品質。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” with {color} fur, "
            f"in a calm normal idle state. Features include {ear}, {body}, {personality}, and {feature}, "
            "naturally reflected in posture and expression. Front or slight-angle view, simple background."
        )
        return jp, en

    def _generate_n2(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」がお座りしている1枚の画像。"
            f"背筋を伸ばして座り、落ち着いた表情。{ear}、{body}、{personality}が表れている。"
            "正面または少し斜めから。背景はシンプル。高品質。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” sitting upright (sit pose) with {color} fur. "
            f"Calm expression, showing {ear}, {body}, and {personality}. Front or slight-angle view, simple background."
        )
        return jp, en

    def _generate_n3(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」が寝転んで休んでいる、または眠っている1枚の画像。"
            "丸くなったり横になった自然な寝姿。柔らかい雰囲気。高品質。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” with {color} fur, lying down and resting or sleeping. "
            "Natural relaxed sleeping posture, soft atmosphere. Simple background."
        )
        return jp, en

    # -------------------------
    # Positive states
    # -------------------------
    def _generate_p1(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」が遊んでいる、またはお散歩しているアクティブな1枚の画像。"
            "楽しそうな動きや表情。高品質、シンプル背景。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” with {color} fur, playing or walking actively. "
            "Joyful movement or expression. Simple background."
        )
        return jp, en

    def _generate_p2(self, pet_type, breed, name, color, ear, body, personality, feature):
        if pet_type == "犬":
            jp = (
                f"{color}の毛を持つ{breed}の犬「{name}」が、犬特有の喜びのしぐさを見せている1枚の画像。"
                f"{ear}、{body}、{personality}の特徴を持ち、{feature}が表情に現れている。"
                "尻尾を大きく振り、耳が後ろに倒れ、口角が上がった“犬の笑顔”。"
                "前のめりで近づくような、全身で嬉しさを表現する自然な姿。高品質、シンプル背景。"
            )
            en = (
                f"A high-quality image of a {breed} dog named “{name}” with {color} fur, showing canine-specific joy. "
                f"Features include {ear}, {body}, {personality}, and {feature}, reflected naturally. "
                "Tail wagging widely, ears slightly pulled back, mouth corners lifted in a “dog smile”. "
                "Leaning forward with lively, full-body happy energy. Simple background."
            )
        elif pet_type == "猫":
            jp = (
                f"{color}の毛を持つ{breed}の猫「{name}」が、猫特有の喜びのしぐさを見せている1枚の画像。"
                f"{ear}、{body}、{personality}の特徴を持ち、{feature}が表情に現れている。"
                "しっぽをまっすぐ立てて先端が揺れ、目を細めた優しい表情。"
                "頬や体をすり寄せる、または前足をふみふみする姿。高品質、シンプル背景。"
            )
            en = (
                f"A high-quality image of a {breed} cat named “{name}” with {color} fur, showing feline-specific joy. "
                f"Features include {ear}, {body}, {personality}, and {feature}, expressed naturally. "
                "Tail raised with a gently twitching tip, soft narrowed eyes, rubbing its cheek or body, or kneading with its front paws. "
                "Simple background."
            )
        elif pet_type == "うさぎ":
            jp = (
                f"{color}の毛を持つ{breed}のうさぎ「{name}」が、喜びでピョンと跳ねている姿勢の1枚の画像。"
                f"{ear}、{body}、{personality}の特徴を持ち、{feature}が表情に現れている。"
                "耳がピンと立ち、体が軽く宙に浮く自然なジャンプの瞬間。明るい表情で、嬉しさが全身に表れている。高品質、シンプル背景。"
            )
            en = (
                f"A high-quality image of a {breed} rabbit named “{name}” with {color} fur, joyfully hopping in the air. "
                f"Features include {ear}, {body}, {personality}, and {feature}, reflected naturally. "
                "Ears standing upright, body slightly lifted in a natural happy jump, bright expression, full-body joyful energy. Simple background."
            )
        else:
            jp = f"{color}の毛を持つ{breed}の{pet_type}「{name}」が喜んでいる自然な姿の1枚の画像。高品質、シンプル背景。"
            en = f"A high-quality image of a {breed} {pet_type} named “{name}” with {color} fur, showing a joyful expression. Simple background."
        return jp, en

    def _generate_p3(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」が伏せの姿勢をしている1枚の画像。"
            "前足を伸ばして伏せている自然なポーズ。高品質、シンプル背景。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” in a down/lie-down pose. "
            "Front legs extended forward, natural posture. Simple background."
        )
        return jp, en

    def _generate_p4(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」が片手（前足）を上げてお手をしている1枚の画像。"
            "かわいらしい仕草で、正面または少し斜めから。高品質、シンプル背景。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” raising one paw to perform a shake gesture. "
            "Cute posture, front or slight-angle view. Simple background."
        )
        return jp, en

    def _generate_p5(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」がごはんを食べている、または食べたい様子を見せている1枚の画像。"
            "器の前で待っていたり、食べている自然な姿。高品質、シンプル背景。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” with {color} fur, eating food or eagerly waiting for food. "
            "Natural posture near a food bowl. Simple background."
        )
        return jp, en

    def _generate_p6(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」がお水を飲んでいる、または飲みたい様子の1枚の画像。"
            "水皿の前で自然な姿勢。高品質、シンプル背景。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” drinking water or wanting to drink. "
            "Natural posture near a water bowl. Simple background."
        )
        return jp, en

    def _generate_p7(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」がトイレに座っている、またはトイレ中の自然な姿勢の1枚の画像。"
            "清潔でシンプルな背景。高品質。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” sitting in a toilet area or in a natural toilet posture. "
            "Clean, simple background."
        )
        return jp, en

    def _generate_p8(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」がボールなどをくわえて持ってきている1枚の画像。"
            "楽しそうな表情と動き。高品質、シンプル背景。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” bringing a ball or toy in its mouth. "
            "Playful expression and movement. Simple background."
        )
        return jp, en

    def _generate_p9(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」がハウス（おうち）に入っている1枚の画像。"
            "落ち着いた表情で、安心した雰囲気。高品質、シンプル背景。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” inside its house or crate. "
            "Calm, relaxed atmosphere. Simple background."
        )
        return jp, en

    def _generate_p10(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」が後ろ足で立ち上がる「ちん（立っち）」のポーズをしている1枚の画像。"
            "バランスよく立っている自然な姿。高品質、シンプル背景。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” standing upright on its hind legs (stand pose). "
            "Balanced, natural posture. Simple background."
        )
        return jp, en

    def _generate_p11(self, pet_type, breed, name, color, ear, body, personality, feature):
        jp = (
            f"{color}の毛を持つ{breed}の{pet_type}「{name}」がきれいきれい・入浴・毛づくろいをしている1枚の画像。"
            "清潔感があり、柔らかい雰囲気。高品質、シンプル背景。"
        )
        en = (
            f"A high-quality image of a {breed} {pet_type} named “{name}” being cleaned, bathing, or grooming itself. "
            "Clean, soft atmosphere. Simple background."
        )
        return jp, en
