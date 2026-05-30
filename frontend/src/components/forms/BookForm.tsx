'use client';

import { useState, useEffect } from 'react';
import {
  TextInput,
  NumberInput,
  Checkbox,
  Select,
  Chip,
  Group,
  Stack,
  Button,
  Text,
  Divider,
} from '@mantine/core';
import { BookDetail, Topic, CreateBookInput } from '@/types/database';
import { FORMAT_BASE, FORMAT_EXTRAS } from '@/components/constants';

interface BookFormProps {
  book?: BookDetail;
  onCancel: () => void;
  onSave: (data: Partial<CreateBookInput>) => void;
}

function parseFormatOriginal(formatOriginal: string | null | undefined) {
  if (!formatOriginal) return { base: null, extras: [] as string[] };
  const base = FORMAT_BASE.find((f) => formatOriginal.startsWith(f.abbrev));
  const extras = FORMAT_EXTRAS.filter((e) =>
    formatOriginal.includes(e.abbrev),
  ).map((e) => e.abbrev);
  return { base: base?.abbrev ?? null, extras };
}

const LANGUAGES = [
  'Deutsch',
  'Englisch',
  'Französisch',
  'Italienisch',
  'Spanisch',
  'Russisch',
  'Latein',
  'Griechisch',
  'Niederländisch',
  'Polnisch',
  'Tschechisch',
  'Schwedisch',
  'Dänisch',
  'Norwegisch',
  'Ungarisch',
];

export function BookForm({ book, onCancel, onSave }: BookFormProps) {
  const parsed = parseFormatOriginal(book?.format_original);

  const [title, setTitle] = useState(book?.title ?? '');
  const [subtitle, setSubtitle] = useState(book?.subtitle ?? '');
  const [publicationYear, setPublicationYear] = useState<number | string>(
    book?.publication_year ?? '',
  );
  const [condition, setCondition] = useState(book?.condition ?? '');
  const [illustrations, setIllustrations] = useState(book?.illustrations ?? '');
  const [packaging, setPackaging] = useState(book?.packaging ?? '');
  const [publisher, setPublisher] = useState(book?.publisher ?? '');
  const [placeOfPublication, setPlaceOfPublication] = useState(
    book?.place_of_publication ?? '',
  );
  const [formatBase, setFormatBase] = useState<string | null>(parsed.base);
  const [formatExtras, setFormatExtras] = useState<string[]>(parsed.extras);
  const [isTranslation, setIsTranslation] = useState(
    book?.is_translation ?? false,
  );
  const [originalLanguage, setOriginalLanguage] = useState<string | null>(
    book?.original_language ?? null,
  );
  const [isMultivolume, setIsMultivolume] = useState(
    book?.is_multivolume ?? false,
  );
  const [topicId, setTopicId] = useState<string | null>(
    book?.topic_id?.toString() ?? null,
  );
  const [topics, setTopics] = useState<Topic[]>([]);

  useEffect(() => {
    fetch('/api/topics')
      .then((r) => r.json())
      .then((result) => {
        if (result.data) setTopics(result.data);
      });
  }, []);

  function assembleFormat() {
    const base = FORMAT_BASE.find((f) => f.abbrev === formatBase);
    if (!base) return { format_original: null, format_expanded: null };

    const extras = FORMAT_EXTRAS.filter((e) => formatExtras.includes(e.abbrev));

    const format_original =
      extras.length > 0
        ? `${base.abbrev}${extras.map((e) => e.abbrev).join(' und ')}`
        : base.abbrev;

    const format_expanded =
      extras.length > 0
        ? `${base.expanded} ${extras.map((e) => e.expanded).join(' ')}`
        : base.expanded;

    return { format_original, format_expanded };
  }

  function handleSubmit() {
    const { format_original, format_expanded } = assembleFormat();

    onSave({
      title,
      subtitle: subtitle || undefined,
      publication_year:
        publicationYear !== '' ? Number(publicationYear) : undefined,
      condition: condition || undefined,
      illustrations: illustrations || undefined,
      packaging: packaging || undefined,
      publisher: publisher || undefined,
      place_of_publication: placeOfPublication || undefined,
      format_original: format_original ?? undefined,
      format_expanded: format_expanded ?? undefined,
      is_translation: isTranslation,
      original_language: originalLanguage ?? undefined,
      is_multivolume: isMultivolume,
      topic_id: topicId ? Number(topicId) : undefined,
    });
  }

  return (
    <Stack gap="md">
      <TextInput
        label="Titel"
        value={title}
        onChange={(e) => setTitle(e.currentTarget.value)}
        required
      />
      <TextInput
        label="Untertitel"
        value={subtitle}
        onChange={(e) => setSubtitle(e.currentTarget.value)}
      />
      <NumberInput
        label="Erscheinungsjahr"
        value={publicationYear}
        onChange={setPublicationYear}
        min={1000}
        max={2100}
        hideControls
      />
      <Select
        label="Thema"
        data={topics.map((t) => ({
          value: t.topic_id.toString(),
          label: t.topic_name,
        }))}
        value={topicId}
        onChange={setTopicId}
      />
      <TextInput
        label="Verlag"
        value={publisher}
        onChange={(e) => setPublisher(e.currentTarget.value)}
      />
      <TextInput
        label="Erscheinungsort"
        value={placeOfPublication}
        onChange={(e) => setPlaceOfPublication(e.currentTarget.value)}
      />

      <div>
        <Text
          fw={500}
          size="sm"
          mb={4}
        >
          Format
        </Text>
        <Select
          placeholder="Format"
          data={FORMAT_BASE.map((f) => ({
            value: f.abbrev,
            label: `${f.abbrev} – ${f.expanded}`,
          }))}
          value={formatBase}
          onChange={setFormatBase}
          mb="xs"
        />
        <Chip.Group
          multiple
          value={formatExtras}
          onChange={setFormatExtras}
        >
          <Group gap="xs">
            {FORMAT_EXTRAS.map((e) => (
              <Chip
                key={e.abbrev}
                value={e.abbrev}
                size="sm"
              >
                {e.label}
              </Chip>
            ))}
          </Group>
        </Chip.Group>
      </div>

      <TextInput
        label="Zustand"
        value={condition}
        onChange={(e) => setCondition(e.currentTarget.value)}
      />
      <TextInput
        label="Illustrationen"
        value={illustrations}
        onChange={(e) => setIllustrations(e.currentTarget.value)}
      />
      <TextInput
        label="Beilagen, besondere Verpackungen, etc."
        value={packaging}
        onChange={(e) => setPackaging(e.currentTarget.value)}
      />

      <Checkbox
        label="Übersetzung"
        checked={isTranslation}
        onChange={(e) => setIsTranslation(e.currentTarget.checked)}
      />
      {isTranslation && (
        <Select
          label="Originalsprache"
          data={LANGUAGES}
          value={originalLanguage}
          onChange={setOriginalLanguage}
          searchable
        />
      )}

      <Checkbox
        label="Mehrbändiges Werk"
        checked={isMultivolume}
        onChange={(e) => setIsMultivolume(e.currentTarget.checked)}
      />

      <Divider />
      <Text
        c="dimmed"
        size="sm"
      >
        Beteiligte Personen – folgt noch
      </Text>

      <Group>
        <Button onClick={handleSubmit}>Speichern</Button>
        <Button
          variant="subtle"
          onClick={onCancel}
        >
          Abbrechen
        </Button>
      </Group>
    </Stack>
  );
}
