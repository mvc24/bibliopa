# shared helpers

- `text_matching.py`: `normalise_text` (NFC, lowercase, collapse whitespace), `remove_diacritics`, and `test_similarity` (RapidFuzz `ratio`). Imported by iteration-1 stages 02, 04, 05, 07 and iteration-2 stages 04, 05. The live copy is `scripts/text_matching.py`.
- `progress.py`: a one-line terminal progress bar used by the slow fuzzy scans.
