# iteration 1 logs

| file | stage | what it holds |
|---|---|---|
| `processing_log.json` | 01 | per-file row counts and price matches for the 16 smallest files; the rest was overwritten |
| `discrepancies.json` | 01 | the 79 p rows those 16 files could not match |
| `pass1_preparation.log`, `pass2_preparation.log` | 05 | batch counts for the two people passes |
| `validation_log.json` | 06 | per-file validation counts, 48 files |
| `data_loading_log.json` | 07 | orchestrator-era log, 93 per-file entries from 2025-09-24: entries loaded, people logged, corrupt entries |

Home-directory paths were replaced with `~`. Nothing else was edited.
