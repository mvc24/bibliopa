'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { BookDetail } from '@/types/database';
import { formatPerson, formatDate } from '@/lib/formatters';
import { AppShell } from '../../../components/layout/AppShell';
import {
  Card,
  Title,
  Stack,
  Text,
  Group,
  Badge,
  Collapse,
  Divider,
  Table,
  Button,
  Box,
  Flex,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';

export default function BookPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const [book, setBook] = useState<BookDetail | null>(null);
  const [showPrices, setShowPrices] = useState(false);
  const [showDebugInfo, setShowDebugInfo] = useState(false);
  const [opened, { toggle }] = useDisclosure(false);

  useEffect(() => {
    params.then(({ id }) => {
      fetch(`/api/books/${id}`)
        .then((response) => response.json())
        .then((result) => {
          setBook(result.data);
          setShowPrices(result.permissions?.canViewPrices || false);
          setShowDebugInfo(result.permissions?.canViewDebugInfo || false);
        });
    });
  }, [params]);

  if (!book) {
    return (
      <AppShell>
        <Card
          shadow="sm"
          padding="lg"
        >
          <Text>Lädt...</Text>
        </Card>
      </AppShell>
    );
  }

  // Separate people by role
  const authors = book.people.filter((p) => p.is_author);
  const editors = book.people.filter((p) => p.is_editor);
  const contributors = book.people.filter((p) => p.is_contributor);
  const translators = book.people.filter((p) => p.is_translator);

  return (
    <AppShell>
      <Stack
        gap="xl"
        my="xl"
      >
        <Link
          href="/books"
          style={{ textDecoration: 'none' }}
        >
          <Text c="blue">← Zurück zur Übersicht</Text>
        </Link>

        <Flex
          gap="md"
          justify="flex-start"
          align="flex-start"
          direction="row"
          my="lg"
        >
          {/* Main Book Information */}
          <Card
            shadow="sm"
            padding="lg"
          >
            <Title order={2}>{book.title}</Title>

            {book.subtitle && (
              <Title
                order={3}
                fs="italic"
                fw={500}
              >
                {book.subtitle}
              </Title>
            )}

            {/* Authors */}
            {authors.length > 0 && (
              <Group gap="xs">
                <Text fw={500}>Autor:in:</Text>
                <Text>{authors.map((a) => formatPerson(a))}</Text>
              </Group>
            )}

            {/* Editors */}
            {editors.length > 0 && (
              <Group gap="xs">
                <Text fw={500}>Herausgeber:in:</Text>
                <Text>{editors.map((e) => formatPerson(e))}</Text>
              </Group>
            )}

            {/* Contributors */}
            {contributors.length > 0 && (
              <Group gap="xs">
                <Text fw={500}>Weitere Beteiligte:</Text>
                <Text>{contributors.map((c) => formatPerson(c))}</Text>
              </Group>
            )}

            {translators.length > 0 && (
              <Group gap="xs">
                <Text fw={500}>Übersetzer:in:</Text>
                <Text>{translators.map((t) => formatPerson(t))}</Text>
              </Group>
            )}

            {/* Publication Details */}
            <Group gap="xl">
              {book.publisher && (
                <Group gap="xs">
                  <Text fw={500}>Verlag:</Text>
                  <Text>{book.publisher}</Text>
                </Group>
              )}

              {book.place_of_publication && (
                <Group gap="xs">
                  <Text fw={500}>Ort:</Text>
                  <Text>{book.place_of_publication}</Text>
                </Group>
              )}

              {book.publication_year && (
                <Group gap="xs">
                  <Text fw={500}>Jahr:</Text>
                  <Text>{book.publication_year}</Text>
                </Group>
              )}
            </Group>

            {/* Edition and Pages */}
            <Group gap="xl">
              {book.edition && (
                <Group gap="xs">
                  <Text fw={500}>Auflage:</Text>
                  <Text>{book.edition}</Text>
                </Group>
              )}

              {book.pages && (
                <Group gap="xs">
                  <Text fw={500}>Seiten:</Text>
                  <Text>{book.pages}</Text>
                </Group>
              )}
            </Group>

            {/* ISBN */}
            {book.isbn && (
              <Group gap="xs">
                <Text fw={500}>ISBN:</Text>
                <Text>{book.isbn}</Text>
              </Group>
            )}

            {/* Topic */}
            {book.topic && (
              <Group gap="xs">
                <Text fw={500}>Thema:</Text>
                <Badge
                  variant="light"
                  size="lg"
                >
                  {book.topic.topic_name}
                </Badge>
              </Group>
            )}

            {/* Format and Condition */}
            <Group gap="xl">
              {book.format_expanded && (
                <Group gap="xs">
                  <Text fw={500}>Format:</Text>
                  <Text>{book.format_expanded}</Text>
                </Group>
              )}

              {book.condition && (
                <Group gap="xs">
                  <Text fw={500}>Zustand:</Text>
                  <Text>{book.condition}</Text>
                </Group>
              )}

              {book.copies && book.copies > 1 && (
                <Group gap="xs">
                  <Text fw={500}>Exemplare:</Text>
                  <Text>{book.copies}</Text>
                </Group>
              )}
            </Group>

            {/* Translation Info */}
            {book.is_translation && (
              <Group gap="xs">
                {book.original_language && (
                  <Text size="sm">Original: {book.original_language}</Text>
                )}
              </Group>
            )}

            {/* Multivolume Info */}
            {book.is_multivolume && (
              <Group gap="xs">
                <Text fw={500}>Mehrbändig:</Text>
                {book.series_title && <Text>{book.series_title}</Text>}
                {book.total_volumes && (
                  <Text
                    size="sm"
                    c="dimmed"
                  >
                    ({book.total_volumes} Bände)
                  </Text>
                )}
              </Group>
            )}

            {/* Additional Details */}
            {book.illustrations && (
              <Group gap="xs">
                <Text fw={500}>Illustrationen:</Text>
                <Text>{book.illustrations}</Text>
              </Group>
            )}

            {book.packaging && (
              <Group gap="xs">
                <Text fw={500}>Verpackung:</Text>
                <Text>{book.packaging}</Text>
              </Group>
            )}

            {book.admin_data?.original_entry && (
              <Box>
                <Group>
                  <Button
                    size="compact-sm"
                    onClick={toggle}
                  >
                    Original-Eintrag anzeigen
                  </Button>
                </Group>
                <Collapse in={opened}>
                  <Text
                    size="sm"
                    ff="monospace"
                    style={{ whiteSpace: 'pre-wrap' }}
                  >
                    {book.admin_data.original_entry}
                  </Text>
                </Collapse>
              </Box>
            )}
          </Card>

          {/* Volumes */}
          {book.volumes && book.volumes.length > 0 && (
            <Card
              shadow="sm"
              padding="lg"
            >
              <Title
                order={3}
                mb="md"
              >
                Bände
              </Title>
              <Table>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Band Nr.</Table.Th>
                    <Table.Th>Titel</Table.Th>
                    <Table.Th>Seiten</Table.Th>
                    <Table.Th>Notizen</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {book.volumes.map((volume) => (
                    <Table.Tr key={volume.volume_id}>
                      <Table.Td>{volume.volume_number || '—'}</Table.Td>
                      <Table.Td>{volume.volume_title || '—'}</Table.Td>
                      <Table.Td>{volume.pages || '—'}</Table.Td>
                      <Table.Td>{volume.notes || '—'}</Table.Td>
                    </Table.Tr>
                  ))}
                </Table.Tbody>
              </Table>
            </Card>
          )}

          {/* Debug Information (admin only) */}
          {showDebugInfo && (
            <Card
              shadow="sm"
              padding="lg"
              bg="gray.1"
            >
              <Title
                order={3}
                mb="md"
                c="orange"
              >
                🔧 Debug-Informationen (nur Admin)
              </Title>
              <Stack gap="sm">
                <Group gap="xs">
                  <Text fw={500}>Composite ID:</Text>
                  <Text
                    ff="monospace"
                    size="sm"
                  >
                    {book.composite_id}
                  </Text>
                </Group>

                {/* Person Unified IDs */}
                {book.people.length > 0 && (
                  <Box>
                    <Text
                      fw={500}
                      mb="xs"
                    >
                      Unified IDs (Personen):
                    </Text>
                    <Stack gap="xs">
                      {book.people.map((person) => (
                        <Group
                          key={person.person_id}
                          gap="xs"
                        >
                          <Text size="sm">
                            {person.display_name ||
                              person.family_name ||
                              person.single_name}
                            :
                          </Text>
                          <Text
                            ff="monospace"
                            size="sm"
                            c="dimmed"
                          >
                            {person.unified_id}
                          </Text>
                        </Group>
                      ))}
                    </Stack>
                  </Box>
                )}

                {/* Admin Data */}
                {book.admin_data && (
                  <>
                    <Group gap="xs">
                      <Text fw={500}>Parsing Confidence:</Text>
                      <Badge
                        color={
                          book.admin_data.parsing_confidence === 'high'
                            ? 'green'
                            : book.admin_data.parsing_confidence === 'medium'
                            ? 'yellow'
                            : 'red'
                        }
                      >
                        {book.admin_data.parsing_confidence || 'unknown'}
                      </Badge>
                    </Group>

                    {book.admin_data.needs_review && (
                      <Badge
                        color="red"
                        size="lg"
                      >
                        Benötigt Überprüfung
                      </Badge>
                    )}

                    {book.admin_data.verification_notes && (
                      <Box>
                        <Text fw={500}>Notes:</Text>
                        <Text
                          size="sm"
                          c="dimmed"
                        >
                          {book.admin_data.verification_notes}
                        </Text>
                      </Box>
                    )}
                  </>
                )}
              </Stack>
            </Card>
          )}
        </Flex>

        {/* Prices (only for authorized users) */}
        {showPrices && (
          <Card
            shadow="sm"
            padding="lg"
          >
            <Title
              order={3}
              mb="md"
            >
              Preise
            </Title>
            {book.prices && book.prices.length > 0 ? (
              <>
                <Table>
                  <Table.Thead>
                    <Table.Tr>
                      <Table.Th>Betrag</Table.Th>
                      <Table.Th>Quelle</Table.Th>
                      <Table.Th>Importiert</Table.Th>
                      <Table.Th>Datum</Table.Th>
                    </Table.Tr>
                  </Table.Thead>
                  <Table.Tbody>
                    {book.prices.map((price) => (
                      <Table.Tr key={price.price_id}>
                        <Table.Td>
                          {price.amount
                            ? `€${price.amount.toLocaleString('de-DE', {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2,
                              })}`
                            : '—'}
                        </Table.Td>
                        <Table.Td>{price.source || '—'}</Table.Td>
                        <Table.Td>
                          {price.imported_price ? (
                            <Badge
                              color="blue"
                              size="sm"
                            >
                              Ja
                            </Badge>
                          ) : (
                            <Badge
                              color="gray"
                              size="sm"
                            >
                              Nein
                            </Badge>
                          )}
                        </Table.Td>
                        <Table.Td>{formatDate(price.date_added)}</Table.Td>
                      </Table.Tr>
                    ))}
                  </Table.Tbody>
                </Table>
                <Box mt="md">
                  <Button variant="light">Neuen Preis hinzufügen</Button>
                </Box>
              </>
            ) : (
              <Stack
                align="center"
                gap="md"
              >
                <Text c="dimmed">Keine Preise vorhanden</Text>
                <Button variant="light">Preis hinzufügen</Button>
              </Stack>
            )}
          </Card>
        )}
      </Stack>
    </AppShell>
  );
}
