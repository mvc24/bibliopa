'use client';
import { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'next/navigation';

import { BookOverview, PaginationInfo } from '@/types/database';

import { AppShell } from '../../../components/layout/AppShell';
import { Card, Stack, Group } from '@mantine/core';
import { GridList, GridListItem, Button as AriaButton } from 'react-aria-components';
import { formatPerson } from '@/lib/formatters';
import { AuthorFilter } from '@/components/elements/AuthorFilter';
import { SearchBox } from '@/components/elements/SearchBox';
import { useRemoveBook } from '@/lib/hooks/useRemoveBook';
import { PriceDialog } from '@/components/elements/PriceDialog';

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
  const [priceOpen, setPriceOpen] = useState(false);
  const [activeSearch, setActiveSearch] = useState('');

  const handleSearch = (term: string) => {
    if (term.trim()) {
      setActiveSearch(term);
      setCurrentPage(1);
    } else {
      setActiveSearch('');
      setCurrentPage(1);
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
            <SearchBox onSearch={handleSearch} />
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
        <GridList
          aria-label="Bücher"
          className="book-list"
        >
          {bookData.map((book) => {
            const href = `/books/${book.topic_normalised || 'all'}/${
              book.book_id
            }?page=${currentPage}${
              authorId ? `&author=${authorId}` : ''
            }#book-${book.book_id}`;
            return (
              <GridListItem
                key={book.book_id}
                id={book.book_id}
                textValue={book.title}
                href={href}
                className="book-row"
              >
                {/* DOM id stays on an inner element so the detail page's
                    return link (#book-<id>) can still scroll to it — RAC uses
                    GridListItem's own id as the collection key, not a DOM id. */}
                <div
                  id={`book-${book.book_id}`}
                  className="book-entry"
                >
                  <span className="book-authors">{book.authors}</span>
                  <h2 className="book-title">{book.title}</h2>
                  {book.subtitle && (
                    <p className="book-subtitle">{book.subtitle}</p>
                  )}
                  {book.editors && (
                    <p className="book-editors">
                      Herausgegeben von {book.editors}
                    </p>
                  )}
                  <p className="book-publication">
                    {book.publication_year && `${book.publication_year}. `}
                    Verlag/Ort: {book.publisher} : {book.place_of_publication}
                  </p>
                </div>

                {canModify && (
                  <div className="book-actions">
                    {book.mostRecentPrice ? (
                      <AriaButton
                        onPress={() => {
                          setselectedBookId(book.book_id);
                          setPriceOpen(true);
                        }}
                      >
                        € {book.mostRecentPrice.amount}
                      </AriaButton>
                    ) : (
                      <AriaButton
                        onPress={() => {
                          setselectedBookId(book.book_id);
                          setPriceOpen(true);
                        }}
                      >
                        Preis hinzufügen
                      </AriaButton>
                    )}
                    <AriaButton
                      onPress={() => removeBook(book.book_id)}
                      isDisabled={isLoading}
                    >
                      Abschreiben
                    </AriaButton>
                  </div>
                )}
              </GridListItem>
            );
          })}
        </GridList>

        <PriceDialog
          bookId={selectedBookId}
          isOpen={priceOpen}
          onOpenChange={setPriceOpen}
          onSaved={fetchBooks}
        />

        {pagination && pagination.total_pages > 1 && (
          <nav
            className="pagination"
            aria-label="Seiten"
          >
            <AriaButton
              onPress={() => setCurrentPage((p) => Math.max(1, p - 1))}
              isDisabled={currentPage <= 1}
            >
              ← Vorherige
            </AriaButton>
            <span className="pagination-status">
              Seite {currentPage} von {pagination.total_pages}
            </span>
            <AriaButton
              onPress={() =>
                setCurrentPage((p) => Math.min(pagination.total_pages, p + 1))
              }
              isDisabled={currentPage >= pagination.total_pages}
            >
              Nächste →
            </AriaButton>
          </nav>
        )}
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
