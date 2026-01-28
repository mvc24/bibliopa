import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';
import { CreatePriceInput } from '@/types/database';

/**
 * GET /api/prices
 * Get price history for a book
 * Query param: book_id (required)
 */
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const bookId = searchParams.get('book_id');

    if (!bookId) {
      return NextResponse.json(
        { error: 'book_id query parameter is required' },
        { status: 400 },
      );
    }

    const result = await query(
      `SELECT * FROM prices WHERE book_id = $1 ORDER BY date_added DESC`,
      [parseInt(bookId)],
    );

    return NextResponse.json({ data: result.rows });
  } catch (error) {
    console.error('Error fetching prices:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch prices',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}

/**
 * POST /api/prices
 * Add a new price to a book
 * Requires 'family' or 'admin' role (checked by middleware)
 */
export async function POST(request: NextRequest) {
  try {
    const body: CreatePriceInput = await request.json();

    // Validate required fields
    if (!body.book_id || !body.amount) {
      return NextResponse.json(
        { error: 'book_id and amount are required' },
        { status: 400 },
      );
    }

    // Verify book exists
    const bookCheck = await query(
      `SELECT book_id FROM books WHERE book_id = $1`,
      [body.book_id],
    );

    if (bookCheck.rows.length === 0) {
      return NextResponse.json({ error: 'Book not found' }, { status: 404 });
    }

    // Insert price
    const result = await query(
      `INSERT INTO prices (book_id, amount, source, imported_price)
       VALUES ($1, $2, $3, false)
       RETURNING *`,
      [body.book_id, body.amount, body.source || null],
    );

    return NextResponse.json(
      {
        success: true,
        data: result.rows[0],
        message: 'Price added successfully',
      },
      { status: 201 },
    );
  } catch (error) {
    console.error('Error adding price:', error);
    return NextResponse.json(
      {
        error: 'Failed to add price',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}
