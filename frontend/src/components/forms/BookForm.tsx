'use client';

import { type FormEvent, useState, useEffect, useMemo } from 'react';
import {
  Form,
  TextField,
  NumberField,
  Label,
  Input,
  Button,
  Checkbox,
  CheckboxGroup,
} from 'react-aria-components';
import {
  BookDetail,
  Topic,
  CreateBookInput,
  AuthorListItem,
  NewPersonInput,
} from '@/types/database';
import { TOPICS } from '../topics';
import { FORMAT_BASE, FORMAT_EXTRAS } from '@/components/constants';
import { ComboBoxField } from '@/components/elements/ComboBoxField';
import { formatPerson } from '@/lib/formatters';

interface PersonEntry {
  personId: string;
  displayName: string;
}

// Bare-minimum styling only: enough to see and use the controls.
// border = currentColor in Tailwind v4 (no colour value). Real styling
// happens in a later pass.
const inputClass = 'border px-2 py-1';

// A checkbox box + tick, visible without any colour. The tick shows when the
// parent Checkbox is selected (group-data-[selected]).
function CheckboxBox() {
  return (
    <span className="inline-flex w-4 h-4 border items-center justify-center">
      <span className="hidden group-data-[selected]:block">✓</span>
    </span>
  );
}

// One field per person in a role: a ComboBox for the person plus a free-text
// "Abweichende Schreibweise" (books2people.display_name). An always-empty
// ComboBox at the bottom adds another person.
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
      next.splice(index, 1);
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
    <div className="flex flex-col gap-2">
      <span>{label}</span>
      {selected.map((entry, index) => (
        <div
          key={index}
          className="flex gap-2"
        >
          <ComboBoxField
            label="Person"
            placeholder="Person suchen"
            items={data}
            value={entry.personId}
            onChange={(v) => setPersonAt(index, v)}
            menuTrigger="input"
          />
          <TextField
            value={entry.displayName}
            onChange={(v) => setNameAt(index, v)}
          >
            <Label>Alternative Schreibweise</Label>
            <Input className={inputClass} />
          </TextField>
        </div>
      ))}
      <ComboBoxField
        key={`add-${selected.length}`}
        label="Person hinzufügen"
        placeholder="Person hinzufügen"
        items={data}
        value={null}
        onChange={(v) =>
          v && onChange([...selected, { personId: v, displayName: '' }])
        }
        menuTrigger="input"
      />
    </div>
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

  const toEntries = (
    role: 'is_author' | 'is_editor' | 'is_contributor' | 'is_translator',
  ) =>
    book?.people
      .filter((p) => p[role])
      .map((p) => ({
        personId: p.person_id.toString(),
        displayName: p.display_name ?? '',
      })) ?? [];

  const [authors, setAuthors] = useState<PersonEntry[]>(toEntries('is_author'));
  const [editors, setEditors] = useState<PersonEntry[]>(toEntries('is_editor'));
  const [contributors, setContributors] = useState<PersonEntry[]>(
    toEntries('is_contributor'),
  );
  const [translators, setTranslators] = useState<PersonEntry[]>(
    toEntries('is_translator'),
  );

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

  useEffect(() => {
    fetch('/api/suggestions?field=language')
      .then((r) => r.json())
      .then((result) => setLanguageOptions(result.data ?? []));
  }, []);

  useEffect(() => {
    fetch('/api/people')
      .then((r) => r.json())
      .then((result) => setPeople(result.data ?? []));
  }, []);

  useEffect(() => {
    if (publisher.trim().length < 2) {
      setPublisherOptions([]);
      return;
    }
    const timer = setTimeout(() => {
      fetch(
        `/api/suggestions?field=publisher&q=${encodeURIComponent(publisher)}`,
      )
        .then((r) => r.json())
        .then((result) => setPublisherOptions(result.data ?? []));
    }, 300);
    return () => clearTimeout(timer);
  }, [publisher]);

  useEffect(() => {
    if (!publisher) {
      setPlaceOptions([]);
      return;
    }
    const timer = setTimeout(() => {
      fetch(
        `/api/suggestions?field=place&publisher=${encodeURIComponent(publisher)}`,
      )
        .then((r) => r.json())
        .then((result) => setPlaceOptions(result.data ?? []));
    }, 300);
    return () => clearTimeout(timer);
  }, [publisher]);

  const peopleData = useMemo(
    () =>
      people.map((p) => ({
        value: p.person_id.toString(),
        label: formatPerson(p),
      })),
    [people],
  );

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

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const { format_original, format_expanded } = assembleFormat();

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

    const newPeople: NewPersonInput[] = [];
    if (showNewPerson) {
      const hasName = newIsOrg
        ? newSingleName.trim()
        : newFamilyName.trim() || newGivenNames.trim() || newSingleName.trim();
      if (hasName) {
        newPeople.push({
          family_name: newFamilyName || undefined,
          given_names: newGivenNames || undefined,
          name_prefix: newPrefix || undefined,
          name_particles: newParticles || undefined,
          name_suffix: newSuffix || undefined,
          single_name: newSingleName || undefined,
          is_organisation: newIsOrg,
          is_author: newIsAuthor,
          is_editor: newIsEditor,
          is_contributor: newIsContributor,
          is_translator: newIsTranslator,
        });
      }
    }

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
      newPeople: newPeople.length > 0 ? newPeople : undefined,
    });
  }

  const topicItems = TOPICS.map((t) => ({
    value: t.topic_id.toString(),
    label: t.topic_name,
  }));

  const formatBaseItems = FORMAT_BASE.map((f) => ({
    value: f.abbrev,
    label: `${f.abbrev} – ${f.expanded}`,
  }));

  const languageItems = languageOptions.map((l) => ({ value: l, label: l }));
  const publisherItems = publisherOptions.map((p) => ({ value: p, label: p }));
  const placeItems = placeOptions.map((p) => ({ value: p, label: p }));

  return (
    <Form
      onSubmit={handleSubmit}
      className="flex flex-col gap-3"
    >
      {/* Topic */}
      <ComboBoxField
        label="Thema *"
        items={topicItems}
        value={topicId}
        onChange={(v) => setTopicId(v)}
        menuTrigger="focus"
        isRequired
      />

      {/* People */}
      <hr />
      <span>Beteiligte Personen</span>

      <div className="flex flex-col gap-3">
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
      </div>

      {/* New person toggle */}
      <Checkbox
        isSelected={showNewPerson}
        onChange={setShowNewPerson}
        className="group flex items-center gap-2"
      >
        <CheckboxBox />
        Person nicht gefunden? Neue Person anlegen
      </Checkbox>

      {showNewPerson && (
        <div className="flex flex-col gap-3">
          <Checkbox
            isSelected={newIsOrg}
            onChange={setNewIsOrg}
            className="group flex items-center gap-2"
          >
            <CheckboxBox />
            Organisation
          </Checkbox>

          {newIsOrg ? (
            <TextField
              value={newSingleName}
              onChange={setNewSingleName}
            >
              <Label>Bezeichnung</Label>
              <Input className={inputClass} />
            </TextField>
          ) : (
            <>
              <div className="flex gap-2">
                <TextField
                  value={newGivenNames}
                  onChange={setNewGivenNames}
                >
                  <Label>Vorname(n)</Label>
                  <Input className={inputClass} />
                </TextField>
                <TextField
                  value={newFamilyName}
                  onChange={setNewFamilyName}
                >
                  <Label>Nachname</Label>
                  <Input className={inputClass} />
                </TextField>
              </div>
              <div className="flex gap-2">
                <TextField
                  value={newParticles}
                  onChange={setNewParticles}
                >
                  <Label>Namenszusatz (von, de …)</Label>
                  <Input className={inputClass} />
                </TextField>
                <TextField
                  value={newPrefix}
                  onChange={setNewPrefix}
                >
                  <Label>Präfix (Dr., Prof. …)</Label>
                  <Input className={inputClass} />
                </TextField>
                <TextField
                  value={newSuffix}
                  onChange={setNewSuffix}
                >
                  <Label>Suffix (Jr., d. Ä. …)</Label>
                  <Input className={inputClass} />
                </TextField>
              </div>
              <TextField
                value={newSingleName}
                onChange={setNewSingleName}
              >
                <Label>Einzelname (Platon, Sokrates, …)</Label>
                <Input className={inputClass} />
              </TextField>
            </>
          )}

          <div>
            <span>Rolle(n)</span>
            <div className="flex gap-3 flex-wrap">
              {[
                {
                  label: 'Verfasser:in',
                  value: newIsAuthor,
                  set: setNewIsAuthor,
                },
                {
                  label: 'Herausgeber:in',
                  value: newIsEditor,
                  set: setNewIsEditor,
                },
                {
                  label: 'Mitwirkende:r',
                  value: newIsContributor,
                  set: setNewIsContributor,
                },
                {
                  label: 'Übersetzer:in',
                  value: newIsTranslator,
                  set: setNewIsTranslator,
                },
              ].map(({ label, value, set }) => (
                <Checkbox
                  key={label}
                  isSelected={value}
                  onChange={set}
                  className="group flex items-center gap-1.5"
                >
                  <CheckboxBox />
                  {label}
                </Checkbox>
              ))}
            </div>
          </div>
        </div>
      )}

      <hr />

      {/* Core book fields */}
      <TextField
        value={title}
        onChange={setTitle}
        isRequired
      >
        <Label>Titel *</Label>
        <Input className={inputClass} />
      </TextField>

      <TextField
        value={subtitle}
        onChange={setSubtitle}
      >
        <Label>Untertitel</Label>
        <Input className={inputClass} />
      </TextField>

      <NumberField
        value={publicationYear === '' ? NaN : Number(publicationYear)}
        onChange={(v) => setPublicationYear(Number.isNaN(v) ? '' : v)}
        minValue={1000}
        maxValue={2100}
      >
        <Label>Erscheinungsjahr</Label>
        <Input className={inputClass} />
      </NumberField>

      <div className="flex gap-2">
        {/* Publisher — free text allowed */}
        <ComboBoxField
          label="Verlag"
          items={publisherItems}
          inputValue={publisher}
          onInputChange={setPublisher}
          allowsCustomValue
        />

        {/* Place — free text allowed */}
        <ComboBoxField
          label="Erscheinungsort"
          items={placeItems}
          inputValue={placeOfPublication}
          onInputChange={setPlaceOfPublication}
          allowsCustomValue
        />
      </div>

      {/* Format */}
      <div className="flex flex-col gap-2">
        <span>Erscheinungsform</span>
        <ComboBoxField
          label="Erscheinungsform"
          placeholder="Erscheinungsform wählen"
          items={formatBaseItems}
          value={formatBase}
          onChange={(v) => setFormatBase(v)}
          menuTrigger="focus"
        />

        <CheckboxGroup
          value={formatExtras}
          onChange={setFormatExtras}
          className="flex flex-wrap gap-3"
        >
          {FORMAT_EXTRAS.map((e) => (
            <Checkbox
              key={e.abbrev}
              value={e.abbrev}
              className="group flex items-center gap-1.5"
            >
              <CheckboxBox />
              {e.label}
            </Checkbox>
          ))}
        </CheckboxGroup>
      </div>

      <TextField
        value={condition}
        onChange={setCondition}
      >
        <Label>Zustand</Label>
        <Input className={inputClass} />
      </TextField>

      <TextField
        value={illustrations}
        onChange={setIllustrations}
      >
        <Label>Illustrationen & Abbildungen</Label>
        <Input className={inputClass} />
      </TextField>

      <TextField
        value={packaging}
        onChange={setPackaging}
      >
        <Label>Beilagen</Label>
        <Input className={inputClass} />
      </TextField>

      {/* Translation */}
      <Checkbox
        isSelected={isTranslation}
        onChange={setIsTranslation}
        className="group flex items-center gap-2"
      >
        <CheckboxBox />
        Übersetzung
      </Checkbox>

      {isTranslation && (
        <ComboBoxField
          label="Originalsprache"
          items={languageItems}
          inputValue={originalLanguage ?? ''}
          onInputChange={setOriginalLanguage}
          allowsCustomValue
        />
      )}

      {/* Multivolume */}
      <Checkbox
        isSelected={isMultivolume}
        onChange={setIsMultivolume}
        className="group flex items-center gap-2"
      >
        <CheckboxBox />
        Mehrbändiges Werk
      </Checkbox>

      {/* Actions */}
      <div className="flex gap-2">
        <Button
          type="submit"
          className="border px-3 py-1"
        >
          Speichern
        </Button>
        <Button
          type="button"
          onPress={onCancel}
          className="border px-3 py-1"
        >
          Abbrechen
        </Button>
      </div>
    </Form>
  );
}
