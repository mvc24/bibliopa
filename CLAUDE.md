## Output style override
Ignore the Learning output style completely.
No insight blocks. No "Learn by Doing" prompts. No educational framing unless explicitly asked.

# Bibliopa

Bibliography digitization project for my grandfather. ~20,000 German
book entries from Word documents → parsed JSON via Claude API →
PostgreSQL → Next.js web interface. Solo developer, end user is my
90-year-old grandfather.

## Current phase

ETL pipeline (parsing, cleaning, matching, loading) is largely done.
Frontend is the active focus.

## Stack

- **Frontend** (active): next, react, @refinedev/core, @mantine/core,
  tailwindcss
- **Database**: PostgreSQL with psycopg2, sqlalchemy, alembic
- **Data pipeline** (built, mostly stable): anthropic, python-docx,
  rapidfuzz, ijson

## Environment

Requires `.env` with:

    ANTHROPIC_API_KEY=...
    DATABASE_URL=postgresql://username:password@localhost/bibliopa

Activate the venv before running anything: `source .venv/bin/activate`
