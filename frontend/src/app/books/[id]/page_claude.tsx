'use client';
import { useState, useEffect } from 'react';
import { BookDetail } from '@/types/database';
import { AppShell } from '../../../components/layout/AppShell';
import {
  Card,
  Title,
  Stack,
  Text,
  Group,
  Badge,
  Divider,
  Table,
  Button,
  Box,
} from '@mantine/core';

export default function BookPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const [book, setBook] = useState<BookDetail | null>(null);
  const [showPrices, setShowPrices] = useState(false);
  const [showDebugInfo, setShowDebugInfo] = useState(false);

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
      <Stack gap="lg">
        {/* Main Book Information */}
        <Card
          shadow="sm"
          padding="lg"
        >
          <Stack gap="md">
            <Title order={1}>{book.title}</Title>

            {book.subtitle && (
              <Title
                order={3}
                c="dimmed"
                fw={400}
              >
                {book.subtitle}
              </Title>
            )}

            {/* Authors */}
            {authors.length > 0 && (
              <Group gap="xs">
                <Text fw={600}>Autor(en):</Text>
                <Text>
                  {authors
                    .map(
                      (a) => a.display_name || a.family_name || a.single_name,
                    )
                    .join(', ')}
                </Text>
              </Group>
            )}

            {/* Editors */}
            {editors.length > 0 && (
              <Group gap="xs">
                <Text fw={600}>Herausgeber:</Text>
                <Text>
                  {editors
                    .map(
                      (e) => e.display_name || e.family_name || e.single_name,
                    )
                    .join(', ')}
                </Text>
              </Group>
            )}

            {/* Contributors */}
            {contributors.length > 0 && (
              <Group gap="xs">
                <Text fw={600}>Mitwirkende:</Text>
                <Text>
                  {contributors
                    .map(
                      (c) => c.display_name || c.family_name || c.single_name,
                    )
                    .join(', ')}
                </Text>
              </Group>
            )}

            {/* Translators */}
            {translators.length > 0 && (
              <Group gap="xs">
                <Text fw={600}>Übersetzer:</Text>
                <Text>
                  {translators
                    .map(
                      (t) => t.display_name || t.family_name || t.single_name,
                    )
                    .join(', ')}
                </Text>
              </Group>
            )}

            <Divider />

            {/* Publication Details */}
            <Group gap="xl">
              {book.publisher && (
                <Group gap="xs">
                  <Text fw={600}>Verlag:</Text>
                  <Text>{book.publisher}</Text>
                </Group>
              )}

              {book.place_of_publication && (
                <Group gap="xs">
                  <Text fw={600}>Ort:</Text>
                  <Text>{book.place_of_publication}</Text>
                </Group>
              )}

              {book.publication_year && (
                <Group gap="xs">
                  <Text fw={600}>Jahr:</Text>
                  <Text>{book.publication_year}</Text>
                </Group>
              )}
            </Group>

            {/* Edition and Pages */}
            <Group gap="xl">
              {book.edition && (
                <Group gap="xs">
                  <Text fw={600}>Auflage:</Text>
                  <Text>{book.edition}</Text>
                </Group>
              )}

              {book.pages && (
                <Group gap="xs">
                  <Text fw={600}>Seiten:</Text>
                  <Text>{book.pages}</Text>
                </Group>
              )}
            </Group>

            {/* ISBN */}
            {book.isbn && (
              <Group gap="xs">
                <Text fw={600}>ISBN:</Text>
                <Text>{book.isbn}</Text>
              </Group>
            )}

            {/* Topic */}
            {book.topic && (
              <Group gap="xs">
                <Text fw={600}>Thema:</Text>
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
                  <Text fw={600}>Format:</Text>
                  <Text>{book.format_expanded}</Text>
                </Group>
              )}

              {book.condition && (
                <Group gap="xs">
                  <Text fw={600}>Zustand:</Text>
                  <Text>{book.condition}</Text>
                </Group>
              )}

              {book.copies && book.copies > 1 && (
                <Group gap="xs">
                  <Text fw={600}>Exemplare:</Text>
                  <Text>{book.copies}</Text>
                </Group>
              )}
            </Group>

            {/* Translation Info */}
            {book.is_translation && (
              <Group gap="xs">
                <Badge color="blue">Übersetzung</Badge>
                {book.original_language && (
                  <Text size="sm">aus dem {book.original_language}</Text>
                )}
              </Group>
            )}

            {/* Multivolume Info */}
            {book.is_multivolume && (
              <Group gap="xs">
                <Text fw={600}>Mehrbändig:</Text>
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
                <Text fw={600}>Illustrationen:</Text>
                <Text>{book.illustrations}</Text>
              </Group>
            )}

            {book.packaging && (
              <Group gap="xs">
                <Text fw={600}>Verpackung:</Text>
                <Text>{book.packaging}</Text>
              </Group>
            )}
          </Stack>
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
                        <Table.Td>€{price.amount.toFixed(2)}</Table.Td>
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
                        <Table.Td>
                          {new Date(price.date_added).toLocaleDateString(
                            'de-DE',
                          )}
                        </Table.Td>
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
                <Text fw={600}>Composite ID:</Text>
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
                    fw={600}
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
                  <Divider />
                  <Group gap="xs">
                    <Text fw={600}>Parsing Confidence:</Text>
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
                      <Text fw={600}>Verifikationsnotizen:</Text>
                      <Text
                        size="sm"
                        c="dimmed"
                      >
                        {book.admin_data.verification_notes}
                      </Text>
                    </Box>
                  )}

                  <Box>
                    <Text
                      fw={600}
                      mb="xs"
                    >
                      Original-Eintrag:
                    </Text>
                    <Card
                      bg="white"
                      p="xs"
                    >
                      <Text
                        size="sm"
                        ff="monospace"
                        style={{ whiteSpace: 'pre-wrap' }}
                      >
                        {book.admin_data.original_entry}
                      </Text>
                    </Card>
                  </Box>
                </>
              )}
            </Stack>
          </Card>
        )}
      </Stack>
    </AppShell>
  );
}
