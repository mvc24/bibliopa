# Query Functions Directory

This directory contains all SQL queries separated from the API route logic.

## Structure

Each file represents a database domain:
- `books.ts` - Book-related queries
- `people.ts` - People-related queries (TODO)
- `topics.ts` - Topic-related queries (TODO)
- `prices.ts` - Price-related queries (TODO)

## Practice Workflow

1. **Start with books.ts** - I've created a basic `getAllBooks()` function
2. **Test it** - Import it in the API route and test via http://localhost:3000/api/books
3. **Add complexity** - Add pagination, filtering, JOINs
4. **Create more files** - When ready, create people.ts, topics.ts, etc.

## Query Function Pattern

```typescript
export async function functionName(params: ParamType) {
  const result = await query<ReturnType>(
    `YOUR SQL HERE`,
    [param1, param2] // Always use parameterized queries!
  );

  return result.rows;
}
```

## SQL Tips

- Use `$1, $2, $3` for parameters (prevents SQL injection)
- Use `ILIKE` for case-insensitive search
- Use `COUNT(*) OVER()` for total count with pagination
- Use `JOIN` to combine tables (books + topics, books + people)
- Use `ORDER BY` for sorting
- Use `LIMIT` and `OFFSET` for pagination

## Example: Pagination

```sql
SELECT *, COUNT(*) OVER() as total_count
FROM books
ORDER BY created_at DESC
LIMIT $1 OFFSET $2
```

## Backup Location

Original API route queries are backed up in:
`frontend/src/app/api/.backup/`

You can reference them anytime!
