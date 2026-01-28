'use client';
import { useState, useEffect } from 'react';
import { BookDisplayRow, PaginationInfo } from '@/types/database';
import { useRouter } from 'next/navigation';

import { AppShell } from '../../components/layout/AppShell';
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
} from '@mantine/core';
import { TopicsNav } from '@/components/nav/TopicsNav';

export default function BibliographyPage() {
  // const [books, setBooks] = useState<BookWithRelations[]>([]);
  const [books, setBooks] = useState<BookDisplayRow[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo | null>(null);
  const [currentPage, setCurrentPage] = useState(1);

  const router = useRouter();

  useEffect(() => {
    fetch(`/api/books?page=${currentPage}`)
      .then((response) => response.json())
      .then((result) => {
        // console.log('Books data:', result.data);
        setBooks(result.data);
        setPagination(result.pagination);
      });
  }, [currentPage]);
  return (
    <AppShell>
      <Stack gap="md">
        <Card
          shadow="sm"
          padding="lg"
        >
          <Stack gap="xs">
            <Title order={2}>Bibliography</Title>
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
        <Card
          shadow="sm"
          padding="lg"
        >
          <Table>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Titel</Table.Th>
                <Table.Th>Autor</Table.Th>
                <Table.Th>Erscheinungsjahr</Table.Th>
                {/* <Table.Th>Thema</Table.Th> */}
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
                  {/* <Table.Td>{book.topic_name}</Table.Td> */}
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        </Card>
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
