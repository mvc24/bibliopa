import { NextRequest, NextResponse } from 'next/server';
import {
  getAdminInfoForSingleBook,
  getPeopleForBooks,
  getPricesForBooks,
  getSingleBook,
  updateBookFields,
  deleteBooks2PeopleForBook,
  getPersonUnifiedId,
  findPersonByUnifiedId,
  insertPerson,
  insertBooks2Person,
} from '@/lib/queries/books';
import { BookDetail, CreateBookInput } from '@/types/database';
import { transaction } from '@/lib/db';
import { generateUnifiedId } from '@/lib/formatters';
import { canModify, canViewPrices } from '@/lib/auth';

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
    const canView = await canViewPrices();
    const canModifyBooks = await canModify();

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
        name_prefix: p.name_prefix,
        name_particles: p.name_particles,
        name_suffix: p.name_suffix,
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
      admin_data: admin ? {
        original_entry: admin.original_entry,
        verification_notes: admin.verification_notes,
        corrected_by_api: admin.corrected_by_api,
        missing_person: admin.missing_person,
        multiple_editions: admin.multiple_editions,
        api_concerned: admin.api_concerned,
        problematic_multi_volume: admin.problematic_multi_volume,
      } : undefined,
    };

    return NextResponse.json({
      data: book,
      permissions: { canViewPrices: canView, canModifyBooks: canModifyBooks },
    });
  } catch (error) {
    console.error('Error fetching book:', error);
    return NextResponse.json(
      { error: 'Failed to fetch book' },
      { status: 500 },
    );
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const bookId = parseInt(id);
    const body: Partial<CreateBookInput> = await request.json();

    if (!body.title) {
      return NextResponse.json(
        { error: 'Validation error', message: 'Title is required' },
        { status: 400 },
      );
    }

    await transaction(async (client) => {
      await updateBookFields(client, bookId, body);
      await deleteBooks2PeopleForBook(client, bookId);

      const bookResult = await client.query(
        `SELECT composite_id FROM books WHERE book_id = $1`,
        [bookId],
      );
      const composite_id: string = bookResult.rows[0].composite_id;

      let sortOrder = 1;

      for (const person of body.people ?? []) {
        const unified_id = await getPersonUnifiedId(client, person.person_id);
        await insertBooks2Person(
          client, bookId, composite_id, person.person_id, unified_id,
          {
            is_author: person.roles.includes('author'),
            is_editor: person.roles.includes('editor'),
            is_contributor: person.roles.includes('contributor'),
            is_translator: person.roles.includes('translator'),
          },
          person.display_name,
          sortOrder++,
        );
      }

      for (const newPerson of body.newPeople ?? []) {
        const unified_id = generateUnifiedId(newPerson);
        const existing = await findPersonByUnifiedId(client, unified_id);
        const person_id = existing
          ? existing.person_id
          : (await insertPerson(client, newPerson, unified_id)).person_id;
        await insertBooks2Person(
          client, bookId, composite_id, person_id, unified_id,
          {
            is_author: newPerson.is_author,
            is_editor: newPerson.is_editor,
            is_contributor: newPerson.is_contributor,
            is_translator: newPerson.is_translator,
          },
          undefined,
          sortOrder++,
        );
      }
    });

    return NextResponse.json({ success: true, data: { book_id: bookId } });
  } catch (error) {
    console.error('Error updating book:', error);
    return NextResponse.json(
      {
        error: 'Failed to update book',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}
