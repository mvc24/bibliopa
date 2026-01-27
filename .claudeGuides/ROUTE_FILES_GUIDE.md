# Understanding route.ts Files

## What is a route.ts File?

A `route.ts` file in Next.js is an **HTTP request handler**. Think of it as the "receptionist" of your API - it receives requests from the frontend, figures out what's needed, asks the database for that information, and sends back a response.

---

## The Job of a route.ts File

### ✅ What It DOES:
1. **Receive HTTP requests** from users/browsers
2. **Extract data** from the request (URL parameters, body, query strings)
3. **Validate input** (check if required fields exist, data is correct format)
4. **Call query functions** (your SQL queries from `lib/queries/`)
5. **Format responses** (wrap data in JSON with proper structure)
6. **Handle errors** (catch problems and return error messages)

### ❌ What It Does NOT Do:
- ❌ Write SQL queries (that's `lib/queries/`)
- ❌ Connect to database directly (that's `lib/db.ts`)
- ❌ Handle authentication (middleware does that)
- ❌ Contain business logic (keep it simple!)

---

## The 4-Step Pattern

Every HTTP handler (GET, POST, PUT, DELETE) follows this pattern:

```typescript
export async function GET(request: NextRequest) {
  try {
    // STEP 1: Extract data from request
    // STEP 2: Call your query function
    // STEP 3: Return formatted response
  } catch (error) {
    // STEP 4: Handle errors
  }
}
```

---

## Step-by-Step Breakdown

### STEP 1: Extract Data from Request

This is where you get information from the HTTP request.

#### From URL Query Parameters
```typescript
// User visits: /api/books?page=2&search=philosophy
const searchParams = request.nextUrl.searchParams;
const page = parseInt(searchParams.get('page') || '1');
const search = searchParams.get('search') || undefined;
```

#### From Request Body
```typescript
// User sends: { "title": "New Book", "author": "Jane Doe" }
const body = await request.json();
// Now body.title = "New Book", body.author = "Jane Doe"
```

#### From URL Path (Dynamic Routes)
```typescript
// In /api/books/[id]/route.ts
// User visits: /api/books/123
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const bookId = parseInt(params.id); // bookId = 123
}
```

---

### STEP 2: Validate Input

Check if the data makes sense BEFORE calling the database.

```typescript
// Check required fields
if (!body.title) {
  return NextResponse.json(
    { error: 'Validation error', message: 'Title is required' },
    { status: 400 } // 400 = Bad Request
  );
}

// Check data types
if (isNaN(bookId)) {
  return NextResponse.json(
    { error: 'Invalid book ID' },
    { status: 400 }
  );
}
```

**Why validate?** Prevents bad data from reaching your database and gives users clear error messages.

---

### STEP 3: Call Your Query Function

This is where your SQL runs (but the SQL lives in `lib/queries/`, not here!).

```typescript
// Import at top of file
import { getBooksWithFilters } from '@/lib/queries/books';

// Inside the handler
const { books, totalCount } = await getBooksWithFilters({
  page,
  limit,
  search,
  topicId
});
```

**Key point:** The route.ts file CALLS the query function, but the query function CONTAINS the SQL.

---

### STEP 4: Format and Return Response

Wrap your data in a consistent JSON structure.

#### Success Response (GET)
```typescript
return NextResponse.json({
  data: books,
  pagination: {
    page: 1,
    limit: 50,
    total: 150,
    total_pages: 3
  }
});
```

#### Success Response (POST/PUT)
```typescript
return NextResponse.json(
  {
    success: true,
    data: newBook,
    message: 'Book created successfully'
  },
  { status: 201 } // 201 = Created
);
```

#### Error Response
```typescript
return NextResponse.json(
  {
    error: 'Failed to create book',
    message: 'Title is required'
  },
  { status: 400 } // or 500, 404, etc.
);
```

---

## HTTP Status Codes

Always include the right status code:

| Code | Name | When to Use |
|------|------|-------------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST (created something new) |
| 400 | Bad Request | User sent invalid data |
| 401 | Unauthorized | User not logged in |
| 403 | Forbidden | User logged in but lacks permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate entry (e.g., book already exists) |
| 500 | Internal Server Error | Something broke on the server |

---

## HTTP Methods (Verbs)

Each method handles a different action:

### GET - Read/Retrieve Data
```typescript
export async function GET(request: NextRequest) {
  // Fetch data from database
  // Return data to user
}
```
- **Does NOT modify** the database
- **Example:** Get list of books, get single book

### POST - Create New Data
```typescript
export async function POST(request: NextRequest) {
  const body = await request.json();
  // Validate body
  // Create new record in database
  // Return the created record
}
```
- **Creates** something new
- **Example:** Add new book, add new price
- Returns status `201`

### PUT - Update Existing Data
```typescript
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await request.json();
  // Update record with ID
  // Return updated record
}
```
- **Modifies** existing record
- **Example:** Edit book details, update person name

### DELETE - Remove Data
```typescript
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  // Delete record with ID
  // Return success message
}
```
- **Removes** a record
- **Example:** Delete book from collection

---

## File Naming and Location

### Pattern: `/api/{resource}/route.ts`

- `/api/books/route.ts` → Handles `/api/books` (list/create)
- `/api/books/[id]/route.ts` → Handles `/api/books/123` (get/update/delete specific book)
- `/api/people/route.ts` → Handles `/api/people`
- `/api/prices/route.ts` → Handles `/api/prices`

### Why `[id]` in Brackets?
- `[id]` is a **dynamic route parameter**
- `/api/books/[id]/route.ts` matches any URL like:
  - `/api/books/1`
  - `/api/books/999`
  - `/api/books/abc123`
- Access it with: `params.id`

---

## How Data Flows

```
User's Browser
    ↓
    → Makes HTTP request: GET /api/books?page=2
    ↓
Middleware (middleware.ts)
    ↓
    → Checks authentication
    → Checks permissions
    ↓
Route Handler (route.ts)
    ↓
    → Extracts: page=2
    → Validates: page is a number
    → Calls: getBooksWithPagination(2, 50)
    ↓
Query Function (lib/queries/books.ts)
    ↓
    → Runs SQL: SELECT * FROM books LIMIT 50 OFFSET 50
    ↓
Database (PostgreSQL)
    ↓
    → Returns: 50 book records
    ↓
Query Function
    ↓
    → Returns: { books: [...], totalCount: 150 }
    ↓
Route Handler
    ↓
    → Formats: { data: books, pagination: {...} }
    → Returns: JSON response
    ↓
User's Browser
    ↓
    → Receives JSON
    → Displays books
```

---

## Practice Template

Use this template for new route files:

```typescript
import { NextRequest, NextResponse } from 'next/server';
// TODO: Import your query functions
// import { yourFunction } from '@/lib/queries/your-file';

/**
 * GET /api/your-endpoint
 * Description of what this does
 */
export async function GET(request: NextRequest) {
  try {
    // STEP 1: Extract data
    const searchParams = request.nextUrl.searchParams;
    const param = searchParams.get('param') || 'default';

    // STEP 2: Call query function
    // const data = await yourQueryFunction(param);

    // STEP 3: Return response
    return NextResponse.json({ data: [] });

  } catch (error) {
    // STEP 4: Handle errors
    console.error('Error:', error);
    return NextResponse.json(
      { error: 'Failed', message: error instanceof Error ? error.message : 'Unknown' },
      { status: 500 }
    );
  }
}

/**
 * POST /api/your-endpoint
 * Description of what this creates
 */
export async function POST(request: NextRequest) {
  try {
    // STEP 1: Parse body
    const body = await request.json();

    // STEP 2: Validate
    if (!body.requiredField) {
      return NextResponse.json(
        { error: 'Field required' },
        { status: 400 }
      );
    }

    // STEP 3: Call create function
    // const result = await createFunction(body);

    // STEP 4: Return success
    return NextResponse.json(
      { success: true, data: {} },
      { status: 201 }
    );

  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: 'Failed', message: error instanceof Error ? error.message : 'Unknown' },
      { status: 500 }
    );
  }
}
```

---

## Common Mistakes to Avoid

### ❌ DON'T: Put SQL in route.ts
```typescript
// BAD - SQL in route file
export async function GET(request: NextRequest) {
  const result = await query('SELECT * FROM books');
  return NextResponse.json({ data: result.rows });
}
```

### ✅ DO: Call query functions
```typescript
// GOOD - SQL in lib/queries/, route just calls it
export async function GET(request: NextRequest) {
  const books = await getAllBooks();
  return NextResponse.json({ data: books });
}
```

### ❌ DON'T: Forget error handling
```typescript
// BAD - no try/catch
export async function GET(request: NextRequest) {
  const books = await getAllBooks(); // What if this fails?
  return NextResponse.json({ data: books });
}
```

### ✅ DO: Always use try/catch
```typescript
// GOOD - handles errors
export async function GET(request: NextRequest) {
  try {
    const books = await getAllBooks();
    return NextResponse.json({ data: books });
  } catch (error) {
    return NextResponse.json({ error: 'Failed' }, { status: 500 });
  }
}
```

### ❌ DON'T: Forget status codes
```typescript
// BAD - always returns 200 even on error
return NextResponse.json({ error: 'Failed' });
```

### ✅ DO: Use correct status codes
```typescript
// GOOD - tells client what went wrong
return NextResponse.json({ error: 'Failed' }, { status: 500 });
```

---

## Summary

**A route.ts file is a request handler that:**
1. Receives HTTP requests
2. Extracts and validates data
3. Calls query functions (which contain SQL)
4. Returns formatted JSON responses
5. Handles errors gracefully

**It does NOT contain:**
- SQL queries (those go in `lib/queries/`)
- Database connections (that's in `lib/db.ts`)
- Authentication logic (middleware handles that)

Think of it as the **middleman** between your frontend and your database queries!
