#!/usr/bin/env python3

import re
import sys
from pathlib import Path

EXCLUDED_CATEGORIES = (
    "Lime",
    "Большое ТВ",
    "Turon Media",
    "INFO",
    "Цитадель-Крым",
    "StarNet",
    "Наш Нет",
    "Itv.uz",
    "CATCAST",
    "TEST",
    "Торрент ТВ",
)

# Категории, которые не должны попасть в результат.
# Сопоставление выполняется по group-title,
# а не по адресу потока.

def get_group_title(entry):
    for line in entry:
        if line.startswith("#EXTINF:"):
            match = re.search(
                r'group-title\s*=\s*"([^"]*)"',
                line,
                re.IGNORECASE
            )
            if match:
                return match.group(1).strip().casefold()

    return ""


def should_remove(entry):
    category = get_group_title(entry)

    if not category:
        return False

    return any(
        excluded in category
        for excluded in EXCLUDED_CATEGORIES
    )


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python3 filter_playlist.py "
            "input.m3u output.m3u"
        )
        sys.exit(1)

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])

    text = source.read_text(encoding="utf-8-sig")

    if not text.lstrip().startswith("#EXTM3U"):
        raise SystemExit("ERROR: Invalid M3U playlist")

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
        if should_remove(entry):
            removed += 1
        else:
            kept.extend(entry)

    output = "\n".join(header + kept).rstrip() + "\n"

    if not output.lstrip().startswith("#EXTM3U"):
        raise SystemExit("ERROR: Output playlist is invalid")

    destination.write_text(output, encoding="utf-8")

    print(f"Channels processed: {len(entries)}")
    print(f"Channels removed: {removed}")
    print(f"Channels remaining: {len(entries) - removed}")
    print(f"Saved to: {destination}")


if __name__ == "__main__":
    main()