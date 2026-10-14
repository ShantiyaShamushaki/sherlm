
# SherLM — Learning Notes

## 1. Project Objective

SherLM is an educational project focused on understanding and
implementing a small language model for Persian poetry.

The project combines mathematical foundations, practical
implementation, controlled experiments, and technical documentation.

The goal is not to reproduce a production-scale language model.
The goal is to understand how language models learn statistical
patterns and generate sequences of text.

## 2. What Is a Language Model?

A language model assigns probabilities to sequences of tokens.

Given a sequence of previous tokens, an autoregressive language
model estimates the probability distribution of the next token.

Using the chain rule of probability, a sequence can be represented as:

P(x_1, x_2, ..., x_T)
= product of P(x_t | x_1, ..., x_{t-1})

This means that the probability of a complete sequence can be
decomposed into conditional probabilities for its individual tokens.

## 3. What Is a Token?

A token is a unit used to represent text for a model.

Depending on the tokenizer, a token may represent a character,
a word, part of a word, punctuation, or another text fragment.

Persian text introduces practical challenges such as:

- Arabic and Persian character variants
- Half-spaces and whitespace normalization
- Punctuation and line breaks
- Differences in spelling and orthography

We will investigate these issues before selecting a tokenization strategy.

## 4. Next-Token Prediction

Suppose a training sequence contains:

"به نام خداوند جان و خرد"

During training, the model learns to predict the next token
from the preceding context.

For example, given the context "به نام خداوند",
the model should assign a high probability to the appropriate
next token according to the training data.

This does not mean the model understands poetry in the human sense.
It learns statistical patterns that may capture aspects of
vocabulary, syntax, style, and poetic structure.

## 5. Experimental Environment

- Language: Python
- Deep learning framework: PyTorch
- Hardware: NVIDIA GeForce RTX 3050 Laptop GPU, 6 GB VRAM
- Python environment: Conda environment named `sherlm`

GPU availability was verified with a matrix multiplication
performed on the CUDA device.

## 6. Open Questions

- Which Persian poetry dataset should we use?
- How should we normalize Persian text?
- Should we begin with character-level or subword tokenization?
- What is the smallest useful model architecture?
- How will we evaluate generated poetry?
