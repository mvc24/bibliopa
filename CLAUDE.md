# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bibliopa is a production-scale Python bibliography digitization project that uses the Anthropic API to parse and extract structured data from unstructured German bibliography entries. The project processes approximately 20,000 book entries from 50 Word documents, converting them into structured JSON format for database storage and future web interface development.

**Current Status**: Successfully processed 1,086 entries through complete production pipeline (16 files from xs & s groups), with batch processing system active for remaining ~19,000 entries.

## Architecture

This is a production data engineering project with a complete ETL pipeline:

- **Extract**: Multi-source data consolidation from 50 Word documents with intelligent conflict resolution
- **Transform**: Batch-processed Claude API integration with quality assurance and error handling
- **Load**: Structured JSON output with comprehensive logging and data lineage tracking

### Current Production Pipeline:
1. **Data Consolidation**: `scripts/data_prep.py` - Merges price and no-price versions of files
2. **Auto-Discovery**: `api/batch_processor.py` - Automatically discovers processed topics from batch files
3. **Batch Submission**: `api/batch_processor.py` - Submits 25-entry batches with configurable rate limiting
4. **Status Monitoring**: `api/check_status.py` - Independent batch status checking and result retrieval
5. **API Integration**: `api/parse_single_batch.py` - Core Claude API functions
6. **Quality Assurance**: Built-in confidence scoring and review flagging

## Core Files

### Production Scripts
- `main.py`: Initial prototype script (historical)
- `scripts/data_prep.py`: Multi-source data consolidation with intelligent matching
- `api/batch_processor.py`: Auto-discovery and batch submission with configurable limits and command-line options
- `api/parse_single_batch.py`: Core Claude API functions for batch submission only
- `api/check_status.py`: Independent batch status monitoring, result retrieval, and progress tracking

### Data Organization
- `data/original/`: Source Word documents (preise & keine preise versions)
- `data/consolidated/`: Merged data files ready for batching
- `data/batched/`: 25-entry batches organized by topic for API processing
- `data/parsed/`: Structured JSON results from Claude API
- `data/logs/`: Processing logs and batch tracking metadata
- `utils/`: Project documentation and development notes

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Production Pipeline
```bash
# Run data consolidation for specific file groups
python main.py  # Processes xs group files

# Auto-discover and submit batches to Claude API (default: 15 batches max)
python api/batch_processor.py

# List available topics with batch files (no submission)
python api/batch_processor.py --list-topics

# Submit with custom limits
python api/batch_processor.py --max-submit 20  # Submit up to 20 batches
python api/batch_processor.py --max-submit 3   # For testing with fewer batches

# Check status of all submitted batches
python api/check_status.py

# Check status of specific batch
python api/check_status.py --batch-id msgbatch_01ABC123
```

### Dependencies
Production dependencies:
- `anthropic`: Claude API for structured data extraction
- `python-dotenv`: Environment variable management
- `python-docx`: Word document processing (added for production pipeline)

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
Comprehensive structured JSON schema with:
- **Person Objects**: `family_name`, `given_names`, `display_name` with support for `name_particles`
- **Core Bibliographic**: `title`, `subtitle`, `publisher`, `place_of_publication`, `publication_year`
- **Physical Description**: `pages`, `format_original`, `format_expanded`, `condition`, `copies`
- **Advanced Fields**: `is_multivolume`, `series_title`, `volumes[]`, `is_translation`, `translator`
- **People**: Separate arrays for `authors`, `editors`, `contributors`
- **Administrative**: `parsing_confidence`, `needs_review`, `original_entry`, `verification_notes`
- **Enhanced Metadata**: `isbn`, `illustrations`, `packaging`, `edition`

## Data Engineering Considerations

### Production Parsing Strategy
Enterprise-grade Claude API integration with:
- **Model**: `claude-sonnet-4-20250514` optimized for bibliographic parsing
- **Batch Processing**: 25-entry batches with rate limiting and cost optimization
- **Temperature**: 0 for consistent, reproducible parsing
- **Max tokens**: 8000 per entry with comprehensive prompting
- **Quality Control**: Confidence scoring (high/medium/low) with automated review flagging
- **Error Handling**: Robust retry logic and graceful degradation

### Multi-Source Data Integration
**Challenge Solved**: Intelligent consolidation of two bibliography versions (with/without prices)
- **Data Sovereignty**: 'keine preise' version as authoritative source for content
- **Price Recovery**: Smart matching to preserve pricing data from older 'preise' version
- **Conflict Resolution**: 89% average match rate with comprehensive discrepancy tracking
- **Quality Metrics**: Detailed logging of matches, discrepancies, and processing statistics

### Production Data Management
- **Batch Tracking**: Complete lineage from source file through parsed output
- **Timestamped Results**: `batch_{topic}_{YYYYMMDD-HHMM}.json` format
- **Progress Persistence**: JSON-based batch status tracking with recovery capability
- **Data Integrity**: Original entries preserved with encoding issue correction
- **Comprehensive Logging**: Processing metrics, match rates, and quality indicators

## Current Status & Roadmap

### ✅ COMPLETED PHASES:
1. **Data Analysis & Schema Design**: Comprehensive JSON schema for German bibliographic data
2. **Multi-Source Consolidation**: Intelligent merging of 50 Word documents with conflict resolution
3. **Production Pipeline**: Batch processing system with quality assurance and error handling
4. **Initial Processing**: 1,086 entries successfully processed through complete pipeline

### 🔄 CURRENT FOCUS:
- **Batch Processing Completion**: Processing remaining ~19,000 entries (m, l, xl file groups)
- **Quality Assurance**: Monitoring confidence scores and reviewing flagged entries
- **API Cost Optimization**: Managing batch processing costs and rate limits

### 🗃️ NEAR-TERM ROADMAP:
1. **Database Implementation**: PostgreSQL schema design and data loading
2. **Web Interface Development**: Search system and editing interface for grandfather
3. **Production Deployment**: Final system for 89-year-old end user

## Technical Achievement Summary

This project demonstrates enterprise-level data engineering capabilities:
- **Scalable ETL Pipeline**: Processing 20,000+ bibliographic records
- **AI Integration**: Production Claude API implementation with batch processing
- **Data Quality Engineering**: Automated validation, confidence scoring, and review workflows
- **Multi-Source Integration**: Intelligent conflict resolution and data consolidation
- **Production Monitoring**: Comprehensive logging, metrics, and error recovery

Serves as both a meaningful family legacy preservation project and a professional portfolio demonstration of modern data engineering practices.
- to memorize