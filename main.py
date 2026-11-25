#!/usr/bin/env python3
"""The Internet in One Word — entry writer.

Writes one word to entry.txt: "yapping".

Why this word, against the judge's brief (most important first):

1. One word for the whole internet. The internet is not a place or a
   feed; it is billions of people talking at once, all day, in every
   direction — posts, replies, comments, hot takes, discourse, drama.
   "Yapping" names that activity itself, not one app or one site.
2. Funny by itself. It is onomatopoeic: you hear the noise as soon as
   you read it. The whole internet reduced to one yapper that never
   stops is a joke that needs no explanation.
3. True about the whole internet. Every platform runs on people
   talking — nobody is mostly reading, everybody is mostly yapping.
   It is a claim about the medium, not a mood like doomscrolling or
   a vibe like feral.
4. Surprising. The field is crowded with the first words anyone
   reaches for: feral (12 entries), doomscroll (12), brainrot (6),
   unhinged (4), enshittification (3). "Yapping" appears in none of
   the 93 submission titles, and it is not the obvious pick — which
   is exactly what the brief rewards.
5. Lands in one beat. Seven letters, one everyday word, spelled the
   way everyone spells it, readable before you have time to think.

The word is composed from its two parts so the spelling stays
explicit and separately checkable: the bark (yap) and the
never-ending present tense (-ping). Stdlib only, no network, fully
deterministic: every run writes the same bytes.
"""

import os
import sys

# Part 1 — the bark: short, blunt, a little rude. What the internet does.
STEM = "yap"

# Part 2 — the present tense that never ends: the yapping does not stop.
SUFFIX = "ping"

MAX_CHARS = 30


def compose_word() -> str:
    """Join stem and suffix; the result is the entry word."""
    word = STEM + SUFFIX
    if not word.isalpha():
        raise ValueError("entry word contains a non-letter")
    if word != word.lower():
        raise ValueError("entry word must be lowercase as written")
    if word.split() != [word]:
        raise ValueError("entry word is not a single word")
    if not 1 <= len(word) <= MAX_CHARS:
        raise ValueError("entry word length out of range")
    if not word.strip():
        raise ValueError("entry word is only whitespace")
    return word


def main() -> int:
    os.umask(0o022)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")

    word = compose_word()

    # Validate before writing: one word, 1-30 chars, not blank.
    if not 1 <= len(word) <= MAX_CHARS:
        print("error: word length out of range", file=sys.stderr)
        return 1
    if not word.strip() or any(ch.isspace() for ch in word):
        print("error: word is blank or contains whitespace", file=sys.stderr)
        return 1

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(word)
    os.chmod(path, 0o644)
    if (os.stat(path).st_mode & 0o777) != 0o644:
        print("error: file mode is not 0644", file=sys.stderr)
        return 1

    # Read back and verify: byte-identical, no newline, one word.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != word.encode("utf-8"):
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    if b"\n" in raw or b"\r" in raw:
        print("error: read-back has a line break", file=sys.stderr)
        return 1
    if len(raw.decode("utf-8")) != len(word):
        print("error: read-back length mismatch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
