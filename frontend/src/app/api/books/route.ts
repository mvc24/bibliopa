import { NextRequest, NextResponse } from 'next/server';
// TODO(human): Import your query functions from lib/queries/books
// import { getAllBooks, createBook } from '@/lib/queries/books';
import { CreateBookInput } from '@/types/database';
import {
  getAllBooksForTablePaginated,
  getTotalBookCount,
} from '@/lib/queries/books';
import { canViewPrices } from '@/lib/auth';

/**
 * GET /api/books
 * List books with pagination, filtering, and search
 *
 * Query params: page, limit, search, topic_id, author
 */
export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '100');
    const topic = searchParams.get('topic') || undefined;
    const canView = await canViewPrices();

    const books = await getAllBooksForTablePaginated(page, limit, topic);

    const totalCount = await getTotalBookCount();

    // ===== STEP 3: Format and return response =====
    return NextResponse.json({
      data: books,
      pagination: {
        page: page,
        limit: limit,
        total: totalCount,
        total_pages: Math.ceil(totalCount / limit),
      },
      permissions: {
        canViewPrices: canView,
      },
    });
  } catch (error) {
    // ===== STEP 4: Handle errors =====
    console.error('Error fetching books:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch books',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }, // 500 = Internal Server Error
    );
  }
}

/**
 * POST /api/books
 * Create a new book entry
 *
 * Requires 'family' or 'admin' role (checked by middleware)
 *
 * Request body: { title, subtitle, publisher, ... }
 */
export async function POST(request: NextRequest) {
  try {
    // ===== STEP 1: Parse request body =====
    const body: CreateBookInput = await request.json();

    // ===== STEP 2: Validate required fields =====
    if (!body.title) {
      return NextResponse.json(
        { error: 'Validation error', message: 'Title is required' },
        { status: 400 }, // 400 = Bad Request
      );
    }

    // ===== STEP 3: Call your create query function =====
    // TODO(human): Replace with your query function
    // const newBook = await createBook(body);

    // Temporary placeholder - replace this!
    const newBook = { book_id: 1, ...body };

    // ===== STEP 4: Return success response =====
    return NextResponse.json(
      {
        success: true,
        data: newBook,
        message: 'Book created successfully',
      },
      { status: 201 }, // 201 = Created
    );
  } catch (error) {
    // ===== STEP 5: Handle errors =====
    console.error('Error creating book:', error);
    return NextResponse.json(
      {
        error: 'Failed to create book',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}
