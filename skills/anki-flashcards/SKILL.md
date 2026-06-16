---
name: anki-flashcards
description: Create Anki flashcards (.apkg) from questions, notes, or extracted Q&A pairs and import them into Anki for spaced repetition. Supports basic, reverse, and cloze cards, single cards or JSON batches. Use when the user says "make anki cards", "create flashcards", "add to anki", "flashcard this", or wants to memorize specific content with spaced repetition.
license: MIT
---

# Anki Flashcards

Turn content into Anki flashcards and import them for spaced repetition.

## When to use

Trigger when the user explicitly wants flashcards: "make anki cards", "create flashcards", "add to anki", "flashcard this", "remember this in anki".

Do NOT trigger for general note-taking, summarizing, or learning Q&A. Only when the user wants cards.

## Dependencies

- **Anki** desktop installed (for auto-import).
- **uv** on PATH. The script declares its Python dependency (genanki) inline, so `uv run` installs it automatically. No manual venv.

Install the skill at `~/.claude/skills/anki-flashcards/`; the paths below assume that location.

## Step 1: write atomic Q&A pairs

- One idea per card. Do not combine concepts.
- Self-contained question: "In the two-component model, what is storage strength?" not "What is storage strength?"
- Testable: a specific, recallable answer must exist.
- Avoid list cards ("name all 7 ..."), they are hard to recall. Split them.
- Add a source when known.

For 3 or more cards, write a JSON batch instead of many single calls.

## Step 2: run the script

Single card:

```
uv run ~/.claude/skills/anki-flashcards/scripts/create_cards.py \
  -q "What is the optimal interval for partial recall?" \
  -a "30 to 50% of the perfect-recall interval" \
  -s "Bjork & Bjork (2011)"
```

Cloze card (put the deletions in -q, omit -a):

```
uv run ~/.claude/skills/anki-flashcards/scripts/create_cards.py \
  -m cloze -q "The capital of France is {{c1::Paris}}."
```

Reverse card (tested both directions): add `-m reverse`.

Batch from a JSON file, into a named deck:

```
uv run ~/.claude/skills/anki-flashcards/scripts/create_cards.py --batch cards.json -d "My Deck"
```

## Batch JSON schema

```json
[
  { "question": "Q text", "answer": "A text", "source": "optional", "model": "basic" }
]
```

`model` is one of `basic` (default), `reverse`, `cloze`. For `cloze`, put the deletions in `question` and omit `answer`.

## Step 3: confirm

After the script runs, report the card count and deck in one short sentence. The script writes a `.apkg` and opens it so Anki imports it (cross-platform: macOS, Linux, Windows). If Anki is closed, give the user the `.apkg` path to import manually via File then Import.

## CLI flags

- `-q, --question` card front, or cloze text
- `-a, --answer` card back
- `-s, --source` optional citation
- `-m, --model` `basic` (default), `reverse`, `cloze`
- `-d, --deck` deck name (default "Claude Cards")
- `--batch` JSON file of cards
- `-o, --output` .apkg path (default claude-cards.apkg)
- `--no-import` write the .apkg without opening Anki

## Card quality

Good cards are atomic, phrased as a question, and have one recallable answer. Effortful retrieval (desirable difficulty) builds stronger memory than easy recognition, so prefer questions that force recall over cards that merely show information.
