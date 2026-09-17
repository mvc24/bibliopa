# 03 — parse with the rewritten prompt

- **Input:** batch files under `data/raw/batched/<topic>/`.
- **Output:** `data/parsed/batch_<topic>_<n>-<total>.json`, each result with `custom_id`, `price` (carried over from the input, no longer sent to the model) and `parsed_entry`.
- **Decided:** the confidence score and `needs_review` of iteration 1 are gone. Instead six boolean flags: `is_reference`, `corrected_by_api`, `missing_person`, `multiple_editions`, `api_concerned`, `problematic_multi_volume`, each requiring a `verification_notes` explanation. People are returned as a single `display_name`; splitting names is left to stage 04. Model `claude-sonnet-4-6`, system prompt cached.
- **Logged:** `data/logs/batch_progress.json`; `check_status.py` trusts the filesystem over the log and prints a dashboard with stuck batches.
- **Went wrong:** per-entry API errors inside a successful batch are silently skipped on retrieval; they were found afterwards by comparing input ids with output ids. The copies of `batch_processor.py` and `check_status.py` in `api/` were later edited for the August 2026 re-parse of missing entries; these are the May 2026 versions.

## The six flags, with one real example each

Iteration 1 asked for `parsing_confidence` (high/medium/low) and
`needs_review`. Neither said *what* to check. The rewritten prompt asks
for six booleans, each with an explanation in `verification_notes`, and
the rule "when in doubt, prefer flagging over correcting: a flagged
record can be reviewed, a wrongly-corrected record is invisible".

| Flag | Entry | What the model did |
|---|---|---|
| `is_reference` | `FISCHER VON ERLACH, Johann Bernhard. Siehe SEDLMAYR, KREUL, Andreas` | stopped; only `original_entry` and the flag are filled |
| `corrected_by_api` | `ZUR GESCHICHE der Alemannen. Herausgegeben von Wolfgang Müller. …` | title corrected to GESCHICHTE, reason recorded |
| `missing_person` | `CHRISTIAN, Curt. Bernard Bolzano. Leben und Wirkung. Herausgegeben von …Mit Abb. …` | parsed the rest, flagged the empty editor |
| `multiple_editions` | `DAVIES, Martin. Die Gutenbergbibel. Amsterdam Time-Life 1996. … Dazu Taschenbuchausgabe DTV 1976` | first-described edition is the record, the DTV edition goes in notes |
| `api_concerned` | `STENDHAL, Friedrich. Von der Liebe. Leipzig Insel 1929. …` | nothing changed; note that Stendhal's given name was not Friedrich |
| `problematic_multi_volume` | `ERDBALL und seine Naturwunder. … Band. In zwei Abtheilungen. … 15. Auflage … 16. Aufl. … 5. Aufl. …` | only the volumes with clear data are recorded |

One example is in the prompt as a caution against over-correcting:
`MICHELAGNIOLO BUONAROTI` is not a misspelling of Michelangelo;
"Michelagniolo" is a historical variant. The typo is the single R in the
surname. The model's first-run correction would have been wrong.

Kept out of the prompt: the price (extracted by regex before batching,
merged back by `custom_id`), the topic (context only, taken from the
filename) and name splitting (the model returns one `display_name`
string per person; splitting is stage 04).
