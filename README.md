# Teaching skills for Claude Code

Three skills for **teaching**, **examining**, and **memorizing**, built for Claude Code and portable to other AI coding agents (Cursor, Codex, and more).

## The skills

- **learning-by-doing**: a hands-on teaching method. Concrete example first, quick theory, practice on something broken (where the connection forms), then redo alone. Handles concept vs skill, progressive hints, adaptive pacing, and spaced review. Grounded in 2025 learning research: avoiding metacognitive laziness, retrieval practice, spacing, Bloom's taxonomy, and the zone of proximal development. No dependencies, just a `SKILL.md`.
- **anki-flashcards**: generate Anki flashcards (`.apkg`) for spaced repetition. Picks up where learning-by-doing leaves off, to lock learning into long-term memory.
- **oral-examiner**: help an examiner question a student live to measure real understanding, not recitation. The mirror of learning-by-doing: it measures understanding instead of building it, with a Bloom climb, transfer questions, bias control, and rubric-based grading.

They all rest on the same evidence: active recall, spaced repetition, desirable difficulty, and Bloom's taxonomy.

## Install

### Via skills.sh (recommended)

```bash
npx skills add github:Dooc-Nuken/teaching-skills
```

Installs both skills. Restart your agent afterward.

### Manual

Copy each folder into `~/.claude/skills/`, then restart your agent.

```bash
git clone https://github.com/Dooc-Nuken/teaching-skills.git
cd teaching-skills
for s in learning-by-doing anki-flashcards oral-examiner; do
  mkdir -p ~/.claude/skills/"$s"
  cp -R ./skills/"$s"/. ~/.claude/skills/"$s"/
done
```

Windows (PowerShell):

```powershell
foreach ($s in "learning-by-doing","anki-flashcards","oral-examiner") {
  $dst = "$env:USERPROFILE\.claude\skills\$s"
  New-Item -ItemType Directory -Path $dst -Force | Out-Null
  Copy-Item -Path ".\skills\$s\*" -Destination $dst -Recurse -Force
}
```

## Dependencies

- **learning-by-doing**: none.
- **anki-flashcards**: Anki desktop and `uv`. The card script declares its Python dependency (genanki) inline, so `uv run` installs it automatically.

## Verify

In Claude Code, ask "list your available skills". You should see `learning-by-doing` and `anki-flashcards`.

## License

MIT. See [LICENSE](LICENSE).
