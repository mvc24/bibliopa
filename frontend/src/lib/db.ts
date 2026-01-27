import { Pool, QueryResult, QueryResultRow } from 'pg';

// Singleton pattern for database connection pool
let pool: Pool | null = null;

/**
 * Get or create PostgreSQL connection pool
 * Uses singleton pattern to reuse connections across requests
 */
export function getPool(): Pool {
  if (!pool) {
    pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      max: 20, // Maximum number of clients in the pool
      idleTimeoutMillis: 30000, // Close idle clients after 30 seconds
      connectionTimeoutMillis: 2000, // Return error after 2 seconds if no connection available
    });

    // Log pool errors
    pool.on('error', (err) => {
      console.error('Unexpected error on idle PostgreSQL client', err);
      process.exit(-1);
    });
  }

  return pool;
}

/**
 * Execute a query with parameterized values (prevents SQL injection)
 * @param text - SQL query string with $1, $2, etc. placeholders
 * @param params - Array of values to substitute into placeholders
 * @returns Query result
 */
export async function query<T extends QueryResultRow = any>(
  text: string,
  params?: any[]
): Promise<QueryResult<T>> {
  const pool = getPool();
  const start = Date.now();

  try {
    const result = await pool.query<T>(text, params);
    const duration = Date.now() - start;

    // Log slow queries (over 100ms) in development
    if (process.env.NODE_ENV === 'development' && duration > 100) {
      console.log('Slow query executed:', {
        text,
        duration: `${duration}ms`,
        rows: result.rowCount,
      });
    }

    return result;
  } catch (error) {
    console.error('Database query error:', {
      text,
      error: error instanceof Error ? error.message : 'Unknown error',
    });
    throw error;
  }
}

/**
 * Execute a transaction with multiple queries
 * Automatically rolls back if any query fails
 * @param callback - Function that receives a client and executes queries
 * @returns Result from callback
 */
export async function transaction<T>(
  callback: (client: any) => Promise<T>
): Promise<T> {
  const pool = getPool();
  const client = await pool.connect();

  try {
    await client.query('BEGIN');
    const result = await callback(client);
    await client.query('COMMIT');
    return result;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}

/**
 * Close the database pool
 * Call this when shutting down the application
 */
export async function closePool(): Promise<void> {
  if (pool) {
    await pool.end();
    pool = null;
  }
}
