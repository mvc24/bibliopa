'use client';
import { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'next/navigation';

import { BookOverview, PaginationInfo } from '@/types/database';
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
  Kbd,
} from '@mantine/core';
import { formatPerson } from '@/lib/formatters';
import { useDisclosure } from '@mantine/hooks';
import { AuthorFilter } from '@/components/elements/AuthorFilter';
import { useRemoveBook } from '@/lib/hooks/useRemoveBook';
import { useAddPrice } from '@/lib/hooks/useAddPrice';

export default function BibliographyPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const authorParam = searchParams.get('author');
  const authorId = authorParam ? parseInt(authorParam) : null;
  const pageParam = searchParams.get('page');
  const initialPage = pageParam ? parseInt(pageParam) : 1;
  const topic = (params.topic as string) || 'all';
  const [books, setBooks] = useState<BookOverview[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo | null>(null);
  const [currentPage, setCurrentPage] = useState(initialPage);
  const [showPrices, setShowPrices] = useState(false);
  const [canModify, setCanModify] = useState(false);
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

  const fetchBooks = async () => {
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
        console.log('Books data:', result.data);
        console.log('first book topic; ', result.data[0]?.topic);
        // console.log('overview permissions: ', result.permissions);
        setBooks(result.data);
        setPagination(result.pagination);
        setShowPrices(result.permissions?.canViewPrices || false);
        setCanModify(result.permissions?.canModifyBooks || false);
      });
  };

  const { removeBook, isLoading } = useRemoveBook(fetchBooks);
  const { addPrice, isLoadingPrice } = useAddPrice(() => {
    fetchBooks();
    close();
  });
  useEffect(() => {
    fetchBooks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentPage, topic, activeSearch, authorId]);

  useEffect(() => {
    if (books.length > 0 && window.location.hash) {
      const element = document.querySelector(window.location.hash);
      element?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [books]);

  useEffect(() => {
    if (pageParam) {
      setCurrentPage(parseInt(pageParam));
    }
  }, [pageParam]);

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
        <Card
          shadow="sm"
          padding="lg"
        >
          <Stack gap="xs">
            <AuthorFilter />
            <TextInput
              label="Suche"
              placeholder="Volltextsuche"
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
              {/* <Button
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
              )} */}
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
              id={`book-${book.book_id}`}
              onClick={() =>
                router.push(
                  `/books/${book.topic_normalised || 'all'}/${
                    book.book_id
                  }?page=${currentPage}${
                    authorId ? `&author=${authorId}` : ''
                  }#book-${book.book_id}`,
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
                      Verlag/Ort: {book.publisher} : {book.place_of_publication}
                    </Text>
                  </Group>
                </Box>

                {canModify && (
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
                      onClick={(e) => {
                        e.stopPropagation();
                        removeBook(book.book_id);
                      }}
                      loading={isLoading}
                    >
                      Abschreiben
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
          <Text>
            Hier kannst du mit <Kbd>Strg</Kbd> + <Kbd>C</Kbd> die Adresse der
            Website kopieren, auf der du den Preis gefunden hast.
          </Text>
          <Text>
            Du kannst aber auch nur eine Notiz hinzufügen, oder das Feld leer
            lassen.
          </Text>
          <Button
            onClick={(e) => {
              e.stopPropagation();
              if (selectedBookId === null) return;
              addPrice(selectedBookId, priceAmount, priceSource);
            }}
            loading={isLoadingPrice}
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
