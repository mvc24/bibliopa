import { NextRequest, NextResponse } from 'next/server';

import { BookWithTopic, CreateBookInput } from '@/types/database';
import {
  getBookCount,
  getBooksFilteredByAuthor,
  getBooksOverviewWithTopic,
  getPeopleForBooks,
  getPricesForBooks,
  markBookAsRemoved,
} from '@/lib/queries/books';
import { canViewPrices } from '@/lib/auth';
import { getAllTopics } from '@/lib/queries/topics';

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
    const topicNormalised = searchParams.get('topic') || undefined;
    const search = searchParams.get('search') || undefined;

    const authorPersonId = searchParams.get('author')
      ? parseInt(searchParams.get('author')!)
      : undefined;
    const canView = await canViewPrices();

    let books: BookWithTopic[] = [];
    if (authorPersonId) {
      books = await getBooksFilteredByAuthor(page, limit, authorPersonId);
    } else if (topicNormalised && topicNormalised !== 'all') {
      books = await getBooksOverviewWithTopic(page, limit, topicNormalised);
    } else {
      books = [];
    }
    const totalCount = await getBookCount(topicNormalised, authorPersonId);

    const bookIds = books.map((book) => book.book_id);
    const people = await getPeopleForBooks(bookIds);

    const prices = await getPricesForBooks(bookIds);
    const topics = await getAllTopics();

    const booksWithPeople = books.map((book) => ({
      ...book,
      topic: topics.filter((t) => t.topic_id === book.topic_id),
      people: people.filter((p) => p.book_id === book.book_id),
      prices: prices.filter((p) => p.book_id === book.book_id),
    }));

    // ===== STEP 3: Format and return response =====
    return NextResponse.json({
      data: booksWithPeople,
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

/**
 * PATCH /api/books?id=<book_id>
 * Update book status (currently supports marking as removed)
 *
 * Query params: id (required)
 * Request body: { is_removed: boolean }
 */
export async function PATCH(request: NextRequest) {
  try {
    // ===== STEP 1: Get book ID from query params =====
    const { searchParams } = new URL(request.url);
    const bookIdParam = searchParams.get('id');

    if (!bookIdParam) {
      return NextResponse.json(
        { error: 'Validation error', message: 'Book ID is required' },
        { status: 400 },
      );
    }

    const bookId = parseInt(bookIdParam);

    // ===== STEP 2: Parse request body =====
    const body = await request.json();

    // ===== STEP 3: Update book status =====
    if (body.is_removed === true) {
      await markBookAsRemoved(bookId);
    } else {
      return NextResponse.json(
        {
          error: 'Validation error',
          message: 'Only is_removed=true is supported',
        },
        { status: 400 },
      );
    }

    // ===== STEP 4: Return success response =====
    return NextResponse.json(
      {
        success: true,
        message: 'Book status updated successfully',
      },
      { status: 200 },
    );
  } catch (error) {
    // ===== STEP 5: Handle errors =====
    console.error('Error updating book status:', error);
    return NextResponse.json(
      {
        error: 'Failed to update book status',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}
