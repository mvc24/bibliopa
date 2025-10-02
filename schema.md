# Schema

## Tables

### Primary
- books
- people (normalised person entities)
- topics
- prices

### Relationships
- books2people
- books2volumes 
- books2prices

### Admin
book_admin
users
sessions

## SQL

CREATE TABLE books (
    book_id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    subtitle TEXT,
    publisher TEXT,
    place_of_publication TEXT,
    publication_year INTEGER,
    edition TEXT,
    pages INTEGER,
    isbn TEXT,
    format_original TEXT,
    format_expanded TEXT,
    condition TEXT,
    copies INTEGER,
    illustrations TEXT,
    packaging TEXT,
    topic_id UUID REFERENCES topics(topic_id),
    is_translation BOOLEAN DEFAULT FALSE,
    original_language TEXT,
    is_multivolume BOOLEAN DEFAULT FALSE,
    series_title TEXT,
    total_volumes INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


people

CREATE TABLE people (
    person_id UUID PRIMARY KEY,
    family_name TEXT,
    given_names TEXT,
    display_name TEXT NOT NULL,
    name_particles TEXT,
    single_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


topics

CREATE TABLE topics (
    topic_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


price

CREATE TABLE prices (
    price_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    is_original BOOLEAN NOT NULL DEFAULT FALSE,
    source TEXT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE books2volumes (
    volume_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    volume_number INTEGER NOT NULL,
    volume_title TEXT,
    pages INTEGER,
    notes TEXT,
    UNIQUE (book_id, volume_number)
);

CREATE TABLE books2people (
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    person_id UUID NOT NULL REFERENCES people(person_id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('author', 'editor', 'contributor', 'translator')),
    sort_order INTEGER,
    PRIMARY KEY (book_id, person_id, role)
);


CREATE TABLE book_admin (
    book_id UUID PRIMARY KEY REFERENCES books(book_id) ON DELETE CASCADE,
    source_filename TEXT NOT NULL,
    original_entry TEXT NOT NULL,
    parsing_confidence TEXT CHECK (parsing_confidence IN ('high', 'medium', 'low')),
    needs_review BOOLEAN DEFAULT FALSE,
    verification_notes TEXT,
    batch_id TEXT,
    composite_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'viewer',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    session_token TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



TRUNCATE TABLE books CASCADE;
TRUNCATE TABLE prices CASCADE;
TRUNCATE TABLE book_admin CASCADE;
TRUNCATE TABLE books2volumes CASCADE;


TRUNCATE TABLE  CASCADE;
TRUNCATE TABLE  CASCADE;

[
    {
        "submitted": {
            "data/batched/symbolkunde/symbolkunde_1-2.json": {
                "batch_id": "msgbatch_019beNjKvjn6q31m7x7r3nzR",
                "topic": "symbolkunde",
                "submitted_at": "20250911-2241",
                "entry_count": 25
            },
            "data/batched/symbolkunde/symbolkunde_2-2.json": {
                "batch_id": "msgbatch_01Y3pEMStCQmdZUdAizds63Q",
                "topic": "symbolkunde",
                "submitted_at": "20250911-2241",
                "entry_count": 6
            },
            ...
        },
        "completed": [],
        "failed": []
    }
]
