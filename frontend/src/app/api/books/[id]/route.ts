import { NextRequest, NextResponse } from 'next/server';
import { query, transaction } from '@/lib/db';

/**
 * GET /api/books/[id]
 * Get a single book with all related data
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const bookId = parseInt(params.id);

    if (isNaN(bookId)) {
      return NextResponse.json(
        { error: 'Invalid book ID' },
        { status: 400 }
      );
    }

    // Get book
    const bookResult = await query(
      `SELECT b.*, t.topic_name
       FROM books b
       LEFT JOIN topics t ON b.topic_id = t.topic_id
       WHERE b.book_id = $1`,
      [bookId]
    );

    if (bookResult.rows.length === 0) {
      return NextResponse.json(
        { error: 'Book not found' },
        { status: 404 }
      );
    }

    const book = bookResult.rows[0];

    // Get people (authors, editors, etc.)
    const peopleResult = await query(
      `SELECT * FROM books2people WHERE book_id = $1 ORDER BY sort_order`,
      [bookId]
    );

    // Get prices
    const pricesResult = await query(
      `SELECT * FROM prices WHERE book_id = $1 ORDER BY date_added DESC`,
      [bookId]
    );

    // Get volumes (if multivolume)
    const volumesResult = await query(
      `SELECT * FROM books2volumes WHERE book_id = $1 ORDER BY volume_number`,
      [bookId]
    );

    // Get admin data
    const adminResult = await query(
      `SELECT * FROM book_admin WHERE book_id = $1`,
      [bookId]
    );

    // Combine everything
    const bookWithRelations = {
      ...book,
      authors: peopleResult.rows.filter((p: any) => p.is_author),
      editors: peopleResult.rows.filter((p: any) => p.is_editor),
      contributors: peopleResult.rows.filter((p: any) => p.is_contributor),
      translator: peopleResult.rows.find((p: any) => p.is_translator) || null,
      prices: pricesResult.rows,
      volumes: volumesResult.rows,
      admin_data: adminResult.rows[0] || null,
    };

    return NextResponse.json({ data: bookWithRelations });
  } catch (error) {
    console.error('Error fetching book:', error);
    return NextResponse.json(
      { error: 'Failed to fetch book', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

/**
 * PUT /api/books/[id]
 * Update a book
 * Requires 'family' or 'admin' role (checked by middleware)
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const bookId = parseInt(params.id);
    const body = await request.json();

    if (isNaN(bookId)) {
      return NextResponse.json(
        { error: 'Invalid book ID' },
        { status: 400 }
      );
    }

    // Build update query dynamically based on provided fields
    const updateFields: string[] = [];
    const updateValues: any[] = [];
    let paramIndex = 1;

    const allowedFields = [
      'title', 'subtitle', 'publisher', 'place_of_publication',
      'publication_year', 'edition', 'pages', 'isbn', 'format_original',
      'format_expanded', 'condition', 'copies', 'illustrations', 'packaging',
      'topic_id', 'is_translation', 'original_language', 'is_multivolume',
      'series_title', 'total_volumes'
    ];

    for (const field of allowedFields) {
      if (body[field] !== undefined) {
        updateFields.push(`${field} = $${paramIndex}`);
        updateValues.push(body[field]);
        paramIndex++;
      }
    }

    if (updateFields.length === 0) {
      return NextResponse.json(
        { error: 'No fields to update' },
        { status: 400 }
      );
    }

    // Add updated_at
    updateFields.push(`updated_at = CURRENT_TIMESTAMP`);

    // Add book_id as last parameter
    updateValues.push(bookId);

    const result = await query(
      `UPDATE books SET ${updateFields.join(', ')} WHERE book_id = $${paramIndex} RETURNING *`,
      updateValues
    );

    if (result.rows.length === 0) {
      return NextResponse.json(
        { error: 'Book not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: result.rows[0],
      message: 'Book updated successfully'
    });
  } catch (error) {
    console.error('Error updating book:', error);
    return NextResponse.json(
      { error: 'Failed to update book', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

/**
 * DELETE /api/books/[id]
 * Delete a book (cascades to related tables)
 * Requires 'admin' role (checked by middleware)
 */
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const bookId = parseInt(params.id);

    if (isNaN(bookId)) {
      return NextResponse.json(
        { error: 'Invalid book ID' },
        { status: 400 }
      );
    }

    const result = await query(
      `DELETE FROM books WHERE book_id = $1 RETURNING book_id`,
      [bookId]
    );

    if (result.rows.length === 0) {
      return NextResponse.json(
        { error: 'Book not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      message: 'Book deleted successfully'
    });
  } catch (error) {
    console.error('Error deleting book:', error);
    return NextResponse.json(
      { error: 'Failed to delete book', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
