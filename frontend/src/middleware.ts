import { withAuth } from 'next-auth/middleware';
import { NextResponse } from 'next/server';

/**
 * Middleware to protect routes based on authentication and roles
 * Runs on every request to matched paths
 */
export default withAuth(
  function middleware(req) {
    const token = req.nextauth.token;
    const path = req.nextUrl.pathname;

    // Check if path requires specific roles
    if (
      path.startsWith('/books/new') ||
      (path.startsWith('/books/') && path.includes('/edit'))
    ) {
      // Add/Edit entries requires family or admin role
      if (!token || (token.role !== 'family' && token.role !== 'admin')) {
        return NextResponse.redirect(
          new URL('/login?error=unauthorized', req.url),
        );
      }
    }

    if (path.startsWith('/people/') && path.includes('/edit')) {
      // Edit people requires family or admin role
      if (!token || (token.role !== 'family' && token.role !== 'admin')) {
        return NextResponse.redirect(
          new URL('/login?error=unauthorized', req.url),
        );
      }
    }

    // API routes protection
    if (path.startsWith('/api/')) {
      // POST, PUT, DELETE require authentication
      if (['POST', 'PUT', 'DELETE'].includes(req.method)) {
        if (!token) {
          return NextResponse.json(
            { error: 'Unauthorized', message: 'Authentication required' },
            { status: 401 },
          );
        }

        // Write operations on books/people/prices require family or admin
        if (
          (path.includes('/books') ||
            path.includes('/people') ||
            path.includes('/prices')) &&
          token.role !== 'family' &&
          token.role !== 'admin'
        ) {
          return NextResponse.json(
            { error: 'Forbidden', message: 'Insufficient permissions' },
            { status: 403 },
          );
        }

        // DELETE operations on system data require admin only
        // (books/people/prices already handled above - family can delete those)
        if (
          req.method === 'DELETE' &&
          token.role !== 'admin' &&
          !path.includes('/books') &&
          !path.includes('/people') &&
          !path.includes('/prices')
        ) {
        }
        return NextResponse.json(
          { error: 'Forbidden', message: 'Admin access required' },
          { status: 403 },
        );
      }
    }

    return NextResponse.next();
  },
  {
    callbacks: {
      // Determine which paths require authentication
      authorized: ({ token, req }) => {
        const path = req.nextUrl.pathname;

        // Public paths (no auth required)
        const publicPaths = [
          '/',
          '/login',
          '/bibliography',
          '/books',
          '/project',
          '/contact',
        ];

        // Allow public paths
        if (publicPaths.some((p) => path === p || path.startsWith(p + '/'))) {
          return true;
        }

        // Allow API auth routes
        if (path.startsWith('/api/auth')) {
          return true;
        }

        // Allow GET requests to API (browse without login)
        if (path.startsWith('/api/') && req.method === 'GET') {
          return true;
        }

        // All other paths require authentication
        return !!token;
      },
    },
  },
);

// Specify which routes this middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|public).*)',
  ],
};
