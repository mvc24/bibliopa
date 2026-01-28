import { query, sql } from '@/lib/db';
import { Book, BookWithRelations, BookDisplayRow } from '@/types/database';

/**
 * Get all books with basic information
 * Practice: Start with SELECT * FROM books
 */
export async function getAllBooks() {
  const result = await query<Book>(`SELECT * FROM books`, []);

  return result.rows;
}

export async function getTotalBookCount() {
  const result = await query<{ count: number }>(
    `SELECT COUNT(*) FROM books`,
    [],
  );

  return result.rows[0].count;
}

export async function getAllBooksForTablePaginated(
  page: number,
  limit: number,
) {
  const offset = (page - 1) * limit;
  const result = await query<BookDisplayRow>(
    sql`
    SELECT
      b.book_id,
      b.title,
      b.subtitle,
      b.publication_year,
      t.topic_name,
      JSONB_AGG(
        JSONB_BUILD_OBJECT(
          'family_name', p.family_name,
          'given_names', p.given_names,
          'name_particles', p.name_particles,
          'single_name', p.single_name,
          'display_name', b2p.display_name,
          'is_author', b2p.is_author,
          'is_editor', b2p.is_editor
        )
      ) AS people
    FROM books b
    LEFT JOIN book_admin ba ON b.book_id = ba.book_id
    LEFT JOIN topics t ON b.topic_id = t.topic_id
    LEFT JOIN books2people b2p ON b.book_id = b2p.book_id
    LEFT JOIN people p ON b2p.person_id = p.person_id
    GROUP BY b.book_id, b.title, b.subtitle, b.publication_year, t.topic_name
    LIMIT $1 OFFSET $2
    `,
    [limit, offset],
  );
  return result.rows;
}

export async function getAllBooksWithEverything() {
  const result = await query<BookDisplayRow>(
    sql`
     SELECT
      b.*,
      ba.*,
      b2p.*,
      p.*,
      t.*,
      b2v.*,
      pr.*
    FROM books b
    LEFT JOIN book_admin ba ON b.book_id = ba.book_id
    LEFT JOIN topics t ON b.topic_id = t.topic_id
    LEFT JOIN books2people b2p ON b.book_id = b2p.book_id
    LEFT JOIN people p ON b2p.person_id = p.person_id
    LEFT JOIN books2volumes b2v ON b.book_id = b2v.book_id
    LEFT JOIN prices pr ON b.book_id = pr.book_id
    ORDER BY b.title
    `,
    [],
  );
  return result.rows;
}

export async function getBookWithEverythingById(id: number) {
  const result = await query<BookDisplayRow>(
    sql`
    SELECT
      b.*,
      ba.*,
      b2p.*,
      p.*,
      t.*,
      b2v.*,
      pr.*
    FROM books b
    LEFT JOIN book_admin ba ON b.book_id = ba.book_id
    LEFT JOIN topics t ON b.topic_id = t.topic_id
    LEFT JOIN books2people b2p ON b.book_id = b2p.book_id
    LEFT JOIN people p ON b2p.person_id = p.person_id
    LEFT JOIN books2volumes b2v ON b.book_id = b2v.book_id
    LEFT JOIN prices pr ON b.book_id = pr.book_id
    WHERE b.book_id = $1
    `,
    [id],
  );
  return result.rows;
}

// TODO(human): Add more query functions as you practice:
// - getBooksWithPagination(page, limit)
// - getBooksWithFilters(search, topicId, etc.)
// - getBookById(bookId)
// - getBookWithAllRelations(bookId) - joins with people, topics, prices
// - searchBooksByTitle(searchTerm)
// - createBook(bookData)
// - updateBook(bookId, updates)
// - deleteBook(bookId)
