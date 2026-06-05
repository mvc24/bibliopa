import { query, sql } from '@/lib/db';
import {
  Book,
  BookWithTopic,
  Books2People,
  Price,
  AuthorListItem,
  BookDetail,
  BookAdmin,
  CreateBookInput,
  NewPersonInput,
} from '@/types/database';

/**
 * Get all books with basic information
 * Practice: Start with SELECT * FROM books
 */
export async function getAllBooks() {
  const result = await query<Book>(
    sql`
    SELECT *
    FROM books b
    WHERE b.is_removed = FALSE AND b.is_active <> 0;
    `,
    [],
  );

  return result.rows;
}
export async function getAllBooksPaginated(page: number, limit: number) {
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
    WHERE b.is_removed = FALSE AND b.is_active <> 0
    LIMIT $1 OFFSET $2
    `,
    [limit, offset],
  );

  return result.rows;
}

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

    WHERE b.is_removed = FALSE AND b.is_active <> 0
      AND t.topic_normalised = $1

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
      p.name_prefix,
      p.name_particles,
      p.name_suffix,
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

export async function getCountByAuthor(authorPersonId: number) {
  const result = await query<{ count: number }>(
    sql`
    SELECT COUNT(*)
    FROM books b
    LEFT JOIN books2people b2p ON b.book_id = b2p.book_id AND b2p.is_author = TRUE
    WHERE b.is_removed = FALSE AND b.is_active <> 0
        AND b2p.person_id = $1
    `,
    [authorPersonId],
  );

  return result.rows[0].count;
}

export async function getCountForTopic(topic_normalised: string) {
  const result = await query<{ count: number }>(
    sql`
    SELECT COUNT(*)
    FROM books b
    LEFT JOIN topics t ON b.topic_id = t.topic_id
    WHERE b.is_removed = FALSE AND b.is_active <> 0 AND t.topic_normalised = $1
    `,
    [topic_normalised],
  );

  return result.rows[0].count;
}

export async function getCountForActiveBooks() {
  const result = await query<{ count: number }>(
    sql`
    SELECT COUNT(*)
    FROM books b
    WHERE b.is_removed = FALSE AND b.is_active <> 0
    `,
    [],
  );

  return result.rows[0].count;
}

// export async function getBookCount(
//   topic_normalised?: string,
//   authorPersonId?: number,
// ) {
//   const result = await query<{ count: number }>(
//     sql`
//     SELECT COUNT(DISTINCT b.book_id) as count
//     FROM books b
//     LEFT JOIN topics t ON b.topic_id = t.topic_id
//     LEFT JOIN books2people b2p ON b.book_id = b2p.book_id AND b2p.is_author = TRUE
//     WHERE b.is_removed = FALSE AND b.is_active <> 0
//       AND ($1::text IS NULL OR t.topic_normalised = $1)
//       AND ($2::integer IS NULL OR b2p.person_id = $2)
//     `,
//     [topic_normalised, authorPersonId],
//   );
//   return result.rows[0].count;
// }

export async function getAllAuthors() {
  const result = await query<AuthorListItem[]>(
    sql`
      SELECT DISTINCT
        p.person_id,
        p.family_name,
        p.given_names,
        p.name_prefix,
        p.name_particles,
        p.name_suffix,
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
    WHERE b.is_removed = FALSE AND b.is_active <> 0
      AND b2p.person_id = $1
      AND b2p.is_author = TRUE
    ORDER BY b.title
    LIMIT $2 OFFSET $3
    `,
    [authorPersonId, limit, offset],
  );
  return result.rows;
}

export async function getSingleBook(bookId: number) {
  const result = await query<BookWithTopic>(
    sql`
    SELECT
      b.*,
      t.topic_id,
      t.topic_name,
      t.topic_normalised
    FROM books b
    LEFT JOIN topics t ON b.topic_id = t.topic_id
    WHERE b.book_id = $1 AND b.is_removed = FALSE AND b.is_active <> 0
    `,
    [bookId],
  );
  return result.rows[0];
}

export async function getAdminInfoForSingleBook(bookId: number) {
  const result = await query<BookAdmin>(
    sql`
      SELECT *
      FROM book_admin
      WHERE book_id = $1
    `,
    [bookId],
  );
  return result.rows[0];
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

export async function insertBook(
  client: any,
  input: CreateBookInput,
): Promise<{ book_id: number }> {
  const result = await client.query(
    `INSERT INTO books (
      composite_id, title, subtitle, publisher, place_of_publication,
      publication_year, format_original, format_expanded, condition,
      illustrations, packaging, topic_id, is_translation, original_language,
      is_multivolume
    ) VALUES (
      'pending', $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14
    )
    RETURNING book_id`,
    [
      input.title,
      input.subtitle ?? null,
      input.publisher ?? null,
      input.place_of_publication ?? null,
      input.publication_year ?? null,
      input.format_original ?? null,
      input.format_expanded ?? null,
      input.condition ?? null,
      input.illustrations ?? null,
      input.packaging ?? null,
      input.topic_id ?? null,
      input.is_translation ?? false,
      input.original_language ?? null,
      input.is_multivolume ?? false,
    ],
  );
  return result.rows[0];
}

export async function updateBookCompositeId(
  client: any,
  bookId: number,
  compositeId: string,
): Promise<void> {
  await client.query(
    `UPDATE books SET composite_id = $1 WHERE book_id = $2`,
    [compositeId, bookId],
  );
}

export async function getPersonUnifiedId(
  client: any,
  personId: number,
): Promise<string> {
  const result = await client.query(
    `SELECT unified_id FROM people WHERE person_id = $1`,
    [personId],
  );
  return result.rows[0].unified_id;
}

export async function findPersonByUnifiedId(
  client: any,
  unifiedId: string,
): Promise<{ person_id: number } | null> {
  const result = await client.query(
    `SELECT person_id FROM people WHERE unified_id = $1`,
    [unifiedId],
  );
  return result.rows[0] ?? null;
}

export async function insertPerson(
  client: any,
  input: NewPersonInput,
  unifiedId: string,
): Promise<{ person_id: number }> {
  const result = await client.query(
    `INSERT INTO people (
      unified_id, family_name, given_names, name_prefix, name_particles,
      name_suffix, single_name, is_organisation
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    RETURNING person_id`,
    [
      unifiedId,
      input.family_name ?? null,
      input.given_names ?? null,
      input.name_prefix ?? null,
      input.name_particles ?? null,
      input.name_suffix ?? null,
      input.single_name ?? null,
      input.is_organisation ?? false,
    ],
  );
  return result.rows[0];
}

export async function insertBooks2Person(
  client: any,
  bookId: number,
  compositeId: string,
  personId: number,
  unifiedId: string,
  roles: { is_author: boolean; is_editor: boolean; is_contributor: boolean; is_translator: boolean },
  displayName: string | undefined,
  sortOrder: number,
): Promise<void> {
  await client.query(
    `INSERT INTO books2people (
      book_id, composite_id, person_id, unified_id,
      is_author, is_editor, is_contributor, is_translator,
      display_name, sort_order
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)`,
    [
      bookId,
      compositeId,
      personId,
      unifiedId,
      roles.is_author,
      roles.is_editor,
      roles.is_contributor,
      roles.is_translator,
      displayName ?? null,
      sortOrder,
    ],
  );
}

export async function updateBookFields(
  client: any,
  bookId: number,
  input: Partial<CreateBookInput>,
): Promise<void> {
  await client.query(
    `UPDATE books SET
      title = $1,
      subtitle = $2,
      publisher = $3,
      place_of_publication = $4,
      publication_year = $5,
      format_original = $6,
      format_expanded = $7,
      condition = $8,
      illustrations = $9,
      packaging = $10,
      topic_id = $11,
      is_translation = $12,
      original_language = $13,
      is_multivolume = $14
    WHERE book_id = $15`,
    [
      input.title ?? null,
      input.subtitle ?? null,
      input.publisher ?? null,
      input.place_of_publication ?? null,
      input.publication_year ?? null,
      input.format_original ?? null,
      input.format_expanded ?? null,
      input.condition ?? null,
      input.illustrations ?? null,
      input.packaging ?? null,
      input.topic_id ?? null,
      input.is_translation ?? false,
      input.original_language ?? null,
      input.is_multivolume ?? false,
      bookId,
    ],
  );
}

export async function deleteBooks2PeopleForBook(
  client: any,
  bookId: number,
): Promise<void> {
  await client.query(`DELETE FROM books2people WHERE book_id = $1`, [bookId]);
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
