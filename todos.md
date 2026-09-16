# probleme

## data work parked until after the portfolio (noted 2026-09-16)

The "finished" point for the project is: Splink dedupe done + the ~1000
missing entries loaded. Everything below waits for that, in this order.

- [ ] books2people: 20 books hold the same person twice (e.g. editor +
      translator as two rows instead of one row with both flags). List them
      with the query in the session notes below. Merge = keep lower b2p_id,
      OR the flags, delete the other. Only THEN add
      `UNIQUE (book_id, person_id)` via a migration.
- [ ] books2people: a few hundred books have no people rows at all because
      person matching failed (not the same set as the 1000 missing entries).
      Find them: books with no row in books2people whose parsed record has
      authors/editors.
- [ ] Splink: exact `family_name` matches carry a negative weight in the
      saved waterfall chart, so m/u estimation is off (support_notes.md).
- [ ] Missing ~1000 entries: reparsed in Aug 2026
      (`data_reload/reparse_missing/`), not yet loaded; people for them
      still to be matched ("worry about people later" below).
- [ ] `load_b2p.py`: no duplicate protection; do not run twice on the same
      JSON. Note is at the top of the file.

Steps this touches: the constraint can only come after the merge; the
missing-entries load can only come after their people are matched, or
they land in the "no people rows" pile too.

Query for the 20 pairs:
```sql
SELECT book_id, unified_id, count(*) FROM books2people
GROUP BY book_id, unified_id HAVING count(*) > 1;
```

## suche

- ku, hung ming -> namen mit 2 buchstaben können nicht gesucht werden

- anzahl exemplare bearbeiten und anzeigen
- themenbereich anzeigen bei übersicht

- abfrage nach preis
- 

## fixing missing books

- [x] get data from db
- [ ] create set of cids from books
- [ ] combine parsed files, create 


## FOUND THEM!

- [ ] set of complete cids from batched
- [ ] minus set of reference cids from parsed
- [ ] minus set of existing cids from database
- [ ] create batched data from missing in separate folder
- [ ] reparse
- [ ] worry about people later
- [ ]



---

wtf is this? 

  {
    "text": "A || || || || || || || || || || || || LBUS, Anita || Von seltenen Vögeln. Mit zahlreichen Abbildungen und zwei Farbtafeln. Frankfurt. S. Fischer 2005. 296 S. Buntes OLn. mit Klarsichtfolie und Lesebändchen. Neuwertig.",
    "source": "BIBLIOPHILE BÜCHER.docx",
    "price": 40,
    "topic": "BIBLIOPHILE BÜCHER",
    "topic_normalised": "bibliophile"
  },


https://bibliopa.vercel.app/books/briefe/9319?page=1&author=232#book-9319

BLAVATSKY!
DOSTOJEWSKY!! Nur 2 EINTRÄGE?!

            {
                "display_name": "DOSTOJEWSKI, F.M.",
                "composite_id": "insel_229_10_27",
                "sort_order": 1,
                "is_author": true,
                "is_editor": false,
                "is_contributor": false,
                "is_translator": false
            },
            {
                "display_name": "DOSTOJEWSKI, F.M.",
                "composite_id": "russland_89_4_17",
                "sort_order": 1,
                "is_author": true,
                "is_editor": false,
                "is_contributor": false,
                "is_translator": false
            },
            {
                "display_name": "DOSTOJEWSKI, F.M.",
                "composite_id": "russland_90_4_17",
                "sort_order": 1,
                "is_author": true,
                "is_editor": false,
                "is_contributor": false,
                "is_translator": false
            },
            {
                "display_name": "DOSTOJEWSKI, F.M.",
                "composite_id": "russland_92_4_17",
                "sort_order": 1,
                "is_author": true,
                "is_editor": false,
                "is_contributor": false,
                "is_translator": false
            }
