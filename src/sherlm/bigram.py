
from collections import Counter, defaultdict
from pathlib import Path
import random

from data import read_poems, tokenize


BOS = "<BOS>"
EOS = "<EOS>"


class BigramLanguageModel:
    def __init__(self):
        self.bigram_counts = defaultdict(Counter)
        self.unigram_counts = Counter()

    def fit(self, poems):
        """Learn word frequencies and adjacent-word frequencies."""
        for poem in poems:
            tokens = tokenize(poem["text"])

            if not tokens:
                continue

            sequence = [BOS] + tokens + [EOS]

            for current, next_word in zip(
                sequence[:-1], sequence[1:]
            ):
                self.bigram_counts[current][next_word] += 1
                self.unigram_counts[current] += 1

    def probability(self, current, next_word):
        """Estimate P(next_word | current) using observed bigrams."""
        total = self.unigram_counts[current]

        if total == 0:
            return 0.0

        count = self.bigram_counts[current][next_word]
        return count / total

    def most_likely_next(self, current, top_n=5):
        """Return the most frequent observed next words."""
        counts = self.bigram_counts[current]
        total = self.unigram_counts[current]

        if total == 0:
            return []

        return [
            (word, count / total)
            for word, count in counts.most_common(top_n)
        ]

    def generate(self, max_tokens=40, seed=42):
        """Generate text by sampling observed next-word transitions."""
        rng = random.Random(seed)
        current = BOS
        output = []

        for _ in range(max_tokens):
            candidates = self.bigram_counts[current]

            if not candidates:
                break

            words = list(candidates.keys())
            weights = list(candidates.values())

            next_word = rng.choices(words, weights=weights, k=1)[0]

            if next_word == EOS:
                break

            output.append(next_word)
            current = next_word

        return " ".join(output)


if __name__ == "__main__":
    dataset_path = Path("data") / "hafez_ghazal_clean.txt"
    poems = read_poems(dataset_path)

    model = BigramLanguageModel()
    model.fit(poems)

    print(f"Poems used: {len(poems)}")
    print(f"Unique observed words: {len(model.unigram_counts)}")

    word = "یک"
    print(f"\nPossible next words after '{word}':")

    for next_word, probability in model.most_likely_next(word):
        print(f"  {next_word}: {probability:.3f}")

    print("\nGenerated text:")
    print(model.generate(max_tokens=40))
