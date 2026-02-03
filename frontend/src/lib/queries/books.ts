import { query, sql } from '@/lib/db';
import {
  Book,
  BookWithTopic,
  Books2People,
  Price,
  AuthorListItem,
} from '@/types/database';

/**
 * Get all books with basic information
 * Practice: Start with SELECT * FROM books
 */
export async function getAllBooks() {
  const result = await query<Book>(`SELECT * FROM books`, []);

  return result.rows;
}

// Rebuild query functions

export async function getBooksOverviewWithTopic(
  page: number,
  limit: number,
  topic_normalised?: string,
) {
  const offset = (page - 1) * limit;
  const result = await query<BookWithTopic>(
    sql`
    SELECT
      b.*,
      t.topic_id,
      t.topic_name,
      t.topic_normalised
    FROM books b
    LEFT JOIN topics t ON b.topic_id = t.topic_id

    WHERE b.is_removed = FALSE
      AND ($1::text IS NULL OR t.topic_normalised = $1)

    LIMIT $2 OFFSET $3
    `,
    [topic_normalised, limit, offset],
  );
  return result.rows;
}

export async function getPeopleForBooks(bookIds: number[]) {
  const result = await query<Books2People>(
    sql`
    SELECT
      b2p.*,
      p.person_id,
      p.unified_id,
      p.family_name,
      p.given_names,
      p.name_particles,
      p.single_name,
      p.is_organisation
    FROM books2people b2p
    LEFT JOIN people p ON b2p.person_id = p.person_id
    WHERE b2p.book_id = ANY($1)
    ORDER BY b2p.book_id, b2p.sort_order
    `,
    [bookIds],
  );
  return result.rows;
}

export async function getPricesForBooks(bookIds: number[]) {
  const result = await query<Price>(
    sql`
    SELECT
    pr.*
    FROM prices pr
    WHERE pr.book_id = ANY($1)
    `,
    [bookIds],
  );
  return result.rows;
}

export async function getBookCount(
  topic_normalised?: string,
  authorPersonId?: number,
) {
  const result = await query<{ count: number }>(
    sql`
    SELECT COUNT(*) as count
    FROM books b
    LEFT JOIN topics t ON b.topic_id = t.topic_id
    LEFT JOIN books2people b2p ON b.book_id = b2p.book_id AND b2p.is_author = TRUE
    WHERE b.is_removed = FALSE
      AND ($1::text IS NULL OR t.topic_normalised = $1)
      AND ($2::integer IS NULL OR b2p.person_id = $2)
    `,
    [topic_normalised, authorPersonId],
  );
  return result.rows[0].count;
}

export async function getAllAuthors() {
  const result = await query<AuthorListItem[]>(
    sql`
      SELECT DISTINCT
        p.person_id,
        p.family_name,
        p.given_names,
        p.name_particles,
        p.single_name,
        p.is_organisation,
        COALESCE(p.family_name, p.single_name) AS sort_name
      FROM people p
      JOIN books2people b2p ON p.person_id = b2p.person_id
      WHERE b2p.is_author = TRUE
      ORDER BY sort_name ASC, p.given_names ASC;
    `,
    [],
  );
  return result.rows;
}

export async function getBooksFilteredByAuthor(
  page: number,
  limit: number,
  authorPersonId: number,
) {
  const offset = (page - 1) * limit;
  const result = await query<BookWithTopic>(
    sql`
    SELECT
      b.*,
      t.topic_id,
      t.topic_name,
      t.topic_normalised
    FROM books b
    LEFT JOIN topics t ON b.topic_id = t.topic_id
    LEFT JOIN books2people b2p ON b.book_id = b2p.book_id
    WHERE b.is_removed = FALSE
      AND b2p.person_id = $1
      AND b2p.is_author = TRUE
    LIMIT $2 OFFSET $3
    `,
    [authorPersonId, limit, offset],
  );
  return result.rows;
}
/**
 * Mark a book as removed (soft delete)
 * Sets is_removed = TRUE for the specified book
 */
export async function markBookAsRemoved(bookId: number) {
  const result = await query(
    `UPDATE books
     SET is_removed = TRUE
     WHERE book_id = $1
     RETURNING book_id`,
    [bookId],
  );

  return result.rows[0];
}

export async function getAllRemovedBooks() {
  const result = await query<BookWithTopic>(
    sql`
    SELECT
      b.*,
      t.topic_id,
      t.topic_name,
      t.topic_normalised
    FROM books b
    LEFT JOIN topics t ON b.topic_id = t.topic_id

    WHERE b.is_removed = TRUE

  `,
    [],
  );

  return result.rows;
}

// old, way too complicated, VERY VERY SLOW

