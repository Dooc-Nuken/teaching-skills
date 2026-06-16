# /// script
# requires-python = ">=3.9"
# dependencies = ["genanki>=0.13"]
# ///
"""Create Anki flashcards (.apkg) from the CLI or a JSON batch.

Supports basic, reverse, and cloze card models. Writes a .apkg and, unless
--no-import is passed, opens it so Anki imports it (cross-platform).

This is an original implementation built on the open-source genanki library.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import genanki

# Stable, arbitrary model IDs (must stay constant across runs).
BASIC_MODEL = genanki.Model(
    1733401001,
    "Basic (teaching-skills)",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Source"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Back}}'
            '<br><br><div style="color:#888;font-size:12px">{{Source}}</div>',
        }
    ],
)

REVERSE_MODEL = genanki.Model(
    1733401002,
    "Basic reversed (teaching-skills)",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Source"}],
    templates=[
        {"name": "Card 1", "qfmt": "{{Front}}", "afmt": '{{FrontSide}}<hr id="answer">{{Back}}'},
        {"name": "Card 2", "qfmt": "{{Back}}", "afmt": '{{FrontSide}}<hr id="answer">{{Front}}'},
    ],
)

CLOZE_MODEL = genanki.Model(
    1733401003,
    "Cloze (teaching-skills)",
    fields=[{"name": "Text"}, {"name": "Source"}],
    templates=[
        {
            "name": "Cloze",
            "qfmt": "{{cloze:Text}}",
            "afmt": '{{cloze:Text}}<br><div style="color:#888;font-size:12px">{{Source}}</div>',
        }
    ],
    model_type=genanki.Model.CLOZE,
)


def make_note(card):
    model = card.get("model", "basic")
    source = card.get("source", "") or ""
    if model == "cloze":
        return genanki.Note(model=CLOZE_MODEL, fields=[card["question"], source])
    chosen = REVERSE_MODEL if model == "reverse" else BASIC_MODEL
    return genanki.Note(model=chosen, fields=[card["question"], card.get("answer", "") or "", source])


def stable_deck_id(name):
    # Derive a stable deck id from the name so repeated runs merge into one deck.
    return int(hashlib.md5(name.encode("utf-8")).hexdigest()[:8], 16)


def auto_import(path):
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", str(path)], check=False)
        elif sys.platform.startswith("win"):
            subprocess.run(["cmd", "/c", "start", "", str(path)], check=False)
        else:
            return False
        return True
    except FileNotFoundError:
        return False


def main():
    p = argparse.ArgumentParser(description="Create Anki flashcards (.apkg).")
    p.add_argument("-q", "--question", help="Card front, or cloze text with {{c1::...}}")
    p.add_argument("-a", "--answer", default="", help="Card back")
    p.add_argument("-s", "--source", default="", help="Optional citation")
    p.add_argument("-m", "--model", default="basic", choices=["basic", "reverse", "cloze"])
    p.add_argument("-d", "--deck", default="Claude Cards", help="Deck name")
    p.add_argument("--batch", help="JSON file: list of {question, answer, source?, model?}")
    p.add_argument("-o", "--output", default="claude-cards.apkg", help=".apkg output path")
    p.add_argument("--no-import", action="store_true", help="Write the file without opening Anki")
    args = p.parse_args()

    if args.batch:
        cards = json.loads(Path(args.batch).read_text(encoding="utf-8"))
        if not isinstance(cards, list) or not cards:
            p.error("--batch file must be a non-empty JSON list")
    elif args.question:
        cards = [{"question": args.question, "answer": args.answer, "source": args.source, "model": args.model}]
    else:
        p.error("provide -q/--question or --batch")

    deck = genanki.Deck(stable_deck_id(args.deck), args.deck)
    for card in cards:
        if "question" not in card:
            p.error(f"card missing 'question': {card!r}")
        deck.add_note(make_note(card))

    out = Path(args.output)
    genanki.Package(deck).write_to_file(out)
    print(f"Wrote {len(cards)} card(s) to {out} (deck: {args.deck})")

    if not args.no_import:
        if auto_import(out):
            print("Opened for import in Anki.")
        else:
            print(f"Could not auto-open. Import manually in Anki: File > Import > {out}")


if __name__ == "__main__":
    main()
