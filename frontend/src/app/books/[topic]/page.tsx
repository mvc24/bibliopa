'use client';
import { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'next/navigation';

import { BookDetail, PaginationInfo } from '@/types/database';
import { useRouter } from 'next/navigation';

import { AppShell } from '../../../components/layout/AppShell';
import {
  Card,
  Title,
  Stack,
  TextInput,
  Button,
  Group,
  Modal,
  NumberInput,
  Text,
  Pagination,
  Box,
} from '@mantine/core';
import { formatPerson } from '@/lib/formatters';
import { useDisclosure } from '@mantine/hooks';
import { AuthorFilter } from '@/components/nav/elements/AuthorFilter';

export default function BibliographyPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const authorParam = searchParams.get('author');
  const authorId = authorParam ? parseInt(authorParam) : null;
  const topic = (params.topic as string) || 'all';
  const [books, setBooks] = useState<BookDetail[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [showPrices, setShowPrices] = useState(false);
  const [selectedBookId, setselectedBookId] = useState<number | null>(null);
  const [priceAmount, setPriceAmount] = useState<number | string>('');
  const [priceSource, setPriceSource] = useState('');
  const [opened, { open, close }] = useDisclosure(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeSearch, setActiveSearch] = useState('');
  const router = useRouter();

  const handleSearch = () => {
    if (searchTerm.trim()) {
      setActiveSearch(searchTerm);
      setCurrentPage(1);
    } else {
      setActiveSearch('');
    }
  };

  useEffect(() => {
    const url = activeSearch
      ? `/api/books?page=${currentPage}&search=${encodeURIComponent(
          activeSearch,
        )}`
      : authorId
      ? `/api/books?page=${currentPage}&author=${authorId}`
      : `/api/books?page=${currentPage}&topic=${topic}`;

    fetch(url)
      .then((response) => response.json())
      .then((result) => {
        // console.log('Books data:', result.data);
        // console.log('first book topic; ', result.data[0]?.topic);
        setBooks(result.data);
        setPagination(result.pagination);
        setShowPrices(result.permissions?.canViewPrices || false);
      });
  }, [currentPage, topic, activeSearch, authorId]);

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
        <Card
          shadow="sm"
          padding="lg"
        >
          <Stack gap="xs">
            <Title order={2}>Bibliographie</Title>
            <AuthorFilter />
            <TextInput
              label="Suche"
              placeholder="Titel oder Personen"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.currentTarget.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleSearch();
                }
              }}
            />
            <Group gap="m">
              {/* <Button variant="light">Advanced filters</Button> */}
              <Button
                size="sm"
                onClick={handleSearch}
              >
                Suchen
              </Button>
              {activeSearch && (
                <Button
                  variant="subtle"
                  onClick={() => {
                    setActiveSearch('');
                    setSearchTerm('');
                    setCurrentPage(1);
                  }}
                >
                  Clear search
                </Button>
              )}
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
                  `/books/${book.topic?.topic_normalised}/${book.book_id}?page=${currentPage}`,
                )
              }
              style={{ cursor: 'pointer' }}
              shadow="sm"
              padding="md"
            >
              <Group
                justify="space-between"
                align="flex-start"
              >
                <Box style={{ flex: 2 }}>
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
                </Box>

                {showPrices && (
                  <Box
                    style={{
                      flex: 1,
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'flex-end',
                      gap: '8px',
                    }}
                  >
                    {book.mostRecentPrice ? (
                      <Button
                        variant="light"
                        radius="xl"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          setselectedBookId(book.book_id);
                          open();
                        }}
                      >
                        € {book.mostRecentPrice.amount}
                      </Button>
                    ) : (
                      <Button
                        radius="xl"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          setselectedBookId(book.book_id);
                          open();
                        }}
                      >
                        Preis hinzufügen
                      </Button>
                    )}
                    <Button
                      size="sm"
                      variant="light"
                      onClick={async (e) => {
                        e.stopPropagation();

                        if (
                          !confirm(
                            'Willst du das Buch wirklich aus dem Bestand nehmen?',
                          )
                        ) {
                          return;
                        }

                        try {
                          const response = await fetch(
                            `/api/books?id=${book.book_id}`,
                            {
                              method: 'PATCH',
                              headers: { 'Content-Type': 'application/json' },
                              body: JSON.stringify({ is_removed: true }),
                            },
                          );

                          if (response.ok) {
                            // Refresh the books list
                            const url = activeSearch
                              ? `/api/books?page=${currentPage}&search=${encodeURIComponent(
                                  activeSearch,
                                )}`
                              : `/api/books?page=${currentPage}&topic=${topic}`;

                            const result = await fetch(url).then((r) =>
                              r.json(),
                            );
                            setBooks(result.data);
                          } else {
                            alert('Fehler beim Entfernen');
                          }
                        } catch (error) {
                          console.error('Error removing book:', error);
                          alert('Fehler beim Entfernen');
                        }
                      }}
                    >
                      Buch entfernen
                    </Button>
                  </Box>
                )}
              </Group>
            </Card>
          ))}
        </Stack>

        <Modal
          opened={opened}
          onClose={close}
        >
          <NumberInput
            label="Betrag"
            placeholder="Euro"
            value={priceAmount}
            onChange={setPriceAmount}
            // error="Bitte gib einen Betrag ein oder mach das Fenster mit 'ESC' (Taste links oben auf der Tastatur) zu."
            required
            hideControls
          ></NumberInput>
          <TextInput
            label="Quelle"
            placeholder="Quelle"
            value={priceSource}
            onChange={(e) => setPriceSource(e.currentTarget.value)}
          ></TextInput>
          <Button
            my="lg"
            size="sm"
            onClick={async () => {
              if (!selectedBookId || !priceAmount) {
                alert(
                  'Bitte gib einen Betrag ein oder mach das Fenster mit ESC (Taste links oben auf der Tastatur) zu.',
                );
                return;
              }

              try {
                const response = await fetch('/api/prices', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    book_id: selectedBookId,
                    amount:
                      typeof priceAmount === 'string'
                        ? parseFloat(priceAmount)
                        : priceAmount,
                    source: priceSource || null,
                  }),
                });

                if (response.ok) {
                  close();
                  setPriceAmount('');
                  setPriceSource('');
                  // Refresh the books list
                  const result = await fetch(
                    `/api/books?page=${currentPage}&topic=${topic}`,
                  ).then((r) => r.json());
                  setBooks(result.data);
                } else {
                  alert('Fehler beim Speichern');
                }
              } catch (error) {
                console.error('Error saving price:', error);
                alert('Fehler beim Speichern');
              }
            }}
          >
            Speichern
          </Button>
        </Modal>
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
