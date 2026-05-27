# history.py
# This file handle saving and loading translation history
import os

HISTORY_FILE = "history.txt"

def save_to_history(original, translated, target_language):
    with open(HISTORY_FILE,"a", encoding="utf-8") as f:
        f.write(f"[{target_language}] {original}  → {translated}\n")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return[]
    with open(HISTORY_FILE, "r" , encoding="utf_8") as f:
        lines = f.readlines()
    return[line.strip() for line in lines if line.strip()]
def clear_history():
    with open(HISTORY_FILE, "W" , encoding="utf-8") as f:
        f.write("")