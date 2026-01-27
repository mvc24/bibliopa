# Your Practice Setup - Ready to Go! 🚀

Everything is set up for you to practice writing SQL queries and API routes.

---

## 📁 What's Been Created

### 1. Query Practice Directory
```
frontend/src/lib/queries/
├── README.md           # SQL tips and practice workflow
└── books.ts           # Your starting point (basic SELECT * FROM books)
```

### 2. Simplified Route Template
```
frontend/src/app/api/books/route.ts
```
This file shows the **framework** for route handlers:
- How to extract data from requests
- How to validate input
- Where to call your query functions
- How to format responses
- How to handle errors

**No SQL queries in this file!** They belong in `lib/queries/`

### 3. Backups of Original Code
```
frontend/src/app/api/.backup/
├── books/
├── people/
├── topics/
└── prices/
```
All my original queries are here if you need reference!

### 4. Documentation
- **[ROUTE_FILES_GUIDE.md](ROUTE_FILES_GUIDE.md)** - Complete explanation of route.ts files
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - How to run the frontend
- **[API_REFERENCE.md](API_REFERENCE.md)** - All API endpoints documented

---

## 🎯 Your Learning Path

### Phase 1: Start with Simple Queries

**File:** `frontend/src/lib/queries/books.ts`

1. **Test the basic query** (already written for you):
   ```typescript
   export async function getAllBooks() {
     const result = await query<Book>(`SELECT * FROM books`, []);
     return result.rows;
   }
   ```

2. **Connect it to the API route**:
   - Open `frontend/src/app/api/books/route.ts`
   - Uncomment the import
   - Replace placeholder with `const books = await getAllBooks()`

3. **Test it**:
   ```bash
   npm run dev
   # Visit: http://localhost:3000/api/books
   ```

### Phase 2: Add Pagination

In `books.ts`, write a new function:

```typescript
export async function getBooksWithPagination(page: number, limit: number) {
  const offset = (page - 1) * limit;

  // TODO(human): Write SQL with LIMIT and OFFSET
  const result = await query(
    `YOUR SQL HERE`,
    [limit, offset]
  );

  return result.rows;
}
```

**SQL Hint:**
- Use `LIMIT $1 OFFSET $2`
- Remember: `$1` = first parameter (limit), `$2` = second (offset)

### Phase 3: Add Search

```typescript
export async function searchBooks(searchTerm: string) {
  // TODO(human): Write SQL with WHERE and ILIKE
  // Hint: ILIKE is case-insensitive search
  // Search in both title AND subtitle
}
```

**SQL Hint:**
- Use `WHERE title ILIKE $1 OR subtitle ILIKE $1`
- Wrap the search term: `%${searchTerm}%` (add % in the query or when passing param)

### Phase 4: Join with Topics

```typescript
export async function getBooksWithTopics(page: number, limit: number) {
  // TODO(human): JOIN books table with topics table
  // Return both book data AND topic_name
}
```

**SQL Hint:**
- Use `LEFT JOIN topics t ON b.topic_id = t.topic_id`

### Phase 5: Complex Filters

Combine everything:
- Pagination
- Search
- Topic filter
- Order by date

Reference the backup files if you get stuck!

---

## 🔍 How to Check Your Work

### 1. TypeScript Will Help You
If you mess up, TypeScript will show errors in VSCode:
- Red squiggles = error
- Click on them to see what's wrong

### 2. Test in Browser
```bash
npm run dev
```
Visit: http://localhost:3000/api/books

If you see JSON data, it worked! ✅

### 3. Check the Terminal
Look for errors in the terminal where `npm run dev` is running.

### 4. Use the Backup
Compare your query to `.backup/books/route.ts` to see how I did it.

---

## 📝 SQL Quick Reference

### Parameterized Queries (IMPORTANT!)
```sql
-- ✅ CORRECT (prevents SQL injection)
SELECT * FROM books WHERE title = $1

-- ❌ WRONG (vulnerable to SQL injection)
SELECT * FROM books WHERE title = '${title}'
```

### Common Patterns

**Pagination:**
```sql
SELECT * FROM books
ORDER BY created_at DESC
LIMIT $1 OFFSET $2
```

**Search (case-insensitive):**
```sql
SELECT * FROM books
WHERE title ILIKE $1  -- matches %search%
```

**Join:**
```sql
SELECT b.*, t.topic_name
FROM books b
LEFT JOIN topics t ON b.topic_id = t.topic_id
```

**Count with Pagination:**
```sql
SELECT *, COUNT(*) OVER() as total_count
FROM books
LIMIT $1 OFFSET $2
```

**Multiple Filters:**
```sql
SELECT * FROM books
WHERE 1=1
  AND ($1 IS NULL OR title ILIKE $1)
  AND ($2 IS NULL OR topic_id = $2)
```

---

## 🚨 Common Mistakes

### ❌ Forgetting Parameters Array
```typescript
// WRONG - no parameters array
await query(`SELECT * FROM books WHERE id = $1`);
```

```typescript
// RIGHT - parameters provided
await query(`SELECT * FROM books WHERE id = $1`, [bookId]);
```

### ❌ String Concatenation
```typescript
// WRONG - SQL injection risk!
await query(`SELECT * FROM books WHERE title = '${title}'`);
```

```typescript
// RIGHT - parameterized
await query(`SELECT * FROM books WHERE title = $1`, [title]);
```

### ❌ Wrong Parameter Numbers
```typescript
// WRONG - $1, $2, but only 1 parameter
await query(`SELECT * WHERE id = $1 AND topic = $2`, [bookId]);
```

```typescript
// RIGHT - match parameters
await query(`SELECT * WHERE id = $1 AND topic = $2`, [bookId, topicId]);
```

---

## 💡 Tips for Success

1. **Start Simple** - Get `SELECT *` working before adding complexity
2. **Test Each Change** - Don't write everything at once
3. **Use the Backup** - Reference `.backup/` when stuck
4. **Read Error Messages** - They usually tell you exactly what's wrong
5. **Console.log is Your Friend** - Add `console.log(result.rows)` to see what you got back

---

## 🎓 Learning Goals

By the end of this practice, you should understand:

✅ How to write parameterized SQL queries
✅ How to use LIMIT/OFFSET for pagination
✅ How to JOIN tables
✅ How to filter with WHERE clauses
✅ How route.ts files work
✅ How query functions and routes work together

---

## 📚 Where to Get Help

1. **Check the guides:**
   - [ROUTE_FILES_GUIDE.md](ROUTE_FILES_GUIDE.md)
   - [lib/queries/README.md](src/lib/queries/README.md)

2. **Look at backups:**
   - [src/app/api/.backup/](src/app/api/.backup/)

3. **PostgreSQL docs:**
   - [node-postgres documentation](https://node-postgres.com/)
   - [PostgreSQL SELECT docs](https://www.postgresql.org/docs/current/sql-select.html)

---

## 🎉 You're Ready!

Start with Phase 1, take it step by step, and remember:
- **Queries go in `lib/queries/`**
- **HTTP handling goes in `api/*/route.ts`**
- **Test after each change**
- **Use the backups when stuck**

Good luck! 🚀
