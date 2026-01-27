# API Reference

Quick reference for all available API endpoints.

## Authentication

### POST /api/auth/signin
Login with credentials
```json
{
  "username": "admin",
  "password": "password123"
}
```

### POST /api/auth/signout
Logout current session

---

## Books

### GET /api/books
List books with pagination and filters

**Query Parameters:**
- `page` (number) - Page number (default: 1)
- `limit` (number) - Items per page (default: 50)
- `search` (string) - Search in title/subtitle
- `topic_id` (number) - Filter by topic
- `author` (string) - Filter by author name

**Example:**
```bash
GET /api/books?page=1&limit=20&search=philosophy
```

**Response:**
```json
{
  "data": [
    {
      "book_id": 1,
      "title": "Book Title",
      "authors": [...],
      "editors": [...],
      ...
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

### POST /api/books
Create a new book
**Requires:** family or admin role

**Body:**
```json
{
  "title": "Book Title",
  "subtitle": "Optional subtitle",
  "publisher": "Publisher Name",
  "publication_year": 2024,
  "topic_id": 1,
  "authors": [
    {
      "family_name": "Doe",
      "given_names": "John"
    }
  ]
}
```

### GET /api/books/[id]
Get single book with all relations

**Example:**
```bash
GET /api/books/123
```

**Response:**
```json
{
  "data": {
    "book_id": 123,
    "title": "Book Title",
    "authors": [...],
    "prices": [...],
    "volumes": [...],
    "admin_data": {...}
  }
}
```

### PUT /api/books/[id]
Update a book
**Requires:** family or admin role

**Body:** (all fields optional)
```json
{
  "title": "Updated Title",
  "publication_year": 2025,
  "condition": "excellent"
}
```

### DELETE /api/books/[id]
Delete a book (cascades to related tables)
**Requires:** admin role

---

## People

### GET /api/people
List people with search and filtering

**Query Parameters:**
- `page` (number) - Page number
- `limit` (number) - Items per page
- `search` (string) - Search in names
- `role` (string) - Filter by role: author, editor, contributor, translator

**Example:**
```bash
GET /api/people?search=Smith&role=author
```

### POST /api/people
Create a new person (or return existing if unified_id matches)
**Requires:** family or admin role

**Body:**
```json
{
  "family_name": "Smith",
  "given_names": "Jane",
  "name_particles": "von",
  "is_organisation": false
}
```

Or for single name entities:
```json
{
  "single_name": "UNESCO",
  "is_organisation": true
}
```

### GET /api/people/[id]
Get person with their books

**Response:**
```json
{
  "data": {
    "person_id": 456,
    "family_name": "Smith",
    "given_names": "Jane",
    "books": [...],
    "book_count": 12
  }
}
```

### PUT /api/people/[id]
Update person information
**Requires:** family or admin role

**Body:**
```json
{
  "family_name": "Smith-Jones",
  "given_names": "Jane Marie"
}
```

---

## Topics

### GET /api/topics
List all topics with book counts

**Response:**
```json
{
  "data": [
    {
      "topic_id": 1,
      "topic_name": "Philosophy",
      "book_count": 145,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### POST /api/topics
Create a new topic
**Requires:** admin role

**Body:**
```json
{
  "topic_name": "New Topic"
}
```

---

## Prices

### GET /api/prices
Get price history for a book

**Query Parameters:**
- `book_id` (number, required) - Book ID

**Example:**
```bash
GET /api/prices?book_id=123
```

**Response:**
```json
{
  "data": [
    {
      "price_id": 789,
      "book_id": 123,
      "amount": 4500,
      "source": "https://antiquariat.example.com",
      "imported_price": false,
      "date_added": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### POST /api/prices
Add a new price to a book
**Requires:** family or admin role

**Body:**
```json
{
  "book_id": 123,
  "amount": 4500,
  "source": "https://antiquariat.example.com"
}
```

**Note:** Price amounts should be in cents (e.g., 4500 = €45.00)

---

## Error Responses

All endpoints return consistent error format:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (not logged in)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `409` - Conflict (duplicate entry)
- `500` - Internal Server Error

---

## Role Requirements

| Endpoint | Method | Required Role |
|----------|--------|---------------|
| GET /api/books | GET | None (public) |
| POST /api/books | POST | family, admin |
| PUT /api/books/[id] | PUT | family, admin |
| DELETE /api/books/[id] | DELETE | admin |
| GET /api/people | GET | None (public) |
| POST /api/people | POST | family, admin |
| PUT /api/people/[id] | PUT | family, admin |
| GET /api/topics | GET | None (public) |
| POST /api/topics | POST | admin |
| GET /api/prices | GET | None (public)* |
| POST /api/prices | POST | family, admin |

*Note: Prices are only displayed in UI for family and admin roles, but API doesn't restrict reading

---

## Testing with curl

### Login and get session cookie
```bash
curl -X POST http://localhost:3000/api/auth/callback/credentials \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  -c cookies.txt
```

### Use session cookie for authenticated request
```bash
curl -X POST http://localhost:3000/api/books \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"New Book","topic_id":1}'
```

### Search books
```bash
curl "http://localhost:3000/api/books?search=philosophy&page=1&limit=10"
```
