import { query, sql } from '@/lib/db';
import { Book, BookDetail, BookDisplayRow } from '@/types/database';

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
  topicNormalised?: string,
) {
  const offset = (page - 1) * limit;
  let whereClause = 'WHERE b.is_removed = FALSE';
  const params: (number | string | boolean | null)[] = [limit, offset];

  if (topicNormalised && topicNormalised !== 'all') {
    whereClause += ' AND t.topic_normalised = $3';
    params.push(topicNormalised);
  }

  const result = await query<BookDetail>(
    sql`
    SELECT
      b.book_id,
      b.title,
      b.subtitle,
      b.publication_year,
      b.publisher,
      b.place_of_publication,
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
      ) AS people,

      JSONB_AGG(
        DISTINCT JSONB_BUILD_OBJECT(
            'price_id', pr.price_id,
            'amount', pr.amount,
            'source', pr.source,
            'imported_price', pr.imported_price,
            'date_added', pr.date_added
          )
        ) FILTER (WHERE pr.price_id IS NOT NULL) AS prices

    FROM books b
    LEFT JOIN book_admin ba ON b.book_id = ba.book_id
    LEFT JOIN topics t ON b.topic_id = t.topic_id
    LEFT JOIN books2people b2p ON b.book_id = b2p.book_id
    LEFT JOIN people p ON b2p.person_id = p.person_id
    LEFT JOIN prices pr ON b.book_id = pr.book_id
    ${whereClause}
    GROUP BY b.book_id, b.title, b.subtitle, b.publication_year, b.publisher, b.place_of_publication, t.topic_name
    ORDER BY
      CASE
        WHEN EXISTS (
          SELECT 1 FROM books2people b2p_check
          WHERE b2p_check.book_id = b.book_id AND b2p_check.is_author = TRUE
        )
        THEN (
          SELECT p_author.family_name
          FROM books2people b2p_author
          JOIN people p_author ON b2p_author.person_id = p_author.person_id
          WHERE b2p_author.book_id = b.book_id AND b2p_author.is_author = TRUE
          ORDER BY b2p_author.sort_order
          LIMIT 1
        )
        ELSE (
          SELECT p_editor.family_name
          FROM books2people b2p_editor
          JOIN people p_editor ON b2p_editor.person_id = p_editor.person_id
          WHERE b2p_editor.book_id = b.book_id AND b2p_editor.is_editor = TRUE
          ORDER BY b2p_editor.sort_order
          LIMIT 1
        )
      END
    LIMIT $1 OFFSET $2
    `,
    params,
  );
  return result.rows;
}

export async function getSingleBookPageById(id: number) {
  const result = await query<BookDetail>(
    sql`
      SELECT
        b.*,

        JSONB_BUILD_OBJECT(
          'original_entry', ba.original_entry,
          'parsing_confidence', ba.parsing_confidence,
          'needs_review', ba.needs_review,
          'verification_notes', ba.verification_notes,
          'topic_changed', ba.topic_changed,
          'price_changed', ba.price_changed,
          'batch_id', ba.batch_id,
          'created_at', ba.created_at
        ) AS admin_data,

        JSONB_BUILD_OBJECT(
          'topic_id', t.topic_id,
          'topic_name', t.topic_name
        ) AS topic,

        JSONB_AGG(
          DISTINCT JSONB_BUILD_OBJECT(
            'person_id', p.person_id,
            'unified_id', p.unified_id,
            'family_name', p.family_name,
            'given_names', p.given_names,
            'name_particles', p.name_particles,
            'single_name', p.single_name,
            'is_organisation', p.is_organisation,
            'display_name', b2p.display_name,
            'is_author', b2p.is_author,
            'is_editor', b2p.is_editor,
            'is_contributor', b2p.is_contributor,
            'is_translator', b2p.is_translator,
            'sort_order', b2p.sort_order
          )
        ) FILTER (WHERE p.person_id IS NOT NULL) AS people,

        JSONB_AGG(
          DISTINCT JSONB_BUILD_OBJECT(
            'volume_id', b2v.volume_id,
            'volume_number', b2v.volume_number,
            'volume_title', b2v.volume_title,
            'pages', b2v.pages,
            'notes', b2v.notes
          )
        ) FILTER (WHERE b2v.volume_id IS NOT NULL) AS volumes,

        JSONB_AGG(
          DISTINCT JSONB_BUILD_OBJECT(
            'price_id', pr.price_id,
            'amount', pr.amount,
            'source', pr.source,
            'imported_price', pr.imported_price,
            'date_added', pr.date_added
          )
        ) FILTER (WHERE pr.price_id IS NOT NULL) AS prices

      FROM books b
      LEFT JOIN book_admin ba ON b.book_id = ba.book_id
      LEFT JOIN topics t ON b.topic_id = t.topic_id
      LEFT JOIN books2people b2p ON b.book_id = b2p.book_id
      LEFT JOIN people p ON b2p.person_id = p.person_id
      LEFT JOIN books2volumes b2v ON b.book_id = b2v.book_id
      LEFT JOIN prices pr ON b.book_id = pr.book_id
      WHERE b.book_id = $1
      GROUP BY b.book_id, t.topic_id, ba.book_id
    `,
    [id],
  );
  return result.rows[0];
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
