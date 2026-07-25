from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextBrowser
from PySide6.QtCore import Qt


class StepB1AIGuide(QWidget):
    """
    AI生成の全体ガイド。
    - n1 は「プロンプトのみ」でも「手持ち写真アップロード＋整形」でもOK
    - 以降の状態は n1 をアップロードして生成することを推奨
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("AI生成ガイド（概要）")

        layout = QVBoxLayout(self)

        title = QLabel("AI生成の流れ（概要）")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        text = QTextBrowser()
        text.setOpenExternalLinks(True)

        html = """
        <h3>1. n1（代表画像）の作り方</h3>
        <p>
        n1（代表画像）は、アプリ全体の基準となるとても重要な画像です。<br>
        次の2つの方法のどちらでも生成できます。
        </p>
        <ul>
          <li><b>① プロンプトのみで生成</b><br>
              手持ち写真が無い場合や、ゼロから生成したい場合に使います。<br>
              アプリが自動生成したプロンプトを、Gemini や Copilot に貼り付けてください。
          </li>
          <li><b>② 手持ち写真をアップロードして整形</b><br>
              手持ち写真が暗い・不鮮明・構図が悪い場合は、<br>
              AI サイト（Gemini / Copilot など）に写真をアップロードし、<br>
              その上でプロンプトを貼り付けて、綺麗な n1 を作成できます。
          </li>
        </ul>

        <h3>2. その他の状態（p1〜p12）の作り方</h3>
        <p>
        n1 が完成したら、以降の状態（p1〜p12）の画像・動画生成では、<br>
        <b>AI サイトに n1 画像をアップロードしてからプロンプトを貼り付ける</b>ことを推奨します。<br>
        こうすることで、生成されるペットの姿が n1 と揃い、<br>
        あなたのペットにより近い世界観を保つことができます。
        </p>

        <h3>3. プロンプトについて</h3>
        <p>
        各状態のプロンプトは、アプリが自動生成します。<br>
        <code>generated/prompts/◯◯.txt</code> に保存され、<br>
        StepC_generate や StepPromptConfirm の画面から確認・コピーできます。<br>
        日本語説明と English Prompt の両方が含まれます。
        </p>
        """

        text.setHtml(html)
        layout.addWidget(text)

        btn_next = QPushButton("次へ")
        btn_next.clicked.connect(self.on_next)
        layout.addWidget(btn_next)

    def on_next(self):
        self.controller.show_stepB2()
