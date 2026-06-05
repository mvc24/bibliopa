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
import { TOPICS } from '../topics';
import { FORMAT_BASE, FORMAT_EXTRAS } from '@/components/constants';
import { startsWithFilter } from '@/lib/selectFilters';
import { formatPerson } from '@/lib/formatters';

interface PersonEntry {
  personId: string;
  displayName: string;
}

// One field per person in a role: a Select for the person plus a free-text
// "Abweichende Schreibweise" (books2people.display_name). An always-empty
// Select at the bottom adds another person.
function PersonRolePicker({
  label,
  data,
  selected,
  onChange,
}: {
  label: string;
  data: { value: string; label: string }[];
  selected: PersonEntry[];
  onChange: (entries: PersonEntry[]) => void;
}) {
  function setPersonAt(index: number, value: string | null) {
    const next = [...selected];
    if (value) {
      next[index] = { ...next[index], personId: value };
    } else {
      next.splice(index, 1); // cleared → drop this slot
    }
    onChange(next);
  }

  function setNameAt(index: number, value: string) {
    onChange(
      selected.map((entry, i) =>
        i === index ? { ...entry, displayName: value } : entry,
      ),
    );
  }

  return (
    <Stack gap="xs">
      <Text
        fw={500}
        size="sm"
      >
        {label}
      </Text>
      {selected.map((entry, index) => (
        <Group
          key={index}
          align="flex-end"
          gap="xs"
        >
          <Select
            placeholder="Person suchen"
            data={data}
            value={entry.personId}
            onChange={(value) => setPersonAt(index, value)}
            searchable
            clearable
            filter={startsWithFilter}
            maw={320}
          />
          <TextInput
            label="Alternative Schreibweise"
            value={entry.displayName}
            onChange={(e) => setNameAt(index, e.currentTarget.value)}
            maw={260}
          />
        </Group>
      ))}
      <Select
        key={`add-${selected.length}`}
        placeholder="Person hinzufügen"
        data={data}
        value={null}
        onChange={(value) =>
          value && onChange([...selected, { personId: value, displayName: '' }])
        }
        searchable
        filter={startsWithFilter}
        maw={320}
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

  // one list per role; each entry is a person + their variant spelling
  const [authors, setAuthors] = useState<PersonEntry[]>([]);
  const [editors, setEditors] = useState<PersonEntry[]>([]);
  const [contributors, setContributors] = useState<PersonEntry[]>([]);
  const [translators, setTranslators] = useState<PersonEntry[]>([]);

  // "neue Person anlegen" — shared by both variants
  const [showNewPerson, setShowNewPerson] = useState(false);
  const [newIsOrg, setNewIsOrg] = useState(false);
  const [newGivenNames, setNewGivenNames] = useState('');
  const [newFamilyName, setNewFamilyName] = useState('');
  const [newSingleName, setNewSingleName] = useState('');
  const [newParticles, setNewParticles] = useState('');
  const [newPrefix, setNewPrefix] = useState('');
  const [newSuffix, setNewSuffix] = useState('');
  const [newIsAuthor, setNewIsAuthor] = useState(false);
  const [newIsEditor, setNewIsEditor] = useState(false);
  const [newIsContributor, setNewIsContributor] = useState(false);
  const [newIsTranslator, setNewIsTranslator] = useState(false);

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

    // one entry per person per role; variant spelling → display_name
    const byRole = (entries: PersonEntry[], role: string) =>
      entries.map((entry) => ({
        person_id: Number(entry.personId),
        roles: [role],
        display_name: entry.displayName || undefined,
      }));

    const flat = [
      ...byRole(authors, 'author'),
      ...byRole(editors, 'editor'),
      ...byRole(contributors, 'contributor'),
      ...byRole(translators, 'translator'),
    ];

    // one row per person: union the roles, keep the first non-empty spelling
    const merged = new Map<number, (typeof flat)[number]>();
    for (const entry of flat) {
      const existing = merged.get(entry.person_id);
      if (existing) {
        existing.roles.push(...entry.roles);
        if (!existing.display_name) existing.display_name = entry.display_name;
      } else {
        merged.set(entry.person_id, { ...entry, roles: [...entry.roles] });
      }
    }
    const people = [...merged.values()];

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
        data={TOPICS.map((t) => ({
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
      <Divider
        label="Beteiligte Personen"
        labelPosition="left"
      />

      <Stack gap="md">
        <PersonRolePicker
          label="Verfasser:in"
          data={peopleData}
          selected={authors}
          onChange={setAuthors}
        />
        <PersonRolePicker
          label="Herausgeber:in"
          data={peopleData}
          selected={editors}
          onChange={setEditors}
        />
        <PersonRolePicker
          label="Mitwirkende:r"
          data={peopleData}
          selected={contributors}
          onChange={setContributors}
        />
        <PersonRolePicker
          label="Übersetzer:in"
          data={peopleData}
          selected={translators}
          onChange={setTranslators}
        />
      </Stack>

      <Checkbox
        label="Person nicht gefunden? Neue Person anlegen"
        checked={showNewPerson}
        onChange={(e) => setShowNewPerson(e.currentTarget.checked)}
      />
      {showNewPerson && (
        <Stack gap="sm">
          <Checkbox
            label="Organisation"
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
          <div>
            <Text
              fw={500}
              size="sm"
              mb={4}
            >
              Rolle(n)
            </Text>
            <Group gap="xs">
              <Chip
                checked={newIsAuthor}
                onChange={(v) => setNewIsAuthor(v)}
                size="sm"
              >
                Verfasser:in
              </Chip>
              <Chip
                checked={newIsEditor}
                onChange={(v) => setNewIsEditor(v)}
                size="sm"
              >
                Herausgeber:in
              </Chip>
              <Chip
                checked={newIsContributor}
                onChange={(v) => setNewIsContributor(v)}
                size="sm"
              >
                Mitwirkende:r
              </Chip>
              <Chip
                checked={newIsTranslator}
                onChange={(v) => setNewIsTranslator(v)}
                size="sm"
              >
                Übersetzer:in
              </Chip>
            </Group>
          </div>
        </Stack>
      )}

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
          Erscheinungsform
        </Text>
        <Select
          placeholder="Erscheinungsform"
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
        label="Illustrationen & Abbildungen"
        value={illustrations}
        onChange={(e) => setIllustrations(e.currentTarget.value)}
      />
      <TextInput
        label="Beilagen"
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
