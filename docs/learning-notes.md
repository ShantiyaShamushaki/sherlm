
# SherLM — Learning Notes

# 1. Project Objective

SherLM is an educational project focused on understanding and
implementing a small language model for Persian poetry.

The project combines mathematical foundations, practical
implementation, controlled experiments, and technical documentation.

The goal is not to reproduce a production-scale language model.
The goal is to understand how language models learn statistical
patterns and generate sequences of text.

## 1.2. What Is a Language Model?

A language model assigns probabilities to sequences of tokens.

Given a sequence of previous tokens, an autoregressive language
model estimates the probability distribution of the next token.

Using the chain rule of probability, a sequence can be represented as:

P(x_1, x_2, ..., x_T)
= product of P(x_t | x_1, ..., x_{t-1})

This means that the probability of a complete sequence can be
decomposed into conditional probabilities for its individual tokens.

## 1.3. What Is a Token?

A token is a unit used to represent text for a model.

Depending on the tokenizer, a token may represent a character,
a word, part of a word, punctuation, or another text fragment.

Persian text introduces practical challenges such as:

- Arabic and Persian character variants
- Half-spaces and whitespace normalization
- Punctuation and line breaks
- Differences in spelling and orthography

We will investigate these issues before selecting a tokenization strategy.

## 1.4. Next-Token Prediction

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

## 1.5. Experimental Environment

- Language: Python
- Deep learning framework: PyTorch
- Hardware: NVIDIA GeForce RTX 3050 Laptop GPU, 6 GB VRAM
- Python environment: Conda environment named `sherlm`

GPU availability was verified with a matrix multiplication
performed on the CUDA device.

## 1.6. Open Questions

- Which Persian poetry dataset should we use?
- How should we normalize Persian text?
- Should we begin with character-level or subword tokenization?
- What is the smallest useful model architecture?
- How will we evaluate generated poetry?

# 2. Building the First Statistical Language Model: Bigram

## 2.1. Objective

The first language model in SherLM is a statistical bigram language model. Its purpose is to learn simple word-transition patterns from a small Persian poetry corpus and use those patterns to generate new text.

Rather than understanding meaning or poetry, the model estimates the probability of a word appearing after another word. This provides a simple baseline against which more advanced neural language models can be compared.

## 2.2. What Is a Language Model?

A language model assigns probabilities to sequences of tokens. In next-token prediction, the model estimates the probability distribution of the next token given the preceding context.

In general, this can be expressed as:

$$
P(w_{t+1}\mid w_1,w_2,\ldots,w_t)
$$

where $w_1,\ldots,w_t$ represent the tokens observed so far.

A bigram model makes a simplifying assumption: the next word depends only on the immediately preceding word.

$$
P(w_{t+1}\mid w_1,\ldots,w_t)
\approx P(w_{t+1}\mid w_t)
$$

This assumption greatly simplifies the model and makes its behavior easy to inspect.

## 2.3. Learning Word-Transition Probabilities

SherLM estimates bigram probabilities by counting adjacent word pairs in the training corpus.

The maximum-likelihood estimate is:

$$
P(w_{t+1}\mid w_t)
=
\frac{C(w_t,w_{t+1})}{C(w_t)}
$$

Here:

- $C(w_t,w_{t+1})$ is the number of times the two words occur consecutively.
- $C(w_t)$ is the number of times the current word appears as the first element of a bigram.

For example, suppose the phrase "one day" appears eight times, "one time" appears twice, and "one night" appears twice. The model estimates:

$$
P(\text{day}\mid\text{one})=\frac{8}{12}
$$

$$
P(\text{time}\mid\text{one})
=P(\text{night}\mid\text{one})=\frac{2}{12}
$$

These probabilities are illustrative, not measurements from the SherLM corpus.

The model stores these counts in dictionaries rather than learning numerical parameters through gradient descent.

## 2.4. Sentence Boundaries

The implementation introduces two special tokens:

- `<BOS>`: Beginning of Sequence
- `<EOS>`: End of Sequence

Each poem is represented as a sequence beginning with `<BOS>` and ending with `<EOS>`. These markers allow the model to learn which words may start a poem and which words may end one.

For example:

`<BOS>یک ... <EOS>`

Each poem is processed independently, so the final word of one poem is not treated as the predecessor of the first word of another poem.

## 2.5. Generating Text

Text generation begins at `<BOS>`. At each step, the model samples a next word from the observed transition frequencies for the current word.

If a word has appeared with several different successors, more frequent successors receive greater sampling probability. Generation stops when `<EOS>` is sampled or the maximum output length is reached.

Because the model only considers the immediately preceding word, it cannot reliably maintain a topic, remember earlier lines, follow a rhyme scheme, or construct a coherent poetic argument.

The resulting text may contain valid Persian words and locally plausible word transitions while still being globally incoherent.

## 2.6. Initial Experiment and Observations

The first experiment used all 18 poems in the current dataset.

The observed output was:

- Poems processed: 18
- Reported vocabulary count: 676
- Observed successors after "یک": "روز", "شبی", and "جواب"
- Estimated probability of each displayed successor: approximately 0.333

The equal probabilities indicate that each of these three successors was observed once after "یک" in the processed corpus.

The generated text combined word transitions learned from the poems but did not consistently preserve grammatical or semantic coherence. This is an expected limitation of a first-order statistical model.

The reported vocabulary count should be interpreted carefully: the current implementation counts distinct symbols appearing as the first element of a bigram, including `<BOS>`. It is therefore not necessarily the exact number of distinct Persian words.

## 2.7. Limitations

The initial implementation has several limitations:

1. **Limited context:** It conditions each prediction on only one preceding word.
2. **Sparse observations:** Many possible word transitions never appear in a small corpus.
3. **Zero probabilities:** Any unobserved transition receives probability zero.
4. **Small dataset:** Eighteen poems are sufficient for a demonstration, but not for reliable evaluation or high-quality poetry generation.
5. **No semantic representation:** The model learns frequencies, not word meanings or relationships between concepts.
6. **No independent evaluation:** The first experiment uses the entire corpus for learning and generation. It does not yet measure performance on unseen poems.

## 2.8. Next Steps

The next stage is to establish a more rigorous experimental setup:

1. Split the corpus by complete poems into training and test sets.
2. Ensure that the model learns transition counts from the training set only.
3. Implement add-one (Laplace) smoothing to handle unseen transitions.
4. Evaluate predictions on held-out poems using cross-entropy and perplexity.
5. Compare the statistical baseline with a neural language model implemented in PyTorch.

This progression will make it possible to understand not only how a language model generates text, but also how different model architectures learn and how their performance can be evaluated objectively.