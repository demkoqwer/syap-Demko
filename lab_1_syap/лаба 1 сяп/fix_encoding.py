# Converts every .py file in this folder to UTF-8 (pure ASCII script on purpose).
# Usage: put it next to main.py and run:  python fix_encoding.py
import os

folder = os.path.dirname(os.path.abspath(__file__))

for name in sorted(os.listdir(folder)):
    if not name.lower().endswith(".py") or name == os.path.basename(__file__):
        continue
    path = os.path.join(folder, name)
    with open(path, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8-sig")   # already UTF-8 (BOM allowed)
        status = "already UTF-8"
    except UnicodeDecodeError:
        text = raw.decode("cp1251")      # Windows Cyrillic ANSI
        status = "converted from cp1251"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(name + ": " + status)

print("Done. Now run main.py")
