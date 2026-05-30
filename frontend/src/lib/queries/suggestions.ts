import { query, sql } from '@/lib/db';

export async function findPublishers(search: string) {
  const result = await query<{ publisher: string }>(
    sql`
    SELECT DISTINCT publisher
    FROM books
    WHERE publisher ILIKE $1
      AND publisher IS NOT NULL
    ORDER BY publisher
    LIMIT 20
    `,
    [`%${search}%`],
  );
  return result.rows;
}

export async function findPlaces(publisher: string) {
  const result = await query<{ place_of_publication: string; count: number }>(
    sql`
    SELECT place_of_publication, COUNT(*) AS count
    FROM books
    WHERE publisher = $1
      AND place_of_publication IS NOT NULL
    GROUP BY place_of_publication
    ORDER BY count DESC
    LIMIT 10
    `,
    [publisher],
  );
  return result.rows;
}
