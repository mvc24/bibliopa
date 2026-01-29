import { NextRequest, NextResponse } from 'next/server';

import { CreatePriceInput } from '@/types/database';
import { addPriceToBook } from '@/lib/queries/prices';

export async function POST(request: NextRequest) {
  try {
    const body: CreatePriceInput = await request.json();

    if (!body.book_id) {
      return NextResponse.json({ error: 'book_id fehlt!' }, { status: 400 });
    }

    if (!body.amount) {
      return NextResponse.json(
        { error: 'Bitte gib einen Betrag ein!' },
        { status: 400 },
      );
    }

    const newPrice = await addPriceToBook(
      body.book_id,
      body.amount,
      body.source || null,
    );
    return NextResponse.json(
      {
        success: true,
        data: newPrice,
        message: 'Neuer Preis wurde hinzugefügt',
      },
      { status: 201 },
    );
  } catch (error) {
    console.error('Error adding price:', error);
    return NextResponse.json(
      {
        error: 'Failed to add price',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 },
    );
  }
}
