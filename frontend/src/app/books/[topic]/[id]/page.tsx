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
import { ConditionalTableFields } from '@/components/elements/ConditionalTableFields';

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

  const mostRecentPrice =
    book?.prices
      .filter((pr) => pr.amount)
      .sort(
        (a, b) =>
          new Date(b.date_added).getTime() - new Date(a.date_added).getTime(),
      )[0] || null;

  const authors = book?.people
    .filter((p) => p.is_author)
    .map((p) => `${formatPerson(p)}`);

  const editors = book?.people
    .filter((p) => p.is_editor)
    .map((p) => `${formatPerson(p)} [Herausgeber:in]`);

  const contributors = book?.people
    .filter((p) => p.is_contributor)
    .map((p) => `${formatPerson(p)} [Mitwirkende:r]`);

  const translator = book?.people
    .filter((p) => p.is_translator)
    .map((p) => `${formatPerson(p)} [Übersetzer:in]`);

  let pages = '';
  if (book?.pages) {
    pages = `${book.pages} S.`;
  }

  const peopleWithRoles =
    book?.people
      .map((p) => {
        let role = '';
        let sortOrder = 5; // default for unknown roles

        if (p.is_author) {
          role = '[Autor:in]';
          sortOrder = 1;
        } else if (p.is_editor) {
          role = '[Herausgeber:in]';
          sortOrder = 2;
        } else if (p.is_contributor) {
          role = '[Mitwirkende:r]';
          sortOrder = 3;
        } else if (p.is_translator) {
          role = '[Übersetzer:in]';
          sortOrder = 4;
        }

        return { name: `${formatPerson(p)} ${role}`, sortOrder };
      })
      .sort((a, b) => a.sortOrder - b.sortOrder)
      .map((item) => item.name) || [];

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
          <Grid.Col span={9}>
            <Table
              withRowBorders={false}
              variant={'vertical'}
              // layout={'fixed'}
            >
              <Table.Tbody>
                <ConditionalTableFields
                  label="Titel"
                  value={
                    book?.title && book?.subtitle
                      ? `${book.title} : ${book.subtitle}`
                      : book?.title
                  }
                />
                <ConditionalTableFields
                  label="Verfasser:in"
                  value={authors}
                />

                <ConditionalTableFields
                  label="Ausgabe"
                  value={book?.edition}
                />

                <ConditionalTableFields
                  label="Erscheinungsjahr"
                  value={book?.publication_year}
                />

                <ConditionalTableFields
                  label="Ort/Verlag"
                  value={
                    book?.place_of_publication && book?.publisher
                      ? `${book.place_of_publication} : ${book.publisher}`
                      : book?.place_of_publication || book?.publisher
                  }
                />
                {/* <ConditionalTableFields
                  label="Umfang/Format"
                  value={
                    pages && book?.format_original
                      ? `${book.pages} S.; ${book.format_original}`
                      : pages || `${book?.format_original}`
                  }
                /> */}

                <ConditionalTableFields
                  label="Umfang/Format"
                  value={[pages, book?.format_original, book?.condition]
                    .filter(Boolean)
                    .join('; ')}
                />

                <ConditionalTableFields
                  label="Illustrationen"
                  value={book?.illustrations}
                />

                <ConditionalTableFields
                  label="Originalsprache"
                  value={book?.original_language}
                />

                <ConditionalTableFields
                  label="Verantwortliche"
                  value={peopleWithRoles}
                />

                {/* <ConditionalTableFields
                  label="Titel"
                  value={book?.title}
                />
                <ConditionalTableFields
                  label="Datensatz Original"
                  value={book?.admin_data?.original_entry}
                />
                */}
                <Table.Tr>
                  <Table.Th
                    fw={700}
                    w={120}
                    style={{
                      verticalAlign: 'top',
                      lineBreak: 'strict',
                      background: 'none',
                    }}
                    fz="lg"
                  >
                    Preise
                  </Table.Th>
                  <Table.Td
                    fz="lg"
                    style={{ whiteSpace: 'pre-line' }}
                  >
                    <Box>
                      {book?.prices &&
                      book.prices.filter((p) => p.amount).length > 0 ? (
                        <Stack gap="xs">
                          {book.prices
                            .filter((p) => p.amount)
                            .map((price) => (
                              <Text key={price.price_id}>
                                € {price.amount}
                                {price.source && ` - ${price.source}`}
                                {' - '}
                                {new Date(price.date_added).toLocaleDateString(
                                  'de-DE',
                                )}
                              </Text>
                            ))}
                        </Stack>
                      ) : (
                        <Text size={'md'}>Keine Preise vorhanden</Text>
                      )}
                    </Box>
                  </Table.Td>
                </Table.Tr>

                <Table.Tr style={{ paddingTop: '100px' }}>
                  <Table.Th
                    fw={700}
                    w={120}
                    style={{
                      verticalAlign: 'top',
                      lineBreak: 'strict',
                    }}
                    fz="sm"
                  >
                    Datensatz Original
                  </Table.Th>
                  <Table.Td
                    fz="sm"
                    style={{ whiteSpace: 'pre-line' }}
                  >
                    {book?.admin_data?.original_entry}
                  </Table.Td>
                </Table.Tr>
              </Table.Tbody>
            </Table>
          </Grid.Col>

          {/* <Grid.Col span={3}>
            <Stack gap="md">
              <Button>Abschreiben</Button>
              <Button>Daten bearbeiten</Button>
            </Stack>
          </Grid.Col> */}
        </Grid>

        {/* <Card
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
        </Card> */}
      </Stack>
    </AppShell>
  );
}
