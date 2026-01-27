# Bibliopa Frontend - Getting Started

Your Next.js boilerplate with authentication and API routes is now complete! This guide will help you get up and running.

## What's Been Created

### ✅ Authentication System
- **NextAuth.js** configured with credentials provider
- **JWT-based sessions** (30-day expiry)
- **Role-based access control** (admin, family, viewer, guest)
- **Protected routes** via middleware

### ✅ Database Layer
- **PostgreSQL connection pool** in `src/lib/db.ts`
- **Type-safe queries** with TypeScript interfaces
- **Transaction support** for complex operations

### ✅ API Routes
All CRUD operations are ready:
- `/api/books` - List, create books
- `/api/books/[id]` - Get, update, delete individual book
- `/api/people` - List, create people
- `/api/people/[id]` - Get, update individual person
- `/api/topics` - List, create topics
- `/api/prices` - Get price history, add new prices

### ✅ TypeScript Types
Complete type definitions in `src/types/database.ts` matching your PostgreSQL schema

### ✅ Accessibility Enhancements
- Larger default font sizes (18px base)
- Larger button sizes (lg default)
- Focus rings always visible
- Designed for 90-year-old user with tremor

## Quick Start

### 1. Start the Development Server
```bash
cd frontend
npm run dev
```

Visit: http://localhost:3000

### 2. Create Your First User
You'll need to manually insert a user into the database to test login:

```sql
-- Connect to your PostgreSQL database
psql -U mvc -d bibliopa

-- Create an admin user (password: "admin123")
INSERT INTO users (username, email, password_hash, role, is_active)
VALUES (
  'admin',
  'admin@bibliopa.local',
  '$2a$10$YourHashedPasswordHere',  -- You'll need to generate this (see below)
  'admin',
  true
);
```

To generate a password hash:
```bash
node -e "const bcrypt = require('bcryptjs'); console.log(bcrypt.hashSync('admin123', 10));"
```

### 3. Test Authentication
1. Navigate to http://localhost:3000/login
2. Enter username: `admin`, password: `admin123`
3. You should be logged in and redirected

### 4. Test API Routes
Try these URLs in your browser or with curl:

**List books:**
```bash
curl http://localhost:3000/api/books
```

**Get topics:**
```bash
curl http://localhost:3000/api/topics
```

**Create a book (requires authentication):**
```bash
# First, login to get a session cookie, then:
curl -X POST http://localhost:3000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Book",
    "topic_id": 1
  }'
```

## File Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth/[...nextauth]/route.ts  # NextAuth config
│   │   │   ├── books/route.ts               # Books CRUD
│   │   │   ├── books/[id]/route.ts          # Individual book
│   │   │   ├── people/route.ts              # People CRUD
│   │   │   ├── people/[id]/route.ts         # Individual person
│   │   │   ├── topics/route.ts              # Topics
│   │   │   └── prices/route.ts              # Prices
│   │   ├── layout.tsx                       # Root layout
│   │   └── page.tsx                         # Landing page
│   ├── components/
│   │   ├── providers.tsx                    # SessionProvider + Mantine
│   │   └── ...
│   ├── lib/
│   │   ├── db.ts                            # Database connection pool
│   │   └── auth.ts                          # Auth utilities
│   ├── types/
│   │   ├── database.ts                      # TypeScript types
│   │   └── next-auth.d.ts                   # NextAuth type extensions
│   └── middleware.ts                        # Route protection
├── .env.local                               # Environment variables
└── package.json
```

## Environment Variables

Already configured in `.env.local`:
- `DATABASE_URL` - PostgreSQL connection string
- `NEXTAUTH_URL` - Application URL (http://localhost:3000)
- `NEXTAUTH_SECRET` - Secret for session encryption

## Role Permissions

| Role     | View | Download | Add/Edit | Delete | View Prices | Add Prices |
|----------|------|----------|----------|--------|-------------|------------|
| admin    | ✅   | ✅       | ✅       | ✅     | ✅          | ✅         |
| family   | ✅   | ✅       | ✅       | ❌     | ✅          | ✅         |
| viewer   | ✅   | ✅       | ❌       | ❌     | ❌          | ❌         |
| guest    | ✅   | ❌       | ❌       | ❌     | ❌          | ❌         |

## Next Steps

### 1. Create Login Page UI
The `/login` route exists but needs a form. Example:

```tsx
// src/app/login/page.tsx
'use client';
import { signIn } from 'next-auth/react';
import { useState } from 'react';
import { TextInput, PasswordInput, Button, Stack } from '@mantine/core';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await signIn('credentials', {
      username,
      password,
      callbackUrl: '/bibliography',
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <Stack>
        <TextInput
          label="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <PasswordInput
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button type="submit">Login</Button>
      </Stack>
    </form>
  );
}
```

### 2. Build Bibliography Page
Use the Books API to display books in a table or grid.

### 3. Create Book Forms
Use Mantine forms with React Hook Form (already installed) for adding/editing books.

### 4. Implement Search
Add search functionality that calls `/api/books?search=query`.

### 5. Price Tracking UI
Create interface for adding prices to books using `/api/prices`.

## Troubleshooting

### Database Connection Errors
- Verify PostgreSQL is running: `pg_ctl status`
- Check `.env.local` has correct credentials
- Test connection: `psql -U mvc -d bibliopa`

### Authentication Not Working
- Ensure `NEXTAUTH_SECRET` is set
- Clear browser cookies and try again
- Check browser console for errors

### TypeScript Errors
- Run `npm run dev` to see detailed errors
- Ensure all imports use `@/` prefix (configured in tsconfig.json)

## Documentation

- [Next.js Docs](https://nextjs.org/docs)
- [NextAuth.js Docs](https://next-auth.js.org/)
- [Mantine UI Docs](https://mantine.dev/)
- [PostgreSQL node-postgres Docs](https://node-postgres.com/)

## Support

If you encounter issues:
1. Check browser console for errors
2. Check terminal for server errors
3. Review the plan file: `~/.claude/plans/happy-rolling-wilkes.md`
