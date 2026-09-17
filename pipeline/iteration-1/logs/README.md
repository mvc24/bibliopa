# iteration 1 logs

| file | stage | what it holds |
|---|---|---|
| `processing_log.json` | 01 | per-file row counts and price matches, all 46 topics (48 rows: `erstausgaben` is three files). Totals: 12,573 kp entries, 12,700 p entries, 11,544 matched, 1,156 discrepancies |
| `discrepancies.json` | 01 | 1,179 p rows that stage 01 could not match to a kp row. The log counts 1,156: the file is opened and extended, never reset, so a partial re-run appends its rows a second time |
| `discrepancies_processed.json` | 02 | the same rows searched against every topic: 935 resolved (exact or ≥ 95), 52 between 75 and 95, 192 below 75. Diagnostic only — nothing reads it back into `data/consolidated/` |
| `pass1_preparation.log`, `pass2_preparation.log` | 05 | batch counts for the two people passes |
| `validation_log.json` | 06 | per-file validation counts, 48 files |
| `data_loading_log.json` | 07 | orchestrator-era log, 93 per-file entries from 2025-09-24: entries loaded, people logged, corrupt entries |

Home-directory paths were replaced with `~`. Nothing else was edited.
