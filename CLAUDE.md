# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bibliopa is a production-scale Python bibliography digitization project that uses the Anthropic API to parse and extract structured data from unstructured German bibliography entries. The project processes approximately 20,000 book entries from 50 Word documents, converting them into structured JSON format for PostgreSQL database storage and modern web interface access.

**Current Status**: Successfully processed 525 batch files (~13,000+ entries) through Claude API parsing pipeline. Database infrastructure implemented with PostgreSQL, Alembic migrations, and comprehensive data loading system. Next.js frontend with modern React stack (Refine, Mantine, TailwindCSS) actively under development.

## Architecture

This is a production data engineering project with a complete ETL pipeline and modern web stack:

- **Extract**: Multi-source data consolidation from 50 Word documents with intelligent conflict resolution
- **Transform**: Batch-processed Claude API integration with quality assurance and error handling
- **Load**: PostgreSQL database with structured schema and comprehensive data loading infrastructure
- **Serve**: Modern Next.js web application with React-based admin interface

### Complete Production Pipeline:
1. **Data Consolidation**: `scripts/data_prep.py` - Merges price and no-price versions of files
2. **Auto-Discovery**: `api/batch_processor.py` - Automatically discovers processed topics from batch files
3. **Batch Submission**: `api/batch_processor.py` - Submits 25-entry batches with configurable rate limiting
4. **Status Monitoring**: `api/check_status.py` - Independent batch status checking and result retrieval
5. **API Integration**: `api/parse_single_batch.py` - Core Claude API functions
6. **Quality Assurance**: Built-in confidence scoring and review flagging
7. **Database Loading**: `database/db_orchestrator.py` - Orchestrates data preparation and PostgreSQL loading
8. **Schema Management**: Alembic migrations for database version control
9. **Web Interface**: Next.js frontend with Refine admin framework and Mantine components

## Core Files

### Production Scripts
- `main.py`: Data consolidation orchestrator (processes file groups: xl, l, m, xs, s)
- `scripts/data_prep.py`: Multi-source data consolidation with intelligent matching
- `api/batch_processor.py`: Auto-discovery and batch submission with configurable limits and command-line options
- `api/parse_single_batch.py`: Core Claude API functions for batch submission only
- `api/check_status.py`: Independent batch status monitoring, result retrieval, and progress tracking

### Database Infrastructure
- `database/connection.py`: PostgreSQL connection management
- `database/db_orchestrator.py`: Data loading orchestration with hybrid logging system and critical error handling
- `database/load_entries.py`: Entry preparation and database insertion with enhanced error propagation
- `database/load_topics.py`: Topic management and loading
- `database/tables/`: SQLAlchemy table definitions (books.py, topics.py)
- `alembic/`: Database migration management and version control
- `alembic.ini`: Alembic configuration

### Frontend Application
- `frontend/`: Next.js web application
- `frontend/package.json`: Modern React stack (Next.js 15, React 19, Refine, Mantine, TailwindCSS)
- `frontend/src/`: Application source code with components and pages

### Data Organization
- `data/original/`: Source Word documents (preise & keine preise versions)
- `data/consolidated/`: Merged data files ready for batching
- `data/batched/`: 25-entry batches organized by topic for API processing
- `data/parsed/`: 525+ structured JSON results from Claude API (13,000+ entries)
- `data/logs/`: Processing logs, batch tracking metadata, and database loading status
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

#### Data Processing
```bash
# Run data consolidation for specific file groups
python main.py  # Currently processes xl group files

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

#### Database Operations
```bash
# Run database migrations
alembic upgrade head

# Load data to PostgreSQL database
python database/db_orchestrator.py

# Load specific number of batches
python database/db_orchestrator.py --limit 10
```

#### Frontend Development
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Dependencies

#### Core Python Dependencies
- `anthropic`: Claude API for structured data extraction
- `python-dotenv`: Environment variable management
- `python-docx`: Word document processing
- `psycopg2`: PostgreSQL database adapter
- `sqlalchemy`: Database ORM and schema management
- `alembic`: Database migration management

#### Frontend Dependencies
- `next`: Next.js 15 React framework
- `react`: React 19 core library
- `@refinedev/core`: Admin panel framework
- `@mantine/core`: React components library
- `tailwindcss`: Utility-first CSS framework
- `typescript`: Type-safe JavaScript development

## Environment Configuration

The project requires environment variables stored in `.env`:
```
ANTHROPIC_API_KEY=your_key_here
DATABASE_URL=postgresql://username:password@localhost/bibliopa
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

