import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';
import { CreatePersonInput } from '@/types/database';

/**
 * GET /api/people
 * List people with search and filtering
 */
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '50');
    const offset = (page - 1) * limit;

    const search = searchParams.get('search') || undefined;
    const role = searchParams.get('role') || undefined; // author, editor, contributor, translator

    let queryText = `
      SELECT
        p.*,
        COUNT(DISTINCT b2p.book_id) as book_count,
        COUNT(*) OVER() as total_count
      FROM people p
      LEFT JOIN books2people b2p ON p.person_id = b2p.person_id
      WHERE 1=1
    `;

    const queryParams: any[] = [];
    let paramIndex = 1;

    // Search by name
    if (search) {
      queryText += ` AND (
        p.family_name ILIKE $${paramIndex} OR
        p.given_names ILIKE $${paramIndex} OR
        p.single_name ILIKE $${paramIndex}
      )`;
      queryParams.push(`%${search}%`);
      paramIndex++;
    }

    // Filter by role
    if (role) {
      switch (role) {
        case 'author':
          queryText += ` AND b2p.is_author = true`;
          break;
        case 'editor':
          queryText += ` AND b2p.is_editor = true`;
          break;
        case 'contributor':
          queryText += ` AND b2p.is_contributor = true`;
          break;
        case 'translator':
          queryText += ` AND b2p.is_translator = true`;
          break;
      }
    }

    queryText += ` GROUP BY p.person_id`;
    queryText += ` ORDER BY p.family_name, p.given_names`;
    queryText += ` LIMIT $${paramIndex} OFFSET $${paramIndex + 1}`;
    queryParams.push(limit, offset);

    const result = await query(queryText, queryParams);

    const totalCount = result.rows.length > 0 ? parseInt(result.rows[0].total_count) : 0;
    const totalPages = Math.ceil(totalCount / limit);

    return NextResponse.json({
      data: result.rows,
      pagination: {
        page,
        limit,
        total: totalCount,
        total_pages: totalPages,
      },
    });
  } catch (error) {
    console.error('Error fetching people:', error);
    return NextResponse.json(
      { error: 'Failed to fetch people', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

/**
 * POST /api/people
 * Create a new person or return existing if unified_id matches
 * Requires 'family' or 'admin' role (checked by middleware)
 */
export async function POST(request: NextRequest) {
  try {
    const body: CreatePersonInput = await request.json();

    // Generate unified_id (simplified version - you may want to use your Python logic)
    const unifiedId = body.single_name
      ? `single_${body.single_name.toLowerCase().replace(/\s+/g, '_')}`
      : `${body.family_name?.toLowerCase() || ''}_${body.given_names?.toLowerCase().split(' ')[0] || ''}`.replace(/\s+/g, '_');

    // Check if person already exists
    const existingResult = await query(
      `SELECT * FROM people WHERE unified_id = $1`,
      [unifiedId]
    );

    if (existingResult.rows.length > 0) {
      return NextResponse.json({
        success: true,
        data: existingResult.rows[0],
        message: 'Person already exists'
      });
    }

    // Create new person
    const result = await query(
      `INSERT INTO people (
        unified_id, family_name, given_names, name_particles, single_name, is_organisation
      ) VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING *`,
      [
        unifiedId,
        body.family_name || null,
        body.given_names || null,
        body.name_particles || null,
        body.single_name || null,
        body.is_organisation || false,
      ]
    );

    return NextResponse.json(
      { success: true, data: result.rows[0], message: 'Person created successfully' },
      { status: 201 }
    );
  } catch (error) {
    console.error('Error creating person:', error);
    return NextResponse.json(
      { error: 'Failed to create person', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
