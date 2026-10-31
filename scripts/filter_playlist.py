#!/usr/bin/env python3

import re
import sys
from pathlib import Path

EXCLUDED_CATEGORIES = {
"Lime (VPN🇷🇺)",
"Большое ТВ (VPN)",
"Turon Media (VPN)",
"info",
"Цитадель-Крым (VPN)",
"StarNet (VPN🇳🇱)",
"Наш Нет 🇺🇦",
"Itv.uz (🇺🇿)",
"Catcast 🐈 Not 24/7",
"TEST (VPN)",
"↕️ Торрент ТВ ↕️",
}

def get_group_title(entry):
for line in entry:
if line.startswith("#EXTINF:"):
match = re.search(
r'group-title\s*=\s*"([^"]*)"',
line,
re.IGNORECASE
)
if match:
return match.group(1).strip()

return None

def main():
if len(sys.argv) != 3:
print("Usage: python3 filter_playlist.py input.m3u output.m3u")
sys.exit(1)

source = Path(sys.argv[1])
destination = Path(sys.argv[2])

text = source.read_text(encoding="utf-8-sig")

if not text.lstrip().startswith("#EXTM3U"):
    sys.exit("ERROR: Invalid M3U playlist")

lines = text.splitlines()

header = []
entries = []
current_entry = []

for line in lines:
    if line.startswith("#EXTINF:"):
        if current_entry:
            entries.append(current_entry)

        current_entry = [line]

    elif current_entry:
        current_entry.append(line)

    else:
        header.append(line)

if current_entry:
    entries.append(current_entry)

kept = []
removed = 0

for entry in entries:
    group = get_group_title(entry)

    if group in EXCLUDED_CATEGORIES:
        removed += 1
    else:
        kept.extend(entry)

output = "\n".join(header + kept).rstrip() + "\n"

if not output.lstrip().startswith("#EXTM3U"):
    sys.exit("ERROR: Output playlist is invalid")

destination.write_text(output, encoding="utf-8")

print(f"Всего каналов: {len(entries)}")
print(f"Удалено каналов из запрещённых групп: {removed}")
print(f"Осталось каналов: {len(entries) - removed}")
print(f"Плейлист сохранён: {destination}")

if name == "main":
main()