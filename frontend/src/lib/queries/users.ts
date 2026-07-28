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

export async function getUserByEmail(email: string) {
  const result = await query<User>(
    sql`SELECT * FROM users WHERE email = $1`,
    [email],
  );

  return result.rows[0];
}

export async function getUserById(user_id: string) {
  const result = await query<User>(
    sql`SELECT * FROM users WHERE user_id = $1`,
    [user_id],
  );

  return result.rows[0];
}

export async function createUser(
  username: string,
  email: string,
  password_hash: string,
  role: string,
) {
  const result = await query<User>(
    sql`
        INSERT INTO users (username, email, password_hash, role, is_active)
        VALUES ($1, $2, $3, $4, false)
        RETURNING *
        `,
    [username, email, password_hash, role],
  );

  return result.rows[0];
}

export async function setPassword(user_id: string, password_hash: string) {
  await query(
    sql`
        UPDATE users
        SET password_hash = $1, is_active = true, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = $2
        `,
    [password_hash, user_id],
  );
}

export async function activateUser(user_id: string) {
  await query(
    sql`
        UPDATE users
        SET is_active = true, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = $1
        `,
    [user_id],
  );
}
