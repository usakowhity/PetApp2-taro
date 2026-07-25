# utils/state_loader.py

import json
from pathlib import Path

STATES_PATH = Path("data/states.json")

def load_states():
    """
    data/states.json を読み込み、状態定義を返す（読み取り専用）
    """
    if not STATES_PATH.exists():
        raise FileNotFoundError("data/states.json が見つかりません")
    with STATES_PATH.open(encoding="utf-8") as f:
        return json.load(f)

def is_valid_state(state_key):
    states = load_states()
    return state_key in states
