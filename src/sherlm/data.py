
from pathlib import Path
import re


def read_poems(path: str | Path) -> list[dict[str, str]]:
    """Read a text file and split it into individual poems."""

    text = Path(path).read_text(encoding="utf-8")
    sections = re.split(r"(?m)^\s*---\s*$", text)

    poems = []

    for section in sections:
        lines = section.strip().splitlines()

        if not lines:
            continue

        title = ""
        body_lines = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                title = line.lstrip("#").strip()
            else:
                body_lines.append(line)

        body = "\n".join(body_lines).strip()

        if body:
            poems.append({
                "title": title,
                "text": body,
            })

    return poems


def normalize_text(text: str) -> str:
    """Apply minimal, explicit Persian text normalization."""

    text = text.replace("ي", "ی").replace("ك", "ک")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> list[str]:
    """Create a simple whitespace-based word tokenizer."""

    text = normalize_text(text)

    # Keep the first experiment simple: remove common punctuation.
    text = re.sub(r"[،؛.!؟,:()\[\]«»\"“”]", "", text)

    return text.split()


if __name__ == "__main__":
    dataset_path = Path("data") / "hafez_ghazal_clean.txt"
    poems = read_poems(dataset_path)

    print(f"Number of poems: {len(poems)}")

    for i, poem in enumerate(poems, start=1):
        tokens = tokenize(poem["text"])

        print(
            f"{i:02d}. "
            f"Title: {poem['title'] or '(بدون عنوان)'} | "
            f"Tokens: {len(tokens)}"
        )