// export async function getAllBooksForTablePaginated(
//   page: number,
//   limit: number,
//   topicNormalised?: string,
//   search?: string,
// ) {
//   const offset = (page - 1) * limit;
//   let whereClause = 'WHERE b.is_removed = FALSE';
//   const params: (number | string | boolean | null)[] = [limit, offset];
//   let paramIndex = 3;

//   if (search) {
//     // When searching, ignore topic filter and search across all fields
//     const searchPattern = `%${search}%`;
//     whereClause += ` AND (
//       b.title ILIKE $${paramIndex} OR
//       b.subtitle ILIKE $${paramIndex} OR
//       p.family_name ILIKE $${paramIndex} OR
//       p.given_names ILIKE $${paramIndex} OR
//       p.single_name ILIKE $${paramIndex}
//     )`;
//     params.push(searchPattern);
//     paramIndex++;
//   } else if (topicNormalised && topicNormalised !== 'all') {
//     whereClause += ` AND t.topic_normalised = $${paramIndex}`;
//     params.push(topicNormalised);
//     paramIndex++;
//   }

//   const result = await query<BookDetail>(
//     sql`
//     SELECT
//       b.book_id,
//       b.title,
//       b.subtitle,
//       b.publication_year,
//       b.publisher,
//       b.place_of_publication,

//       JSONB_BUILD_OBJECT(
//           'topic_id', t.topic_id,
//           'topic_name', t.topic_name,
//           'topic_normalised', t.topic_normalised
//         ) AS topic,

//       JSONB_AGG(
//         JSONB_BUILD_OBJECT(
//           'family_name', p.family_name,
//           'given_names', p.given_names,
//           'name_particles', p.name_particles,
//           'single_name', p.single_name,
//           'display_name', b2p.display_name,
//           'is_author', b2p.is_author,
//           'is_editor', b2p.is_editor
//         )
//       ) AS people,

//       JSONB_AGG(
//         DISTINCT JSONB_BUILD_OBJECT(
//             'price_id', pr.price_id,
//             'amount', pr.amount,
//             'source', pr.source,
//             'imported_price', pr.imported_price,
//             'date_added', pr.date_added
//           )
//         ) FILTER (WHERE pr.price_id IS NOT NULL) AS prices

//     FROM books b
//     LEFT JOIN book_admin ba ON b.book_id = ba.book_id
//     LEFT JOIN topics t ON b.topic_id = t.topic_id
//     LEFT JOIN books2people b2p ON b.book_id = b2p.book_id
//     LEFT JOIN people p ON b2p.person_id = p.person_id
//     LEFT JOIN prices pr ON b.book_id = pr.book_id
//     ${whereClause}
//     GROUP BY b.book_id, b.title, b.subtitle, b.publication_year, b.publisher, b.place_of_publication, t.topic_id
//     ORDER BY
//       CASE
//         WHEN EXISTS (
//           SELECT 1 FROM books2people b2p_check
//           WHERE b2p_check.book_id = b.book_id AND b2p_check.is_author = TRUE
//         )
//         THEN (
//           SELECT p_author.family_name
//           FROM books2people b2p_author
//           JOIN people p_author ON b2p_author.person_id = p_author.person_id
//           WHERE b2p_author.book_id = b.book_id AND b2p_author.is_author = TRUE
//           ORDER BY b2p_author.sort_order
//           LIMIT 1
//         )
//         ELSE (
//           SELECT p_editor.family_name
//           FROM books2people b2p_editor
//           JOIN people p_editor ON b2p_editor.person_id = p_editor.person_id
//           WHERE b2p_editor.book_id = b.book_id AND b2p_editor.is_editor = TRUE
//           ORDER BY b2p_editor.sort_order
//           LIMIT 1
//         )
//       END
//     LIMIT $1 OFFSET $2
//     `,
//     params,
//   );
//   return result.rows;
// }

// export async function getTotalBookCount(
//   topicNormalised?: string,
//   search?: string,
// ) {
//   let whereClause = 'WHERE b.is_removed = FALSE';
//   const params: (string | boolean)[] = [];
//   let paramIndex = 1;

//   if (search) {
//     const searchPattern = `%${search}%`;
//     whereClause += ` AND (
//       b.title ILIKE $${paramIndex} OR
//       b.subtitle ILIKE $${paramIndex} OR
//       p.family_name ILIKE $${paramIndex} OR
//       p.given_names ILIKE $${paramIndex} OR
//       p.single_name ILIKE $${paramIndex}
//     )`;
//     params.push(searchPattern);
//     paramIndex++;
//   } else if (topicNormalised && topicNormalised !== 'all') {
//     whereClause += ` AND t.topic_normalised = $${paramIndex}`;
//     params.push(topicNormalised);
//     paramIndex++;
//   }

