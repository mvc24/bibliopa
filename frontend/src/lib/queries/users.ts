import { query, sql } from '@/lib/db';
import { User } from '@/types/database';

export async function getActiveUser(identifier: string) {
  const result = await query<User>(
    sql`
        SELECT *
        FROM users
        WHERE (username = $1 OR email = $1) AND is_active = true
        `,
    [identifier],
  );

  return result.rows[0];
}
