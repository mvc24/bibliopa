'use client';
import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';

import { BookDetail, BookDisplayRow, PaginationInfo } from '@/types/database';
import { useRouter } from 'next/navigation';

import { AppShell } from '../../../components/layout/AppShell';
import {
  Card,
  Title,
  Stack,
  TextInput,
  Button,
  Group,
  Table,
  Text,
  Checkbox,
  Pagination,
  MantineColorsTuple,
  createTheme,
} from '@mantine/core';
import { formatPerson } from '@/lib/formatters';

export default function BibliographyPage() {
  const params = useParams();
  const topic = (params.topic as string) || 'all';
  const [books, setBooks] = useState<BookDetail[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo | null>(null);
  const [currentPage, setCurrentPage] = useState(1);

  const router = useRouter();

  useEffect(() => {
    fetch(`/api/books?page=${currentPage}&topic=${topic}`)
      .then((response) => response.json())
      .then((result) => {
        console.log('Books data:', result.data);
        setBooks(result.data);
        setPagination(result.pagination);
      });
  }, [currentPage, topic]);

  const bookData = books.map((book) => ({
    ...book,
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
  }));

  return (
    <AppShell>
      <Stack gap="md">
        <Card
          shadow="sm"
          padding="lg"
        >
          <Stack gap="xs">
            <Title order={2}>Bibliographie</Title>
            <TextInput
              label="Search"
              placeholder="Title, author, keyword"
            />
            <Group gap="m">
              <Button variant="light">Advanced filters</Button>
              <Button>Search</Button>
            </Group>
            {/* <Group gap="m">
              <Button variant="default">Download CSV</Button>
              <Button variant="default">Download PDF</Button>
            </Group> */}
          </Stack>
        </Card>
        <Stack>
          {bookData.map((book) => (
            <Card
              key={book.book_id}
              onClick={() =>
                router.push(
                  `/books/${book.topic?.topic_normalised}/${book.book_id}`,
                )
              }
              style={{ cursor: 'pointer' }}
              shadow="sm"
              padding="md"
            >
              <Group>
                <Group>
                  <Text size="md">{book.authors}</Text>
                </Group>
                <Title
                  order={2}
                  size="md"
                  textWrap="balance"
                  c="#264a46"
                >
                  {book.title}
                </Title>
                <Text
                  size="sm"
                  c="dimmed"
                >
                  {book.subtitle}
                </Text>

                {book.editors && (
                  <Group>
                    <Text size="sm">Herausgegeben von {book.editors}</Text>
                  </Group>
                )}
                <Group>
                  <Text size="sm">
                    {book.publication_year && `${book.publication_year}. `}
                    Verlag/Ort: {book.publisher}/{book.place_of_publication}
                  </Text>
                </Group>
              </Group>
              <Group>
                <Button>Hello</Button>
              </Group>
            </Card>
          ))}
        </Stack>

        <Pagination
          total={pagination?.total_pages || 0}
          value={currentPage}
          onChange={setCurrentPage}
          size="sm"
          radius="md"
          withEdges
        />
      </Stack>
    </AppShell>
  );
}

/* <Table>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Titel</Table.Th>
                <Table.Th>Autor</Table.Th>
                <Table.Th>Erscheinungsjahr</Table.Th>
                {}
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {books.map((book) => (
                <Table.Tr
                  key={book.book_id}
                  onClick={() => router.push(`/books/${book.book_id}`)}
                  style={{ cursor: 'pointer' }}
                >
                  <Table.Td>{book.title}</Table.Td>
                  <Table.Td>
                    {(() => {
                      const author = book.people.find((p) => p.is_author);
                      return author
                        ? author.family_name || author.single_name || ''
                        : '';
                    })()}
                  </Table.Td>
                  <Table.Td>{book.publication_year}</Table.Td>

                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
           */
