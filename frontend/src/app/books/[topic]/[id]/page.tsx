'use client';
import { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'next/navigation';
import { AppShell } from '@/components/layout/AppShell';
import {
  Card,
  Grid,
  Stack,
  Text,
  Breadcrumbs,
  Anchor,
  Box,
  Table,
  Button,
} from '@mantine/core';
import { BookDetail, BookOverview } from '@/types/database';
import Link from 'next/link';
import { formatPerson } from '@/lib/formatters';
import { ConditionalTableFields } from '@/components/nav/elements/ConditionalTableFields';

export default function SingleBookPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const bookId = params.id as string;
  const topic = params.topic as string;
  const page = searchParams.get('page') || '1';
  const authorId = searchParams.get('author');
  const [book, setBook] = useState<BookDetail | null>(null);
  const [books, setBooks] = useState<BookOverview[]>([]);

  useEffect(() => {
    if (bookId) {
      fetch(`/api/books/${bookId}`)
        .then((response) => response.json())
        .then((data) => setBook(data));
    }
  }, [bookId]);

  const bookData = books.map((book) => ({
    ...book,
    topic_normalised: book.topic_normalised,
    authors: book.people
      .filter((p) => p.is_author)
      .map(formatPerson)
      .join(', '),
    editors: book.people
      .filter((p) => p.is_editor)
      .map(formatPerson)
      .join(', '),
    contributors: book.people
      .filter((p) => p.is_contributor)
      .map(formatPerson)
      .join(', '),
    translator: book.people
      .filter((p) => p.is_translator)
      .map(formatPerson)
      .join(', '),
    mostRecentPrice:
      book.prices
        .filter((pr) => pr.amount)
        .sort(
          (a, b) =>
            new Date(b.date_added).getTime() - new Date(a.date_added).getTime(),
        )[0] || null,
  }));

  return (
    <AppShell>
      <Stack gap="md">
        {/* <Breadcrumbs>
          <Anchor
            component={Link}
            href="/"
          >
            Home
          </Anchor>
          <Anchor
            component={Link}
            href={`/books/${topic}?page=${page}`}
          >
            {book?.topic?.topic_name || topic}
          </Anchor>
          <Text>{book?.title || 'Loading...'}</Text>
        </Breadcrumbs> */}
        <Anchor
          component={Link}
          href={`/books/${topic}?page=${page}${
            authorId ? `&author=${authorId}` : ''
          }#book-${bookId}`}
          style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}
        >
          ← Zurück
        </Anchor>
        {/* <Title order={3}>{book?.title}</Title>
        <Text c="grape">Diese Seite ist noch nicht fertig.</Text>
        <Text size="md">{book?.admin_data?.original_entry}</Text> */}
        <Grid>
          {/* Left column - 2/3 width */}
          <Grid.Col span={8}>
            {/* All your bibliographic info here */}
            <Table withRowBorders={false}>
              <Table.Tbody>
                <ConditionalTableFields
                  label="Titel"
                  value={book?.title}
                />
                <ConditionalTableFields
                  label="Verlag"
                  value={book?.publisher}
                />
              </Table.Tbody>
            </Table>
          </Grid.Col>

          <Grid.Col span={4}>
            <Stack gap="md">
              <Button>Abschreiben</Button>
              <Button>Daten bearbeiten</Button>
            </Stack>
          </Grid.Col>
        </Grid>

        <Box>
          {book?.prices && book.prices.filter((p) => p.amount).length > 0 ? (
            <Stack gap="xs">
              <Text>Preise:</Text>
              {book.prices
                .filter((p) => p.amount)
                .map((price) => (
                  <Text
                    key={price.price_id}
                    size="sm"
                  >
                    € {price.amount}
                    {price.source && ` - ${price.source}`}
                    {' - '}
                    {new Date(price.date_added).toLocaleDateString('de-DE')}
                  </Text>
                ))}
            </Stack>
          ) : (
            <Text>Keine Preise vorhanden</Text>
          )}
        </Box>
        <Card
          shadow="sm"
          padding="lg"
        >
          <pre
            style={{
              fontSize: '8px',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
            }}
          >
            {JSON.stringify(book, null, 2)}
          </pre>
        </Card>
      </Stack>
    </AppShell>
  );
}