//   const result = await query<{ count: number }>(
//     `
//     SELECT COUNT(DISTINCT b.book_id) as count
//     FROM books b
//     LEFT JOIN topics t ON b.topic_id = t.topic_id
//     LEFT JOIN books2people b2p ON b.book_id = b2p.book_id
//     LEFT JOIN people p ON b2p.person_id = p.person_id
//     ${whereClause}
//     `,
//     params,
//   );

//   return result.rows[0].count;
// }

// export async function getSingleBookPageById(id: number) {
//   const result = await query<BookDetail>(
//     sql`
//       SELECT
//         b.*,

//         JSONB_BUILD_OBJECT(
//           'original_entry', ba.original_entry,
//           'parsing_confidence', ba.parsing_confidence,
//           'needs_review', ba.needs_review,
//           'verification_notes', ba.verification_notes,
//           'topic_changed', ba.topic_changed,
//           'price_changed', ba.price_changed,
//           'batch_id', ba.batch_id,
//           'created_at', ba.created_at
//         ) AS admin_data,

//         JSONB_BUILD_OBJECT(
//           'topic_id', t.topic_id,
//           'topic_name', t.topic_name
//         ) AS topic,

//         JSONB_AGG(
//           DISTINCT JSONB_BUILD_OBJECT(
//             'person_id', p.person_id,
//             'unified_id', p.unified_id,
//             'family_name', p.family_name,
//             'given_names', p.given_names,
//             'name_particles', p.name_particles,
//             'single_name', p.single_name,
//             'is_organisation', p.is_organisation,
//             'display_name', b2p.display_name,
//             'is_author', b2p.is_author,
//             'is_editor', b2p.is_editor,
//             'is_contributor', b2p.is_contributor,
//             'is_translator', b2p.is_translator,
//             'sort_order', b2p.sort_order
//           )
//         ) FILTER (WHERE p.person_id IS NOT NULL) AS people,

//         JSONB_AGG(
//           DISTINCT JSONB_BUILD_OBJECT(
//             'volume_id', b2v.volume_id,
//             'volume_number', b2v.volume_number,
//             'volume_title', b2v.volume_title,
//             'pages', b2v.pages,
//             'notes', b2v.notes
//           )
//         ) FILTER (WHERE b2v.volume_id IS NOT NULL) AS volumes,

//         JSONB_AGG(
//           DISTINCT JSONB_BUILD_OBJECT(
//             'price_id', pr.price_id,
//             'amount', pr.amount,
//             'source', pr.source,
//             'imported_price', pr.imported_price,
//             'date_added', pr.date_added
//           )
//         ) FILTER (WHERE pr.price_id IS NOT NULL) AS prices

//       FROM books b
//       LEFT JOIN book_admin ba ON b.book_id = ba.book_id
//       LEFT JOIN topics t ON b.topic_id = t.topic_id
//       LEFT JOIN books2people b2p ON b.book_id = b2p.book_id
//       LEFT JOIN people p ON b2p.person_id = p.person_id
//       LEFT JOIN books2volumes b2v ON b.book_id = b2v.book_id
//       LEFT JOIN prices pr ON b.book_id = pr.book_id
//       WHERE b.book_id = $1
//       GROUP BY b.book_id, t.topic_id, ba.book_id
//     `,
//     [id],
//   );
//   return result.rows[0];
// }

// export async function getAllBooksWithEverything() {
//   const result = await query<BookDisplayRow>(
//     sql`
//      SELECT
//       b.*,
//       ba.*,
//       b2p.*,
//       p.*,
//       t.*,
//       b2v.*,
//       pr.*
//     FROM books b
//     LEFT JOIN book_admin ba ON b.book_id = ba.book_id
//     LEFT JOIN topics t ON b.topic_id = t.topic_id
//     LEFT JOIN books2people b2p ON b.book_id = b2p.book_id
//     LEFT JOIN people p ON b2p.person_id = p.person_id
//     LEFT JOIN books2volumes b2v ON b.book_id = b2v.book_id
//     LEFT JOIN prices pr ON b.book_id = pr.book_id
//     ORDER BY b.title
//     `,
//     [],
//   );
//   return result.rows;
// }

// export async function getBookWithEverythingById(id: number) {
//   const result = await query<BookDisplayRow>(
//     sql`
//     SELECT
//       b.*,
//       ba.*,
//       b2p.*,
//       p.*,
//       t.*,
//       b2v.*,
//       pr.*
//     FROM books b
//     LEFT JOIN book_admin ba ON b.book_id = ba.book_id
//     LEFT JOIN topics t ON b.topic_id = t.topic_id
//     LEFT JOIN books2people b2p ON b.book_id = b2p.book_id
//     LEFT JOIN people p ON b2p.person_id = p.person_id
//     LEFT JOIN books2volumes b2v ON b.book_id = b2v.book_id
//     LEFT JOIN prices pr ON b.book_id = pr.book_id
//     WHERE b.book_id = $1
//     `,
//     [id],
//   );
//   return result.rows;
// }
