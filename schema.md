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

### Current tables

table books

        Column        |            Type             | Collation | Nullable |      Default      
----------------------+-----------------------------+-----------+----------+-------------------
 book_id              | uuid                        |           | not null | 
 title                | text                        |           | not null | 
 subtitle             | text                        |           |          | 
 publisher            | text                        |           |          | 
 place_of_publication | text                        |           |          | 
 publication_year     | integer                     |           |          | 
 edition              | text                        |           |          | 
 pages                | integer                     |           |          | 
 isbn                 | text                        |           |          | 
 format_original      | text                        |           |          | 
 format_expanded      | text                        |           |          | 
 condition            | text                        |           |          | 
 copies               | integer                     |           |          | 
 illustrations        | text                        |           |          | 
 packaging            | text                        |           |          | 
 is_translation       | boolean                     |           |          | false
 original_language    | text                        |           |          | 
 is_multivolume       | boolean                     |           |          | false
 series_title         | text                        |           |          | 
 total_volumes        | integer                     |           |          | 
 created_at           | timestamp without time zone |           |          | CURRENT_TIMESTAMP
 updated_at           | timestamp without time zone |           |          | CURRENT_TIMESTAMP
 topic_id             | uuid                        |           |          | 

Indexes:
    "books_pkey" PRIMARY KEY, btree (book_id)
Foreign-key constraints:
    "books_topic_id_fkey" FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
Referenced by:
    TABLE "book_admin" CONSTRAINT "book_admin_book_id_fkey" FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
    TABLE "books2people" CONSTRAINT "books2people_book_id_fkey" FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
    TABLE "books2volumes" CONSTRAINT "books2volumes_book_id_fkey" FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
    TABLE "prices" CONSTRAINT "prices_book_id_fkey" FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE


                                  Table "public.book_admin"
       Column       |            Type             | Collation | Nullable |      Default      
--------------------+-----------------------------+-----------+----------+-------------------
 book_id            | uuid                        |           | not null | 
 source_filename    | text                        |           | not null | 
 original_entry     | text                        |           | not null | 
 parsing_confidence | text                        |           |          | 
 needs_review       | boolean                     |           |          | false
 verification_notes | text                        |           |          | 
 composite_id       | text                        |           |          | 
 created_at         | timestamp without time zone |           |          | CURRENT_TIMESTAMP
Indexes:
    "book_admin_pkey" PRIMARY KEY, btree (book_id)
Check constraints:
    "book_admin_parsing_confidence_check" CHECK (parsing_confidence = ANY (ARRAY['high'::text, 'medium'::text, 'low'::text]))
Foreign-key constraints:
    "book_admin_book_id_fkey" FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE

                Table "public.books2people"
     Column     |  Type   | Collation | Nullable | Default 
----------------+---------+-----------+----------+---------
 book_id        | uuid    |           | not null | 
 person_id      | uuid    |           | not null | 
 sort_order     | integer |           |          | 
 display_name   | text    |           | not null | 
 family_name    | text    |           |          | 
 given_names    | text    |           |          | 
 name_particles | text    |           |          | 
 single_name    | text    |           |          | 
 is_author      | boolean |           |          | 
 is_editor      | boolean |           |          | 
 is_contributor | boolean |           |          | 
 is_translator  | boolean |           |          | 

 Foreign-key constraints:
    "books2people_book_id_fkey" FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
    "books2people_person_id_fkey" FOREIGN KEY (person_id) REFERENCES people(person_id) ON DELETE CASCADE

                                  Table "public.people"
     Column      |            Type             | Collation | Nullable |      Default      
-----------------+-----------------------------+-----------+----------+-------------------
 person_id       | uuid                        |           | not null | 
 family_name     | text                        |           |          | 
 given_names     | text                        |           |          | 
 display_name    | text                        |           | not null | 
 name_particles  | text                        |           |          | 
 single_name     | text                        |           |          | 
 created_at      | timestamp without time zone |           |          | CURRENT_TIMESTAMP
 updated_at      | timestamp without time zone |           |          | CURRENT_TIMESTAMP
 is_organisation | boolean                     |           |          | false
Indexes:
    "people_pkey" PRIMARY KEY, btree (person_id)
Referenced by:
    TABLE "books2people" CONSTRAINT "books2people_person_id_fkey" FOREIGN KEY (person_id) REFERENCES people(person_id) ON DELETE CASCADE


                                  Table "public.book_admin"
       Column       |            Type             | Collation | Nullable |      Default      
--------------------+-----------------------------+-----------+----------+-------------------
 book_id            | uuid                        |           | not null | 
 source_filename    | text                        |           | not null | 
 original_entry     | text                        |           | not null | 
 parsing_confidence | text                        |           |          | 
 needs_review       | boolean                     |           |          | false
 verification_notes | text                        |           |          | 
 composite_id       | text                        |           |          | 
 created_at         | timestamp without time zone |           |          | CURRENT_TIMESTAMP
Indexes:
    "book_admin_pkey" PRIMARY KEY, btree (book_id)