### Critical Error Handling Architecture
**Enhanced Database Loading Pipeline** with robust error management:
- **Hybrid Log Structure**: `{"entries": [], "completed": [], "failed": []}` format for efficient filtering and detailed tracking
- **Critical Error Propagation**: Comprehensive error flag system from `load_entries.py` through `db_orchestrator.py`
- **Graceful Degradation**: Continue processing remaining files when critical errors occur, maximizing data recovery
- **File Quarantine System**: Failed files automatically excluded from future processing via set-based filtering
- **Granular State Tracking**: Mutually exclusive states (`critical_error` vs `processing_done/loading_done`) prevent edge cases
- **Dual-Write Strategy**: Log persistence after prep and after load for complete audit trail
- **Manual Recovery Support**: Infrastructure for targeted reprocessing of quarantined files

## Current Status & Roadmap

### ✅ COMPLETED PHASES:
1. **Data Analysis & Schema Design**: Comprehensive JSON schema for German bibliographic data
2. **Multi-Source Consolidation**: Intelligent merging of 50 Word documents with conflict resolution
3. **Production Pipeline**: Batch processing system with quality assurance and error handling
4. **Large-Scale Processing**: 525+ batch files processed (~13,000+ entries through Claude API)
5. **Database Infrastructure**: PostgreSQL schema, Alembic migrations, and comprehensive data loading system
6. **Frontend Foundation**: Next.js application with modern React stack and admin framework
7. **Critical Error Handling**: Hybrid logging system with file quarantine and graceful degradation

### 🔄 CURRENT FOCUS:
- **Database Population**: Loading 13,000+ parsed entries from JSON files to PostgreSQL
- **Frontend Development**: Building search interface, data editing capabilities, and user experience
- **Data Quality Review**: Processing flagged entries and confidence score validation
- **Remaining Batch Processing**: Processing any remaining file groups if needed

### 🗃️ NEAR-TERM ROADMAP:
1. **Complete Data Loading**: Populate PostgreSQL database with all parsed entries
2. **Frontend Feature Development**: Search system, filtering, editing interface, and user management
3. **Production Deployment**: Database and web application deployment for grandfather access
4. **User Training & Documentation**: End-user guide and system handoff

## Technical Achievement Summary

This project demonstrates enterprise-level full-stack data engineering capabilities:
- **Scalable ETL Pipeline**: Processing 20,000+ bibliographic records through complete automation
- **AI Integration**: Production Claude API implementation with sophisticated batch processing
- **Database Engineering**: PostgreSQL schema design, Alembic migrations, and complex data loading
- **Modern Web Stack**: Next.js 15, React 19, TypeScript, and professional admin framework
- **Data Quality Engineering**: Automated validation, confidence scoring, and comprehensive review workflows
- **Multi-Source Integration**: Intelligent conflict resolution and data consolidation
- **Production Monitoring**: Comprehensive logging, metrics, error recovery, and data lineage

Serves as both a meaningful family legacy preservation project and a professional portfolio demonstration of modern full-stack data engineering and web development practices.

## Development Approach & Learning Philosophy

### Claude Code Interaction Guidelines
When working with this codebase, prioritize **guided learning** over direct implementation:

#### 🎯 Learning-Focused Development
- **Guide, Don't Code**: Help users understand architectural decisions and error patterns rather than immediately providing solutions
- **Step-by-Step Approach**: Break complex problems into manageable learning opportunities
- **Error Understanding**: When bugs occur, explain the underlying causes and help users trace through the logic
- **Architectural Insight**: Share insights about why certain patterns (like hybrid logging, graceful degradation) improve system robustness

#### 🔍 Problem-Solving Strategy
1. **Analyze Together**: Help users identify what's broken and why
2. **Explain Concepts**: Cover relevant programming concepts (JSON handling, exception patterns, data flow)
3. **Guide Implementation**: Let users write code while providing architectural guidance
4. **Review and Refine**: Help users understand the implications of their implementation choices

#### ⚠️ When to Intervene Directly
Only write code directly when:
- User explicitly requests implementation
- Time-sensitive production issues require immediate fixes
- Complex boilerplate that doesn't offer learning value

This approach builds deeper understanding and creates more confident, self-sufficient developers while ensuring the codebase evolves thoughtfully.