
BOOKS_SCHEMA = {
    "book_id": "SERIAL PRIMARY KEY",
    "composite_id": "TEXT UNIQUE",
    "title": "TEXT NOT NULL",
    "subtitle": "TEXT",
    "publisher": "TEXT",
    "place_of_publication": "TEXT",
    "publication_year": "INTEGER",
    "edition": "TEXT",
    "pages": "INTEGER",
    "isbn": "TEXT",
    "format_original": "TEXT",
    "format_expanded": "TEXT",
    "condition": "TEXT",
    "copies": "INTEGER",
    "illustrations": "TEXT",
    "packaging": "TEXT",
    "topic_id": "INTEGER REFERENCES topics(topic_id)",
    "is_translation": "BOOLEAN DEFAULT FALSE",
    "original_language": "TEXT",
    "is_multivolume": "BOOLEAN DEFAULT FALSE",
    "series_title": "TEXT",
    "total_volumes": "INTEGER",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

PEOPLE_SCHEMA = {
    "person_id": "SERIAL PRIMARY KEY",
    "unified_id": "TEXT UNIQUE",
    "family_name": "TEXT",
    "given_names": "TEXT",
    "name_particles": "TEXT",
    "single_name": "TEXT",
    "is_organisation": "BOOLEAN DEFAULT FALSE",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

TOPICS_SCHEMA = {
    "topic_id": "SERIAL PRIMARY KEY",
    "topic_name": "TEXT NOT NULL UNIQUE",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

PRICES_SCHEMA = {
    "price_id": "SERIAL PRIMARY KEY",
    "book_id": "INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE",
    "amount": "INTEGER",
    "imported_price": "BOOLEAN NOT NULL DEFAULT FALSE",
    "source": "TEXT",
    "date_added": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

BOOKS2VOLUMES_SCHEMA = {
    "volume_id": "SERIAL PRIMARY KEY",
    "book_id": "INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE",
    "volume_number": "INTEGER",
    "volume_title": "TEXT",
    "pages": "INTEGER",
    "notes": "TEXT"
}

BOOKS2PEOPLE_SCHEMA = {
    "b2p_id": "SERIAL PRIMARY KEY",
    "book_id": "INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE",
    "composite_id": "TEXT NOT NULL",
    "person_id": "INTEGER NOT NULL REFERENCES people(person_id) ON DELETE CASCADE",
    "unified_id": "TEXT NOT NULL",
    "display_name": "TEXT",
    "family_name": "TEXT",
    "given_names": "TEXT",
    "name_particles": "TEXT",
    "single_name": "TEXT",
    "sort_order": "INTEGER",
    "is_author": "BOOLEAN DEFAULT FALSE",
    "is_editor": "BOOLEAN DEFAULT FALSE",
    "is_contributor": "BOOLEAN DEFAULT FALSE",
    "is_translator": "BOOLEAN DEFAULT FALSE",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

BOOK_ADMIN_SCHEMA = {
    "book_id": "INTEGER PRIMARY KEY REFERENCES books(book_id) ON DELETE CASCADE",
    "composite_id": "TEXT REFERENCES books(composite_id) ON DELETE CASCADE",
    "original_entry": "TEXT NOT NULL",
    "parsing_confidence": "TEXT",
    "needs_review": "BOOLEAN DEFAULT FALSE",
    "verification_notes": "TEXT",
    "topic_changed": "BOOLEAN DEFAULT FALSE",
    "price_changed": "BOOLEAN DEFAULT FALSE",
    "batch_id": "TEXT",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

USERS_SCHEMA = {
    "user_id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
    "username": "TEXT NOT NULL UNIQUE",
    "email": "TEXT NOT NULL UNIQUE",
    "password_hash": "TEXT NOT NULL",
    "role": "TEXT NOT NULL DEFAULT 'viewer'",
    "is_active": "BOOLEAN DEFAULT TRUE",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

SESSIONS_SCHEMA = {
    "session_id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
    "user_id": "UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE",
    "session_token": "TEXT NOT NULL UNIQUE",
    "expires_at": "TIMESTAMP NOT NULL",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}
