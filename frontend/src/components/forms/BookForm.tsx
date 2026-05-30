'use client';

import { useState, useEffect } from 'react';
import {
  TextInput,
  NumberInput,
  Checkbox,
  Select,
  Autocomplete,
  Chip,
  Group,
  Stack,
  Button,
  Text,
  Divider,
} from '@mantine/core';
import {
  BookDetail,
  Topic,
  CreateBookInput,
  AuthorListItem,
} from '@/types/database';
import { FORMAT_BASE, FORMAT_EXTRAS } from '@/components/constants';
import { startsWithFilter } from '@/lib/selectFilters';
import { formatPerson } from '@/lib/formatters';

// Flip this between 'A' and 'B' to show Opa each layout.
// (A one-line switch instead of commenting blocks out — keeps both
//  sets of fields wired so there are no "unused variable" warnings.)
const PERSON_VARIANT: 'A' | 'B' = 'A';

const ROLES = [
  { value: 'author', label: 'Verfasser:in' },
  { value: 'editor', label: 'Herausgeber:in' },
  { value: 'contributor', label: 'Mitwirkende:r' },
  { value: 'translator', label: 'Übersetzer:in' },
];

interface PersonRow {
  personId: string | null;
  roles: string[];
  displayName: string;
}

// Variant B helper: one role field, each pick is its own single Select,
// with an always-empty Select at the bottom to add another person.
function PersonRolePicker({
  label,
  data,
  selected,
  onChange,
}: {
  label: string;
  data: { value: string; label: string }[];
  selected: string[];
  onChange: (ids: string[]) => void;
}) {
  function setAt(index: number, value: string | null) {
    const next = [...selected];
    if (value) {
      next[index] = value;
    } else {
      next.splice(index, 1); // cleared → drop this slot
    }
    onChange(next);
  }

  return (
    <Stack gap="xs">
      <Text
        fw={500}
        size="sm"
      >
        {label}
      </Text>
      {selected.map((id, index) => (
        <Select
          key={index}
          placeholder="Person suchen"
          data={data}
          value={id}
          onChange={(value) => setAt(index, value)}
          searchable
          clearable
          filter={startsWithFilter}
        />
      ))}
      <Select
        key={`add-${selected.length}`}
        placeholder="Person hinzufügen"
        data={data}
        value={null}
        onChange={(value) => value && onChange([...selected, value])}
        searchable
        filter={startsWithFilter}
      />
    </Stack>
  );
}

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

  const [publisherOptions, setPublisherOptions] = useState<string[]>([]);
  const [placeOptions, setPlaceOptions] = useState<string[]>([]);
  const [languageOptions, setLanguageOptions] = useState<string[]>([]);

  const [people, setPeople] = useState<AuthorListItem[]>([]);

  // Variant A — person first, role beside it
  const [personRows, setPersonRows] = useState<PersonRow[]>([
    { personId: null, roles: [], displayName: '' },
  ]);

  // Variant B — one field per role
  const [authorIds, setAuthorIds] = useState<string[]>([]);
  const [editorIds, setEditorIds] = useState<string[]>([]);
  const [contributorIds, setContributorIds] = useState<string[]>([]);
  const [translatorIds, setTranslatorIds] = useState<string[]>([]);

  // "neue Person anlegen" — shared by both variants
  const [showNewPerson, setShowNewPerson] = useState(false);
  const [newIsOrg, setNewIsOrg] = useState(false);
  const [newGivenNames, setNewGivenNames] = useState('');
  const [newFamilyName, setNewFamilyName] = useState('');
  const [newSingleName, setNewSingleName] = useState('');
  const [newParticles, setNewParticles] = useState('');
  const [newPrefix, setNewPrefix] = useState('');
  const [newSuffix, setNewSuffix] = useState('');

  useEffect(() => {
    fetch('/api/topics')
      .then((r) => r.json())
      .then((result) => {
        if (result.data) setTopics(result.data);
      });
  }, []);

  // language list: loaded once
  useEffect(() => {
    fetch('/api/suggestions?field=language')
      .then((r) => r.json())
      .then((result) => setLanguageOptions(result.data ?? []));
  }, []);

  // people list: loaded once, used by both person variants
  useEffect(() => {
    fetch('/api/people')
      .then((r) => r.json())
      .then((result) => setPeople(result.data ?? []));
  }, []);

  // publisher suggestions: refetch as he types
  useEffect(() => {
    if (publisher.trim().length < 2) {
      setPublisherOptions([]);
      return;
    }
    fetch(`/api/suggestions?field=publisher&q=${encodeURIComponent(publisher)}`)
      .then((r) => r.json())
      .then((result) => setPublisherOptions(result.data ?? []));
  }, [publisher]);

  // place suggestions: based on the chosen publisher
  useEffect(() => {
    if (!publisher) {
      setPlaceOptions([]);
      return;
    }
    fetch(
      `/api/suggestions?field=place&publisher=${encodeURIComponent(publisher)}`,
    )
      .then((r) => r.json())
      .then((result) => setPlaceOptions(result.data ?? []));
  }, [publisher]);

  const peopleData = people.map((p) => ({
    value: p.person_id.toString(),
    label: formatPerson(p),
  }));

  function updateRow(index: number, patch: Partial<PersonRow>) {
    setPersonRows((rows) =>
      rows.map((row, i) => (i === index ? { ...row, ...patch } : row)),
    );
  }

  function addRow() {
    setPersonRows((rows) => [
      ...rows,
      { personId: null, roles: [], displayName: '' },
    ]);
  }

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

    // Variant A: existing people picked by id, with their role(s).
    // (Rows with no person or no role are skipped.)
    const people = personRows
      .filter((row) => row.personId && row.roles.length > 0)
      .map((row) => ({
        person_id: Number(row.personId),
        roles: row.roles,
        display_name: row.displayName || undefined,
      }));

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
      people,
    });
  }

  return (
    <Stack gap="md">
      <Select
        label="Thema"
        data={topics.map((t) => ({
          value: t.topic_id.toString(),
          label: t.topic_name,
        }))}
        value={topicId}
        onChange={setTopicId}
        searchable
        required
        filter={startsWithFilter}
      />
      <Divider labelPosition="left" />
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
        w={100}
      />
      <Group
        grow
        align="flex-start"
      >
        <Autocomplete
          label="Verlag"
          value={publisher}
          onChange={setPublisher}
          data={publisherOptions}
          filter={startsWithFilter}
        />
        <Autocomplete
          label="Erscheinungsort"
          value={placeOfPublication}
          onChange={setPlaceOfPublication}
          data={placeOptions}
          filter={startsWithFilter}
        />
      </Group>

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
        <Autocomplete
          label="Originalsprache"
          data={languageOptions}
          value={originalLanguage ?? ''}
          onChange={setOriginalLanguage}
          filter={startsWithFilter}
        />
      )}

      <Checkbox
        label="Mehrbändiges Werk"
        checked={isMultivolume}
        onChange={(e) => setIsMultivolume(e.currentTarget.checked)}
      />

      <Divider
        label="Beteiligte Personen"
        labelPosition="left"
      />

      {/* VARIANT A — Person zuerst, Rolle daneben */}
      {PERSON_VARIANT === 'A' && (
        <Stack gap="sm">
          {personRows.map((row, index) => (
            <Group
              key={index}
              grow
              align="flex-start"
            >
              <Stack gap="xs">
                <Select
                  label={index === 0 ? 'Person' : undefined}
                  placeholder="Person suchen"
                  data={peopleData}
                  value={row.personId}
                  onChange={(value) => updateRow(index, { personId: value })}
                  searchable
                  filter={startsWithFilter}
                />
                <TextInput
                  label={index === 0 ? 'Abweichende Schreibweise' : undefined}
                  placeholder="wie im Buch gedruckt"
                  value={row.displayName}
                  onChange={(e) =>
                    updateRow(index, { displayName: e.currentTarget.value })
                  }
                />
              </Stack>
              <div>
                {index === 0 && (
                  <Text
                    fw={500}
                    size="sm"
                    mb={4}
                  >
                    Rolle
                  </Text>
                )}
                <Chip.Group
                  multiple
                  value={row.roles}
                  onChange={(value) => updateRow(index, { roles: value })}
                >
                  <Stack gap="xs">
                    {ROLES.map((r) => (
                      <Chip
                        key={r.value}
                        value={r.value}
                        size="sm"
                      >
                        {r.label}
                      </Chip>
                    ))}
                  </Stack>
                </Chip.Group>
              </div>
            </Group>
          ))}
          <Button
            variant="light"
            onClick={addRow}
            style={{ alignSelf: 'flex-start' }}
          >
            + weitere Person
          </Button>
        </Stack>
      )}

      {/* VARIANT B — Rolle zuerst, Personen pro Rolle */}
      {PERSON_VARIANT === 'B' && (
        <Stack gap="md">
          <PersonRolePicker
            label="Verfasser:in"
            data={peopleData}
            selected={authorIds}
            onChange={setAuthorIds}
          />
          <PersonRolePicker
            label="Herausgeber:in"
            data={peopleData}
            selected={editorIds}
            onChange={setEditorIds}
          />
          <PersonRolePicker
            label="Mitwirkende:r"
            data={peopleData}
            selected={contributorIds}
            onChange={setContributorIds}
          />
          <PersonRolePicker
            label="Übersetzer:in"
            data={peopleData}
            selected={translatorIds}
            onChange={setTranslatorIds}
          />
        </Stack>
      )}

      <Checkbox
        label="Person nicht gefunden? Neue Person anlegen"
        checked={showNewPerson}
        onChange={(e) => setShowNewPerson(e.currentTarget.checked)}
      />
      {showNewPerson && (
        <Stack gap="sm">
          <Checkbox
            label="Organisation (keine Einzelperson)"
            checked={newIsOrg}
            onChange={(e) => setNewIsOrg(e.currentTarget.checked)}
          />
          {newIsOrg ? (
            <TextInput
              label="Bezeichnung"
              value={newSingleName}
              onChange={(e) => setNewSingleName(e.currentTarget.value)}
            />
          ) : (
            <>
              <Group grow>
                <TextInput
                  label="Vorname(n)"
                  value={newGivenNames}
                  onChange={(e) => setNewGivenNames(e.currentTarget.value)}
                />
                <TextInput
                  label="Nachname"
                  value={newFamilyName}
                  onChange={(e) => setNewFamilyName(e.currentTarget.value)}
                />
              </Group>
              <Group grow>
                <TextInput
                  label="Namenszusatz (von, de …)"
                  value={newParticles}
                  onChange={(e) => setNewParticles(e.currentTarget.value)}
                />
                <TextInput
                  label="Präfix (Dr., Prof. …)"
                  value={newPrefix}
                  onChange={(e) => setNewPrefix(e.currentTarget.value)}
                />
                <TextInput
                  label="Suffix (Jr., d. Ä. …)"
                  value={newSuffix}
                  onChange={(e) => setNewSuffix(e.currentTarget.value)}
                />
              </Group>
              <TextInput
                label="Einzelname (Platon, Sokrates, …)"
                value={newSingleName}
                onChange={(e) => setNewSingleName(e.currentTarget.value)}
              />
            </>
          )}
        </Stack>
      )}

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
