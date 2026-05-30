import { NextResponse } from 'next/server';
import { getAllPeople } from '@/lib/queries/suggestions';

/**
 * GET /api/people
 * Returns every person (any role) for the book form's person pickers.
 */
export async function GET() {
  try {
    const people = await getAllPeople();
    return NextResponse.json({ data: people });
  } catch (error) {
    console.error('Error fetching people:', error);
    return NextResponse.json(
      { error: 'Failed to fetch people' },
      { status: 500 },
    );
  }
}
