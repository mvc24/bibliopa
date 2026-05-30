import { NextRequest, NextResponse } from 'next/server';
import {
  findPublishers,
  findPlaces,
  findLanguages,
} from '@/lib/queries/suggestions';

/**
 * GET /api/suggestions?field=publisher&q=...
 * GET /api/suggestions?field=place&publisher=...
 * GET /api/suggestions?field=language
 *
 * Returns { data: string[] } for autocomplete fields in the book form.
 */
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const field = searchParams.get('field');

  try {
    if (field === 'publisher') {
      const search = searchParams.get('q') || '';
      const rows = await findPublishers(search);
      return NextResponse.json({ data: rows.map((r) => r.publisher) });
    }

    if (field === 'place') {
      const publisher = searchParams.get('publisher') || '';
      const rows = await findPlaces(publisher);
      return NextResponse.json({
        data: rows.map((r) => r.place_of_publication),
      });
    }

    if (field === 'language') {
      const rows = await findLanguages();
      return NextResponse.json({ data: rows.map((r) => r.original_language) });
    }

    return NextResponse.json({ error: 'Unknown field' }, { status: 400 });
  } catch (error) {
    console.error('Error fetching suggestions:', error);
    return NextResponse.json(
      { error: 'Failed to fetch suggestions' },
      { status: 500 },
    );
  }
}
