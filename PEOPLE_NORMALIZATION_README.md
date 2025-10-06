# People Normalization Pipeline

This document explains how to use the Claude API-powered people normalization system to deduplicate and clean your 17,722 people entries.

## Overview

The system uses a **two-pass approach**:

1. **Pass 1 - Splitting**: Identifies and splits entries containing multiple people (e.g., "Otto Abel u. Wilhelm Wattenbach" → 2 separate records)
2. **Pass 2 - Deduplication**: Assigns `unified_id` and `variants` to all entries, linking duplicate spellings

## Quick Start

### Step 1: Prepare Pass 1 Batches (Already Done!)

```bash
python3 api/people_pass1_batches.py
```

**Results:**
- Found 64 entries needing split
- Created 3 batches in `database/in_progress/pass1_batches/`

### Step 2: Submit Pass 1 to Claude API

```bash
python3 api/people_batch_processor.py pass1
```

This submits the 3 batches for processing. Each entry with multiple people will be split into individual person records with proper `sort_order`.

### Step 3: Check Pass 1 Status

```bash
python3 api/check_people_status.py pass1
```

Run this periodically to check processing status. When `Status: ended`, results will be automatically retrieved and saved to `database/in_progress/pass1_results/`.

### Step 4: Prepare Pass 2 Batches

After Pass 1 completes, merge the split results with original entries:

```bash
python3 api/people_pass2_batches.py
```

**Expected Results:**
- Combines original entries + Pass 1 splits
- Groups by surname for efficient deduplication
- Creates ~251 batches in `database/in_progress/pass2_batches/`

### Step 5: Submit Pass 2 to Claude API

```bash
python3 api/people_batch_processor.py pass2
```

This submits all batches for deduplication. Each batch will receive `unified_id` and `variants` fields.

**Note:** 251 batches is a lot! You may want to submit in smaller chunks. The script automatically skips already-submitted batches, so you can run it multiple times.

### Step 6: Check Pass 2 Status

```bash
python3 api/check_people_status.py pass2
```

Monitor progress and retrieve results as they complete. Results saved to `database/in_progress/pass2_results/`.

## Output Structure

After both passes, each person entry will have:

```json
{
  "book_id": "uuid",
  "composite_id": "string",
  "source_filename": "string",
  "display_name": "ADORNO, Theodor W.",
  "family_name": "Adorno",
  "given_names": "Theodor W.",
  "name_particles": null,
  "single_name": null,
  "is_author": true,
  "is_editor": false,
  "is_contributor": false,
  "is_translator": false,
  "sort_order": 0,
  "is_organisation": false,
  "unified_id": "adorno_theodor_w",           // NEW: Links duplicate entries
  "variants": ["ADORNO, Th. W.", "Adorno, Theodor W."]  // NEW: Other spellings
}
```

### Key Points:

- **`unified_id`**: Same value for all spelling variations of the same person
- **`variants`**: Lists OTHER known spellings (excludes current `display_name`)
- **`unified_id="oops"`**: Entries that couldn't be processed correctly (for manual review)

## Cost Estimate

- **Pass 1**: ~$0.50 (64 entries across 3 batches)
- **Pass 2**: ~$3-8 (17,722 entries across 251 batches)
- **Total**: ~$4-9

## Processing Time

- **Pass 1**: ~5-15 minutes (3 small batches)
- **Pass 2**: ~2-4 hours (251 larger batches)

## Files Created

### Pass 1
- `database/in_progress/pass1_batches/` - Input batches for splitting
- `database/in_progress/pass1_batch_tracking.json` - Submission tracking
- `database/in_progress/pass1_results/` - Split results
- `database/in_progress/pass1_preparation.log` - Summary stats

### Pass 2
- `database/in_progress/pass2_batches/` - Input batches for deduplication
- `database/in_progress/pass2_batch_tracking.json` - Submission tracking
- `database/in_progress/pass2_results/` - Deduplicated results with unified_id
- `database/in_progress/pass2_preparation.log` - Summary stats

## What Happens Next?

After Pass 2 completes, you'll have ~251 result files in `pass2_results/`. You'll need to:

1. **Merge results**: Combine all Pass 2 result files into a single normalized dataset
2. **Handle "oops" entries**: Review entries with `unified_id="oops"`
3. **Load to database**: Use the normalized data with your existing database loading scripts

## Tips

### For Pass 2 (251 batches)

Since Pass 2 has many batches, consider:

1. **Test first**: Submit just 5-10 batches, check results, then continue
2. **Run in batches**: The script resumes from where it left off
3. **Monitor costs**: Check your Anthropic console periodically

### Troubleshooting

**If a batch fails:**
- Check `pass1_batch_tracking.json` or `pass2_batch_tracking.json` for error details
- Failed batches can be resubmitted by removing them from tracking file

**If JSON is malformed:**
- The `retrieve_results()` function handles JSON errors gracefully
- Entries with parsing errors get `unified_id="oops"` for manual review

## Example Workflow

```bash
# 1. Prepare and submit Pass 1 (already prepared)
python3 api/people_batch_processor.py pass1

# 2. Wait ~10 minutes, then check status
python3 api/check_people_status.py pass1

# 3. Once Pass 1 complete, prepare Pass 2
python3 api/people_pass2_batches.py

# 4. Submit Pass 2 (consider testing with first few batches)
python3 api/people_batch_processor.py pass2

# 5. Monitor Pass 2 progress (may take 2-4 hours)
python3 api/check_people_status.py pass2

# 6. Once complete, process the results for database loading
# (You'll implement this next step)
```

## Architecture Notes

This system mirrors your successful bibliography batch processing:
- Same API patterns and error handling
- Same tracking and resumption logic
- Reuses proven prompting strategies for structured output

`unified_id` design allows efficient database joins while preserving all name variants for search and display purposes.
