import { query, sql } from '@/lib/db';
import { Price } from '@/types/database';

export async function getPricesByBookId(id: number) {
  const result = await query<Price>(
    sql`
    SELECT
    p.*
    FROM prices p
    WHERE p.book_id = $1
    `,
    [id],
  );
  return result.rows;
}

export async function addPriceToBook(
  book_id: number,
  amount: number,
  source: string | null,
) {
  const result = await query<Price>(
    sql`
    INSERT INTO prices (book_id, amount, imported_price, source)
    VALUES ($1, $2, false, $3)
    RETURNING *
    `,
    [book_id, amount, source],
  );
  return result.rows[0];
}