Check constraints:
    "book_admin_parsing_confidence_check" CHECK (parsing_confidence = ANY (ARRAY['high'::text, 'medium'::text, 'low'::text]))
Foreign-key constraints:
    "book_admin_book_id_fkey" FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE

                                Table "public.topics"
   Column   |            Type             | Collation | Nullable |      Default      
------------+-----------------------------+-----------+----------+-------------------
 topic_id   | uuid                        |           | not null | gen_random_uuid()
 topic_name | text                        |           | not null | 
 created_at | timestamp without time zone |           |          | CURRENT_TIMESTAMP
Indexes:
    "topics_pkey" PRIMARY KEY, btree (topic_id)
    "topics_topic_name_key" UNIQUE CONSTRAINT, btree (topic_name)
Referenced by:
    TABLE "books" CONSTRAINT "books_topic_id_fkey" FOREIGN KEY (topic_id) REFERENCES topics(topic_id)

               Table "public.books2volumes"
    Column     |  Type   | Collation | Nullable | Default 
---------------+---------+-----------+----------+---------
 volume_id     | uuid    |           | not null | 
 book_id       | uuid    |           | not null | 
 volume_number | integer |           |          | 
 volume_title  | text    |           |          | 
 pages         | integer |           |          | 
 notes         | text    |           |          | 
 volume_index  | integer |           |          | 
Indexes:
    "books2volumes_pkey" PRIMARY KEY, btree (volume_id)
    "books2volumes_book_id_volume_index_key" UNIQUE CONSTRAINT, btree (book_id, volume_index)
Foreign-key constraints:
    "books2volumes_book_id_fkey" FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE


                                Table "public.prices"
   Column    |            Type             | Collation | Nullable |      Default      
-------------+-----------------------------+-----------+----------+-------------------
 price_id    | uuid                        |           | not null | 
 book_id     | uuid                        |           | not null | 
 amount      | integer                     |           |          | 
 is_original | boolean                     |           | not null | false
 date_added  | timestamp without time zone |           |          | CURRENT_TIMESTAMP
Indexes:
    "prices_pkey" PRIMARY KEY, btree (price_id)
Foreign-key constraints:
    "prices_book_id_fkey" FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE


                                Table "public.topics"
   Column   |            Type             | Collation | Nullable |      Default      
------------+-----------------------------+-----------+----------+-------------------
 topic_id   | uuid                        |           | not null | gen_random_uuid()
 topic_name | text                        |           | not null | 
 created_at | timestamp without time zone |           |          | CURRENT_TIMESTAMP
Indexes:
    "topics_pkey" PRIMARY KEY, btree (topic_id)
    "topics_topic_name_key" UNIQUE CONSTRAINT, btree (topic_name)
Referenced by:
    TABLE "books" CONSTRAINT "books_topic_id_fkey" FOREIGN KEY (topic_id) REFERENCES topics(topic_id)

## SQL NEW

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    composite_id TEXT,
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
    topic_id INTEGER REFERENCES topics(topic_id),
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
    person_id SERIAL PRIMARY KEY,
    unified_id TEXT,
    family_name TEXT,
    given_names TEXT,
    name_particles TEXT,
    single_name TEXT,
    is_organisation BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


topics

CREATE TABLE topics (
    topic_id SERIAL PRIMARY KEY,
    topic_name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


price

CREATE TABLE prices (
    price_id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    amount INTEGER,
    imported_price BOOLEAN NOT NULL DEFAULT FALSE,
    source TEXT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE books2volumes (
    volume_id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    volume_number INTEGER,
    volume_title TEXT,
    pages INTEGER,
    notes TEXT,
    UNIQUE (book_id, volume_number)
);

CREATE TABLE books2people (
    book_id INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    composite_id TEXT REFERENCES books(composite_id) ON DELETE CASCADE,
    person_id INTEGER NOT NULL REFERENCES people(person_id) ON DELETE CASCADE,
    unified_id TEXT REFERENCES people(unified_id) ON DELETE CASCADE,
    display_name TEXT,
    family_name TEXT,
    given_names TEXT,
    name_particles TEXT,
    single_name TEXT,
    sort_order INTEGER,
    is_author BOOLEAN DEFAULT FALSE,
    is_editor BOOLEAN DEFAULT FALSE,
    is_contributor BOOLEAN DEFAULT FALSE,
    is_translator BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (book_id, person_id)
);


CREATE TABLE book_admin (
    book_id INTEGER PRIMARY KEY REFERENCES books(book_id) ON DELETE CASCADE,
    composite_id TEXT REFERENCES books(composite_id) ON DELETE CASCADE,
    source_filename TEXT NOT NULL,
    original_entry TEXT NOT NULL,
    parsing_confidence TEXT,
    needs_review BOOLEAN DEFAULT FALSE,
    verification_notes TEXT,
    topic_changed BOOLEAN DEFAULT FALSE,
    price_changed BOOLEAN DEFAULT FALSE,
    batch_id TEXT,
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
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
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


## SQL, old

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
