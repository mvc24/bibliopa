import { NextRequest, NextResponse } from 'next/server';

import {
  Books2People,
  BookWithTopic,
  CreateBookInput,
  Price,
  Topic,
} from '@/types/database';
import { TOPICS } from '@/components/topics';
import {
  getBooksFilteredByAuthor,
  getAllBooksPaginated,
  getBooksOverviewWithTopic,
  searchBooks,
  getCountByAuthor,
  getCountForActiveBooks,
  getCountForTopic,
  getCountForSearch,
  getPeopleForBooks,
  getPricesForBooks,
  markBookAsRemoved,
  insertBook,
  updateBookCompositeId,
  getPersonUnifiedId,
  findPersonByUnifiedId,
  insertPerson,
  insertBooks2Person,
} from '@/lib/queries/books';
import { transaction } from '@/lib/db';
import { generateUnifiedId } from '@/lib/formatters';
import { canModify, canViewPrices } from '@/lib/auth';

/**
 * GET /api/books
 * List books with pagination, filtering, and search
 *
 * Query params: page, limit, search, topic_id, author
 */

type BookWithEverything = BookWithTopic & {
  topic: Topic | null;
  people: Books2People[];
  prices: Price[];
};

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '100');
    const topicNormalised = searchParams.get('topic') || undefined;
    const search = searchParams.get('search') || undefined;

    const authorPersonId = searchParams.get('author')
      ? parseInt(searchParams.get('author')!)
      : undefined;
    const canView = await canViewPrices();
    const canModifyBooks = await canModify();

    let totalCount: number;

    const books = search
      ? await searchBooks(page, limit, search)
      : authorPersonId
        ? await getBooksFilteredByAuthor(page, limit, authorPersonId)
        : topicNormalised
          ? await getBooksOverviewWithTopic(page, limit, topicNormalised)
          : await getAllBooksPaginated(page, limit);

    if (search) {
      totalCount = await getCountForSearch(search);
    } else if (authorPersonId) {
      totalCount = await getCountByAuthor(authorPersonId);
    } else if (topicNormalised) {
      totalCount = await getCountForTopic(topicNormalised);
    } else {
      totalCount = await getCountForActiveBooks();
    }

    console.log(
      'Total count:',
      totalCount,
      'Topic:',
      topicNormalised,
      'Author:',
      authorPersonId,
    );

    const bookIds = books.map((book) => book.book_id);
    const people = await getPeopleForBooks(bookIds);

    const prices = await getPricesForBooks(bookIds);
    const topics = TOPICS;

    const booksWithPeople = books.map((book) => ({
      ...book,
      topic: topics.find((t) => t.topic_id === book.topic_id) || null,
      people: people.filter((p) => p.book_id === book.book_id),
      prices: prices.filter((p) => p.book_id === book.book_id),
    }));

    function getSortKey(book: BookWithEverything) {
      const firstAuthor = book.people
        .filter((p) => p.is_author)
        .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))[0];
      if (firstAuthor) {
        return (
          firstAuthor.family_name ||
          firstAuthor.single_name ||
          ''
        ).toUpperCase();
      }
      return book.title.toUpperCase();
    }

    booksWithPeople.sort((a, b) => {
      const keyA = getSortKey(a);
      const keyB = getSortKey(b);
      return keyA.localeCompare(keyB);
    });

    // ===== STEP 3: Format and return response =====
    return NextResponse.json({
      data: booksWithPeople,
      pagination: {
        page: page,
        limit: limit,
        total: totalCount,
        total_pages: Math.ceil(totalCount / limit),
      },
      permissions: {
        canViewPrices: canView,
        canModifyBooks: canModifyBooks,
      },
    });
  } catch (error) {
    // ===== STEP 4: Handle errors =====
    console.error('Error fetching books:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch books',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }, // 500 = Internal Server Error
    );
  }
}

/**
 * POST /api/books
 * Create a new book entry
 *
 * Requires 'family' or 'admin' role (checked by middleware)
 *
 * Request body: { title, subtitle, publisher, ... }
 */
export async function POST(request: NextRequest) {
  try {
    // ===== STEP 1: Parse request body =====
    const body: CreateBookInput = await request.json();

    // ===== STEP 2: Validate required fields =====
    if (!body.title) {
      return NextResponse.json(
        { error: 'Validation error', message: 'Title is required' },
        { status: 400 }, // 400 = Bad Request
      );
    }

    // ===== STEP 3: Create book, people, and links in one transaction =====

    const newBook = await transaction(async (client) => {
      const { book_id } = await insertBook(client, body);

      const topic = TOPICS.find((t) => t.topic_id === body.topic_id);
      const composite_id = `${topic?.topic_normalised ?? 'unknown'}_${book_id}`;
      await updateBookCompositeId(client, book_id, composite_id);

      let sortOrder = 1;

      for (const person of body.people ?? []) {
        const unified_id = await getPersonUnifiedId(client, person.person_id);
        await insertBooks2Person(
          client, book_id, composite_id, person.person_id, unified_id,
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
          client, book_id, composite_id, person_id, unified_id,
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

      return { book_id, composite_id };
    });

    // ===== STEP 4: Return success response =====
    return NextResponse.json(
      {
        success: true,
        data: newBook,
        message: 'Book created successfully',
      },
      { status: 201 }, // 201 = Created
    );
  } catch (error) {
    // ===== STEP 5: Handle errors =====
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

/**
 * PATCH /api/books?id=<book_id>
 * Update book status (currently supports marking as removed)
 *
 * Query params: id (required)
 * Request body: { is_removed: boolean }
 */
export async function PATCH(request: NextRequest) {
  try {
    // ===== STEP 1: Get book ID from query params =====
    const { searchParams } = new URL(request.url);
    const bookIdParam = searchParams.get('id');

    if (!bookIdParam) {
      return NextResponse.json(
        { error: 'Validation error', message: 'Book ID is required' },
        { status: 400 },
      );
    }

    const bookId = parseInt(bookIdParam);

    // ===== STEP 2: Parse request body =====
    const body = await request.json();

    // ===== STEP 3: Update book status =====
    if (body.is_removed === true) {
      await markBookAsRemoved(bookId);
    } else {
      return NextResponse.json(
        {
          error: 'Validation error',
          message: 'Only is_removed=true is supported',
        },
        { status: 400 },
      );
    }

    // ===== STEP 4: Return success response =====
    return NextResponse.json(
      {
        success: true,
        message: 'Book status updated successfully',
      },
      { status: 200 },
    );
  } catch (error) {
    // ===== STEP 5: Handle errors =====
    console.error('Error updating book status:', error);
    return NextResponse.json(
      {
        error: 'Failed to update book status',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}
