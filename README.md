# Word Alchemist

**Word Alchemist** is a simple Python CLI tool designed to help you brainstorm the name of any creative project. It works by parsing JSON files into string arrays, optionally filtering that data based on properties like character length and syllable count, and generating and outputting all combinations.

This tool aims to spark creativity when it comes to naming important things.

---

## Installation

Install using pip:

```bash
pip install word-alchemist
```

---

## Usage

Let's use the following two JSON files as our example data.

**`words1.json`**

```json
["serendipity", "quixotic", "ephemeral"]
```

**`words2.json`**

```json
["ethereal", "solace", "labyrinth"]
```

Run the following command:

```bash
word-alchemist --files words1.json words2.json -o output.json
```

This generates all combinations of words from the two files and saves the output in `output.json`:

```plaintext
serendipity ethereal
serendipity solace
serendipity labyrinth
quixotic ethereal
quixotic solace
quixotic labyrinth
ephemeral ethereal
ephemeral solace
ephemeral labyrinth
```

If the `-o` or `--output` flag is not provided, the output will be logged directly to the console.

---

### Filters

Filters can be applied using the `--filters` flag to filter out words without having to create new JSON files:

- **`length`**: Filters based on the word length.
- **`syllables`**: Filters based on the syllable count of the word.

Supported operators: `==`, `!=`, `<`, `<=`, `>`, `>=`.

For example, running the following command:

```bash
word-alchemist --files words1.json words2.json --filters "syllables == 3"
```

Outputs:

```plaintext
quixotic ethereal
quixotic labyrinth
```

You can add multiple independent filters to apply them to specific JSON files. Filters are applied in the same order as JSON files. For example:

```bash
word-alchemist --files words1.json words2.json --filters "length > 4" "syllables == 3"
```

This will apply the length filter to `words1.json` and the syllable filter to `words2.json`.

Instead of providing a JSON file, you can use single words in specific slots by using the following flags:

- `--first-word` or `-fw`
- `--second-word` or `-sw`

This allows you to always fill a "slot" in the permutation without having to make a JSON file with a single word.

---

### Formatters

You can modify the output using formatters without editing the input JSON files.

- **`-c` / `--capitalize`**: Capitalizes the first letter of all words
- **`-j` / `--join`**: Removes all whitespace and combines them into a single word
- **`-a` / `--append`**: Appends a specific word to the end of all permutations

For example:

```bash
word-alchemist --files words1.json words2.json --capitalize --append "Labs"
```

Outputs:

```plaintext
Serendipity Ethereal Labs
Serendipity Solace Labs
Serendipity Labyrinth Labs
...
```

---

## Contributing

This is my first time writing any Python so I'm sure I missed some things with respect to best practices both syntactically and distributing the package, any and all PRs are welcome! I also think there's a lot more interesting filters and formatters that could be added, included filtering based on parts of speech (nouns, adjectives, verbs).

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Happy brainstorming! 🚀
