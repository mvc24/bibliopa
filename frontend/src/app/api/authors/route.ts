import { NextResponse } from 'next/server';
import { getAllAuthors } from '@/lib/queries/books';

export async function GET() {
  try {
    const authors = await getAllAuthors();
    return NextResponse.json({ data: authors });
  } catch (error) {
    console.error('Error fetching authors:', error);
    return NextResponse.json(
      { error: 'Failed to fetch authors' },
      { status: 500 },
    );
  }
}
