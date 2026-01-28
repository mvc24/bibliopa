import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';
import { getAllTopics } from '@/lib/queries/topics';
import { Topic } from '@/types/database';

/**

 */
export async function GET(request: NextRequest) {
  try {
    const topics = await getAllTopics();

    return NextResponse.json({ data: topics });
  } catch (error) {
    console.error('Error fetching topics:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch topics',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}

/**
 * POST /api/topics
 * Create a new topic
 * Requires 'admin' role (checked by middleware)
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    if (!body.topic_name) {
      return NextResponse.json(
        { error: 'Topic name is required' },
        { status: 400 },
      );
    }

    // Check if topic already exists
    const existingResult = await query(
      `SELECT * FROM topics WHERE topic_name = $1`,
      [body.topic_name],
    );

    if (existingResult.rows.length > 0) {
      return NextResponse.json(
        { error: 'Topic already exists' },
        { status: 409 },
      );
    }

    // Create new topic
    const result = await query(
      `INSERT INTO topics (topic_name) VALUES ($1) RETURNING *`,
      [body.topic_name],
    );

    return NextResponse.json(
      {
        success: true,
        data: result.rows[0],
        message: 'Topic created successfully',
      },
      { status: 201 },
    );
  } catch (error) {
    console.error('Error creating topic:', error);
    return NextResponse.json(
      {
        error: 'Failed to create topic',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}
