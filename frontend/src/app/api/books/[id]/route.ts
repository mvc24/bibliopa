import { NextRequest, NextResponse } from 'next/server';
import {
  getAdminInfoForSingleBook,
  getPeopleForBooks,
  getPricesForBooks,
  getSingleBook,
} from '@/lib/queries/books';
import { BookDetail } from '@/types/database';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const bookId = parseInt(id);

    const bookBase = await getSingleBook(bookId);
    const people = await getPeopleForBooks([bookId]);
    const prices = await getPricesForBooks([bookId]);
    const admin = await getAdminInfoForSingleBook(bookId);

    const book: BookDetail = {
      ...bookBase,
      topic: bookBase.topic_id
        ? {
            topic_id: bookBase.topic_id,
            topic_name: bookBase.topic_name!,
            topic_normalised: bookBase.topic_normalised!,
          }
        : undefined,
      people: people.map((p) => ({
        person_id: p.person_id,
        unified_id: p.unified_id,
        display_name: p.display_name,
        family_name: p.family_name,
        given_names: p.given_names,
        name_particles: p.name_particles,
        single_name: p.single_name,
        is_organisation: p.is_organisation,
        is_author: p.is_author,
        is_editor: p.is_editor,
        is_contributor: p.is_contributor,
        is_translator: p.is_translator,
        sort_order: p.sort_order,
      })),
      prices: prices.map((pr) => ({
        price_id: pr.price_id,
        amount: pr.amount,
        source: pr.source,
        imported_price: pr.imported_price,
        date_added: pr.date_added,
      })),
      admin_data: {
        original_entry: admin.original_entry,
        verification_notes: admin.verification_notes,
        topic_changed: admin.topic_changed,
      },
    };

    return NextResponse.json(book);
  } catch (error) {
    console.error('Error fetching book:', error);
    return NextResponse.json(
      { error: 'Failed to fetch book' },
      { status: 500 },
    );
  }
}
