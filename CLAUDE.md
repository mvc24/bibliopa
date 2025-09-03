# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bibliopa is a Python-based bibliography digitization project that uses the Anthropic API to parse and extract structured data from unstructured German bibliography entries. The project processes approximately 20,000 book entries from Word documents, converting them into structured JSON format for database storage and future web interface development.

## Architecture

This is a data engineering project focused on ETL (Extract, Transform, Load) operations:

- **Extract**: Python scripts read raw bibliography text from `data/sample_entries.txt`
- **Transform**: Claude API processes unstructured entries using detailed prompts to extract bibliographic metadata
- **Load**: Parsed results are saved as timestamped JSON files in `data/parsed/`

## Core Files

- `main.py`: Initial prototype script for API interaction and basic parsing
- `parse.py`: Production parser with enhanced error handling, user input for labeling, and structured JSON output
- `data/sample_entries.txt`: Source bibliography entries in German
- `data/parsed/`: Output directory for processed JSON results
- `utils/`: Contains project documentation and conversation logs

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Parser
```bash
# Run the main parser (requires user input for label)
python parse.py

# Run the basic prototype
python main.py
```

### Dependencies
Core dependencies are minimal:
- `anthropic`: For API access to Claude models
- `python-dotenv`: For environment variable management

## Environment Configuration

The project requires an Anthropic API key stored in `.env`:
```
ANTHROPIC_API_KEY=your_key_here
```

## Data Structure

### Input Format
German bibliography entries with complex formatting including:
- Author names (single/multiple/edited works)
- Titles and subtitles
- Publication details (city, publisher, year)
- Physical descriptions (pages, condition, format)
- Multi-volume works
- Price information
- Special notations in German abbreviations

### Output Format
Structured JSON with fields:
- `authors`: Array of objects with `first_name` and `last_name`
- `title`: Exact title as written
- `publisher`: Publisher name
- `location`: Publication location
- `year`: Publication year
- `price`: Price if listed
- `pages`: Number of pages
- `condition`: German condition description
- `notes`: Additional details in German
- `is_multivolume`: Boolean
- `is_edited`: Boolean
- `volumes`: Array for multi-volume works
- `editors`/`contributors`: For edited works

## Data Engineering Considerations

### Parsing Strategy
The project uses Claude's language understanding to handle complex bibliographic formats that would be difficult with regex or traditional parsing. The API is configured with:
- Model: `claude-sonnet-4-20250514`
- Temperature: 0 (for consistent parsing)
- Max tokens: 20000 (for large entries)

### Duplicate Detection
The system needs to handle duplicate entries as the original bibliography is continuously updated and alphabetically sorted.

### File Management
- Parsed outputs include full API response metadata for debugging
- Timestamped filenames prevent overwrites: `{label}-{YYYYMMDD-HHMM}.json`
- Original entries preserved exactly as written in German

## Future Development

The project is designed for two phases:
1. **Current**: Data extraction and cleaning using AI
2. **Planned**: Web-based interface for editing entries and adding keywords

This serves as both a practical tool for digitizing a private library collection and a portfolio project demonstrating data engineering skills with AI integration.