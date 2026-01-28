import { NextRequest, NextResponse } from 'next/server';
import { query, transaction } from '@/lib/db';
import {
  BookWithRelations,
  CreateBookInput,
  BookFilters,
} from '@/types/database';

/**
 * GET /api/books
 * List books with pagination, filtering, and search
 */
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '50');
    const offset = (page - 1) * limit;

    const search = searchParams.get('search') || undefined;
    const topicId = searchParams.get('topic_id') || undefined;
    const author = searchParams.get('author') || undefined;

    // Build query with filters
    let queryText = `
      SELECT
        b.*,
        t.topic_name,
        COUNT(*) OVER() as total_count
      FROM books b
      LEFT JOIN topics t ON b.topic_id = t.topic_id
      WHERE 1=1
    `;

    const queryParams: any[] = [];
    let paramIndex = 1;

    // Add search filter (searches title and subtitle)
    if (search) {
      queryText += ` AND (b.title ILIKE $${paramIndex} OR b.subtitle ILIKE $${paramIndex})`;
      queryParams.push(`%${search}%`);
      paramIndex++;
    }

    // Add topic filter
    if (topicId) {
      queryText += ` AND b.topic_id = $${paramIndex}`;
      queryParams.push(parseInt(topicId));
      paramIndex++;
    }

    // Add pagination
    queryText += ` ORDER BY b.created_at DESC LIMIT $${paramIndex} OFFSET $${
      paramIndex + 1
    }`;
    queryParams.push(limit, offset);

    const result = await query(queryText, queryParams);

    const totalCount =
      result.rows.length > 0 ? parseInt(result.rows[0].total_count) : 0;
    const totalPages = Math.ceil(totalCount / limit);

    // For each book, get authors/editors
    const booksWithPeople = await Promise.all(
      result.rows.map(async (book) => {
        const peopleResult = await query(
          `SELECT * FROM books2people WHERE book_id = $1 ORDER BY sort_order`,
          [book.book_id],
        );

        return {
          ...book,
          authors: peopleResult.rows.filter((p: any) => p.is_author),
          editors: peopleResult.rows.filter((p: any) => p.is_editor),
          contributors: peopleResult.rows.filter((p: any) => p.is_contributor),
          translator:
            peopleResult.rows.find((p: any) => p.is_translator) || null,
        };
      }),
    );

    return NextResponse.json({
      data: booksWithPeople,
      pagination: {
        page,
        limit,
        total: totalCount,
        total_pages: totalPages,
      },
    });
  } catch (error) {
    console.error('Error fetching books:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch books',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}

/**
 * POST /api/books
 * Create a new book entry
 * Requires 'family' or 'admin' role (checked by middleware)
 */
export async function POST(request: NextRequest) {
  try {
    const body: CreateBookInput = await request.json();

    // Validate required fields
    if (!body.title) {
      return NextResponse.json(
        { error: 'Validation error', message: 'Title is required' },
        { status: 400 },
      );
    }

    // Use transaction to insert book and related people
    const result = await transaction(async (client) => {
      // Generate composite_id (you might want to customize this)
      const compositeId = `new_${Date.now()}`;

      // Insert book
      const bookResult = await client.query(
        `INSERT INTO books (
          composite_id, title, subtitle, publisher, place_of_publication,
          publication_year, edition, pages, isbn, format_original, format_expanded,
          condition, copies, illustrations, packaging, topic_id, is_translation,
          original_language, is_multivolume, series_title, total_volumes
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21)
        RETURNING *`,
        [
          compositeId,
          body.title,
          body.subtitle || null,
          body.publisher || null,
          body.place_of_publication || null,
          body.publication_year || null,
          body.edition || null,
          body.pages || null,
          body.isbn || null,
          body.format_original || null,
          body.format_expanded || null,
          body.condition || null,
          body.copies || null,
          body.illustrations || null,
          body.packaging || null,
          body.topic_id || null,
          body.is_translation || false,
          body.original_language || null,
          body.is_multivolume || false,
          body.series_title || null,
          body.total_volumes || null,
        ],
      );

      const newBook = bookResult.rows[0];

      // TODO: Insert authors, editors, contributors, translator
      // This would require checking if people exist, creating unified_ids, etc.
      // For now, returning just the book

      return newBook;
    });

    return NextResponse.json(
      { success: true, data: result, message: 'Book created successfully' },
      { status: 201 },
    );
  } catch (error) {
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
