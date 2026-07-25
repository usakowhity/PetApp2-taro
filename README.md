# 🐾 PetApp2 Portable

AIペットアプリ第2弾 — ユーザー自身のペット画像・動画を登録して楽しめるテンプレート版。  
笑顔（顔認識）や声掛け（音声認識）に反応する、インストール不要の Portable アプリです。

---

## 🔹 概要

**PetApp2 Portable** は、ユーザーが飼っている犬・猫・うさぎなどのペット画像や動画を登録し、  
デスクトップ上で表情や動作を再現できる AI ペットアプリです。

ZIP を展開するだけで利用でき、Python ランタイムを同梱した  
**Portable構成（PCの好きな場所に解凍して使えます／USB・SDカードも可）** になっています。

起動は **run.bat** を実行するだけ。インストールは不要です。

---

## 🔹 主な特徴

- **15種類の状態（n1～n3, p1〜p12）に対応**  
  通常・休憩・睡眠などの中立状態（n1〜n3）と、  
  遊び・喜び・お手・ごはんなどのポジティブ状態（p1〜p12）を切り替え可能。

- **AI画像/動画生成ガイド（Gemini / Copilot / Pika）を搭載**  
  ペット素材が不足している場合でも、外部AIツールで簡単に補完できるよう、  
  生成手順や利用方法をガイドします。

- **ペットのプロフィール（名前・種類・毛色など）を元に、15種類の状態に応じたAI生成プロンプト（日本語・英語）を自動生成**  
  各状態に最適化されたプロンプトを作成し、AI画像/動画生成を強力に支援します。

- **Portable版としてインストール不要、run.bat から起動可能**  
  Python埋め込み環境を同梱しているため、追加インストール不要。

---

## 🔹 動作環境

- OS：Windows 10 / Windows 11  
- GPU：不要  
- Python：同梱済み（Portable版）  
- インストール：不要（ZIP展開のみ）

---

## 🔹 使い方

1. ZIP をダウンロードし、PCの好きな場所（内蔵SSD/HDD、USBメモリ、SDカードなど）に解凍  
2. フォルダ内の **run.bat** を起動  
3. 「ようこそ！」画面でペットのプロフィールを登録  
4. 画像・動画を各状態（n1〜n3, p1〜p12）に割り当て  
5. PlayWindow でペットが動作開始  
6. 笑顔（顔認識）や声掛け（音声認識）に応じて状態が切り替わります

---

## 🔹 ダウンロード

- **Portable Edition（PCの好きな場所に解凍して使えます／USB・SDカードも可）**  
  https://github.com/usakowhity/PetApp2-portable/releases

- **GitHub Edition（開発者向け）**  
  https://github.com/usakowhity/PetApp2-portable

---

## 🔹 PetApp2 デモ版（3種類）

PetApp2-portable をベースにした、犬・猫・うさぎの **3つのデモ版** も公開中です。

| デモ版名 | ペット種 | リポジトリ | ダウンロード |
|-----------|-----------|-------------|---------------|
| PetApp2_shelly | 犬デモ版（シェルティ犬「Shelly」） | https://github.com/usakowhity/PetApp2_shelly | https://github.com/usakowhity/PetApp2_shelly/releases/latest |
| PetApp2_mimi | 猫デモ版（シャム猫「Mimi」） | https://github.com/usakowhity/PetApp2_mimi | https://github.com/usakowhity/PetApp2_mimi/releases/latest |
| PetApp2-peter | うさぎデモ版（ネザーランドドワーフ「Peter」） | https://github.com/usakowhity/PetApp2-peter | https://github.com/usakowhity/PetApp2-peter/releases/latest |

---

## 🔹 関連リンク

- **公式サイト（PetAppシリーズ）**  
  https://usakowhity.github.io/

- **DesktopPetApp（前作）**  
  https://usakowhity.github.io/DesktopPetApp/

- **PetApp3 – Taro Edition（Coming Soon）**  
  https://github.com/usakowhity/PetApp3

---

## 🐰 保護うさぎ活動の応援

usakowhity は、  
**一般社団法人うさぎとひとの幸せを支える会** が行う  
保護うさぎ活動を応援しています。

同会では、保護されたうさぎたちの医療ケア、飼育、里親募集、啓発活動を行っており、  
「ふじみ野うさぎハウス」「行田うさぎハウス」などの保護施設を運営しています。

- 活動の詳細：  
  https://usagi-support.org/
- 支援方法（寄付・クラウドファンディング）：  
  https://usagi-support.org/?p=453

---

## 📄 License

MIT License  
Copyright (c) 2024–2026 usakowhity


