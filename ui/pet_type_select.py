import pygame
import sys

# PetApp2 内で使う設定を保存するためのグローバル変数
# （後で config_manager に置き換えてもOK）
SELECTED_PET_TYPE = None
SELECTED_BARK_MP3 = None
SELECTED_P2_TEMPLATE = None


class PetTypeSelectScreen:
    """
    ペット種選択画面（pygame）
    - 犬 / 猫 / うさぎ の3つから選択
    - 種別に応じて鳴き声 mp3 と p2 テンプレートを自動設定
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 600))
        pygame.display.set_caption("PetApp2 - ペット種選択")

        self.font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 24)

        # ボタン領域
        self.btn_dog = pygame.Rect(150, 250, 180, 80)
        self.btn_cat = pygame.Rect(360, 250, 180, 80)
        self.btn_rabbit = pygame.Rect(570, 250, 180, 80)

        self.btn_next = pygame.Rect(350, 450, 200, 70)

        self.selected = None  # "dog" / "cat" / "rabbit"

    def draw(self):
        self.screen.fill((240, 240, 240))

        # タイトル
        title = self.font.render("ペットの種類を選んでください", True, (0, 0, 0))
        self.screen.blit(title, (250, 100))

        # 犬
        pygame.draw.rect(self.screen, (200, 200, 255), self.btn_dog)
        self.screen.blit(self.small_font.render("犬", True, (0, 0, 0)),
                         (self.btn_dog.x + 70, self.btn_dog.y + 25))

        # 猫
        pygame.draw.rect(self.screen, (200, 255, 200), self.btn_cat)
        self.screen.blit(self.small_font.render("猫", True, (0, 0, 0)),
                         (self.btn_cat.x + 70, self.btn_cat.y + 25))

        # うさぎ
        pygame.draw.rect(self.screen, (255, 220, 200), self.btn_rabbit)
        self.screen.blit(self.small_font.render("うさぎ", True, (0, 0, 0)),
                         (self.btn_rabbit.x + 50, self.btn_rabbit.y + 25))

        # 選択中の表示
        if self.selected:
            msg = self.small_font.render(f"選択中：{self.selected}", True, (0, 0, 0))
            self.screen.blit(msg, (350, 350))

        # 次へボタン
        pygame.draw.rect(self.screen, (50, 150, 255), self.btn_next)
        self.screen.blit(self.font.render("次へ", True, (255, 255, 255)),
                         (self.btn_next.x + 50, self.btn_next.y + 15))

        pygame.display.update()

    def set_pet_type(self, pet_type):
        global SELECTED_PET_TYPE, SELECTED_BARK_MP3, SELECTED_P2_TEMPLATE

        SELECTED_PET_TYPE = pet_type

        # 鳴き声 mp3 の自動設定
        if pet_type == "犬":
            SELECTED_BARK_MP3 = "sounds/dog_bark.mp3"
            SELECTED_P2_TEMPLATE = "犬用の喜びテンプレート"
        elif pet_type == "猫":
            SELECTED_BARK_MP3 = "sounds/cat_meow.mp3"
            SELECTED_P2_TEMPLATE = "猫用の喜びテンプレート"
        elif pet_type == "うさぎ":
            SELECTED_BARK_MP3 = "sounds/rabbit_sound.mp3"
            SELECTED_P2_TEMPLATE = "うさぎ用の喜びテンプレート"

        self.selected = pet_type

    def run(self):
        while True:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_dog.collidepoint(event.pos):
                        self.set_pet_type("犬")

                    elif self.btn_cat.collidepoint(event.pos):
                        self.set_pet_type("猫")

                    elif self.btn_rabbit.collidepoint(event.pos):
                        self.set_pet_type("うさぎ")

                    elif self.btn_next.collidepoint(event.pos):
                        if self.selected:
                            # StepA-1（名前入力）へ遷移
                            from ui.stepA_name import StepANameScreen
                            StepANameScreen().run()
                            return
                        else:
                            print("ペット種を選択してください")
