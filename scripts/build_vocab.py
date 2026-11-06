#!/usr/bin/env python3
"""Build data/vocab.json from data/source/*.xlsx (A1-A2) and data/<level>_words.csv (e.g. b1_words.csv).
CSV columns (no header): english,pos,thai   - pos is one of N, V, Adj, Adv, Pron, ...
Usage: pip install openpyxl && python3 scripts/build_vocab.py"""
import csv, glob, json
from pathlib import Path
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
rows, seen = [], set()

def add(en, pos, th, phrase, level):
    k = (en.strip().lower(), level == "LM")
    if k[0] and th and k not in seen:
        seen.add(k)
        rows.append([en.strip(), pos or "", th.strip(), phrase, level])

for x in sorted(glob.glob(str(ROOT / "data/source/*.xlsx"))):
    ws = load_workbook(x, read_only=True).active
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if r[1] and r[3]:
            add(str(r[1]), r[2], str(r[3]), 1 if r[7] == "วลี" else 0, r[4] or "A2")

for c in sorted(glob.glob(str(ROOT / "data/*_words.csv"))):
    level = Path(c).name.split("_")[0].upper()
    with open(c, encoding="utf-8", newline="") as f:
        for row in csv.reader(f):
            if len(row) >= 3 and not row[0].startswith("#"):
                add(row[0], row[1], row[2], 0, level)

import random
lm = [r for r in rows if r[4] == "LM"]
random.Random(7).shuffle(lm)  # IELTS list is alphabetical; shuffle so each day mixes letters
rows = [r for r in rows if r[4] != "LM"] + lm
(ROOT / "data/vocab.json").write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
for lv in ("A1", "A2", "B1", "B2", "C1", "LM"):
    print(lv, sum(1 for r in rows if r[4] == lv))
print("total", len(rows))
