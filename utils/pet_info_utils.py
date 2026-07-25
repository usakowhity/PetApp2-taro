# utils/pet_info_utils.py

from pathlib import Path
import json
import datetime

PET_INFO_PATH = Path("data/pet_info.json")
TEMPLATE = {
  "name": "",
  "species": "",
  "color": "",
  "ears": "",
  "tail": "",
  "magic_word": "",
  "magic_behavior": "",
  "states": [],
  "prompts": {}
}

def ensure_pet_info():
    PET_INFO_PATH.parent.mkdir(parents=True, exist_ok=True)
    # 新規作成または空ファイル対応
    if not PET_INFO_PATH.exists() or PET_INFO_PATH.read_text(encoding="utf-8").strip() == "":
        PET_INFO_PATH.write_text(json.dumps(TEMPLATE, ensure_ascii=False, indent=2), encoding="utf-8")
        return TEMPLATE.copy()
    try:
        text = PET_INFO_PATH.read_text(encoding="utf-8")
        data = json.loads(text)
    except Exception:
        # バックアップして再初期化
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = PET_INFO_PATH.with_name(f"pet_info.json.bak.{ts}")
        PET_INFO_PATH.rename(backup)
        PET_INFO_PATH.write_text(json.dumps(TEMPLATE, ensure_ascii=False, indent=2), encoding="utf-8")
        return TEMPLATE.copy()
    # 欠損キー補完
    changed = False
    for k, v in TEMPLATE.items():
        if k not in data:
            data[k] = v
            changed = True
    if changed:
        PET_INFO_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data

def load_pet_info():
    ensure_pet_info()
    return json.loads(PET_INFO_PATH.read_text(encoding="utf-8"))

def save_prompts(prompts_dict):
    data = load_pet_info()
    data.setdefault("prompts", {})
    data["prompts"].update(prompts_dict)
    PET_INFO_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
