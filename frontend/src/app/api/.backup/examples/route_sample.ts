import { NextRequest, NextResponse } from 'next/server';
// TODO(human): Import your query functions from lib/queries/books
// import { getAllBooks, createBook } from '@/lib/queries/books';
import { CreateBookInput } from '@/types/database';
import { getAllBooksWithEverything } from '@/lib/queries/books';

/**
 * GET /api/books
 * List books with pagination, filtering, and search
 *
 * Query params: page, limit, search, topic_id, author
 */
export async function GET(request: NextRequest) {
  try {
    // ===== STEP 1: Extract data from request =====
    const searchParams = request.nextUrl.searchParams;

    // Parse query parameters with defaults
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '50');
    const search = searchParams.get('search') || undefined;
    const topicId = searchParams.get('topic_id') || undefined;

    // ===== STEP 2: Call your query function =====
    // TODO(human): Replace with your query function
    // const { books, totalCount } = await getBooksWithFilters({
    //   page,
    //   limit,
    //   search,
    //   topicId
    // });

    // Temporary placeholder - replace this when you implement your query!
    const books: any[] = [];
    const totalCount = 0;
    const totalPages = Math.ceil(totalCount / limit);

    // Silence unused variable warnings (remove these lines when implementing)
    console.log('TODO: Use these params in query:', { search, topicId });

    // ===== STEP 3: Format and return response =====
    return NextResponse.json({
      data: books,
      pagination: {
        page,
        limit,
        total: totalCount,
        total_pages: totalPages,
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
