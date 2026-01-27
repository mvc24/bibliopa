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
