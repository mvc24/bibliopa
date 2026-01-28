import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';

/**
 * GET /api/people/[id]
 * Get a single person with their books
 */
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const personId = parseInt(id);

    if (isNaN(personId)) {
      return NextResponse.json({ error: 'Invalid person ID' }, { status: 400 });
    }

    // Get person
    const personResult = await query(
      `SELECT * FROM people WHERE person_id = $1`,
      [personId],
    );

    if (personResult.rows.length === 0) {
      return NextResponse.json({ error: 'Person not found' }, { status: 404 });
    }

    const person = personResult.rows[0];

    // Get books they're associated with
    const booksResult = await query(
      `SELECT
        b.*,
        b2p.is_author,
        b2p.is_editor,
        b2p.is_contributor,
        b2p.is_translator,
        t.topic_name
       FROM books2people b2p
       JOIN books b ON b2p.book_id = b.book_id
       LEFT JOIN topics t ON b.topic_id = t.topic_id
       WHERE b2p.person_id = $1
       ORDER BY b.publication_year DESC, b.title`,
      [personId],
    );

    const personWithBooks = {
      ...person,
      books: booksResult.rows,
      book_count: booksResult.rows.length,
    };

    return NextResponse.json({ data: personWithBooks });
  } catch (error) {
    console.error('Error fetching person:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch person',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}

/**
 * PUT /api/people/[id]
 * Update a person's information
 * Requires 'family' or 'admin' role (checked by middleware)
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const personId = parseInt(id);
    const body = await request.json();

    if (isNaN(personId)) {
      return NextResponse.json({ error: 'Invalid person ID' }, { status: 400 });
    }

    // Build update query
    const updateFields: string[] = [];
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const updateValues: any[] = [];
    let paramIndex = 1;

    const allowedFields = [
      'family_name',
      'given_names',
      'name_particles',
      'single_name',
      'is_organisation',
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
        { status: 400 },
      );
    }

    // Add updated_at
    updateFields.push(`updated_at = CURRENT_TIMESTAMP`);

    // Add person_id as last parameter
    updateValues.push(personId);

    const result = await query(
      `UPDATE people SET ${updateFields.join(
        ', ',
      )} WHERE person_id = $${paramIndex} RETURNING *`,
      updateValues,
    );

    if (result.rows.length === 0) {
      return NextResponse.json({ error: 'Person not found' }, { status: 404 });
    }

    return NextResponse.json({
      success: true,
      data: result.rows[0],
      message: 'Person updated successfully',
    });
  } catch (error) {
    console.error('Error updating person:', error);
    return NextResponse.json(
      {
        error: 'Failed to update person',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}
