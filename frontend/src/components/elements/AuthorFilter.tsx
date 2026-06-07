'use client';

import { useState, useEffect, useMemo } from 'react';
import {
  ComboBox,
  Label,
  Input,
  Text,
  Popover,
  ListBox,
  ListBoxItem,
} from 'react-aria-components';
import { useRouter } from 'next/navigation';
import { AuthorListItem } from '@/types/database';
import { formatPerson } from '@/lib/formatters';
import { startsWithFilterRA } from '@/lib/selectFilters';

// Author search that filters on the surname (not the displayed label) and
// only after 3 characters, since the author list is large. Selecting a name
// navigates to that author's books. Self-contained — drop it in anywhere.
export function AuthorFilter() {
  const router = useRouter();
  const [authors, setAuthors] = useState<AuthorListItem[]>([]);
  const [query, setQuery] = useState('');

  useEffect(() => {
    fetch('/api/authors')
      .then((response) => response.json())
      .then((result) => {
        if (result.data) setAuthors(result.data);
      })
      .catch((error) => {
        console.error('Failed to load authors:', error);
        // authors stays as [] so the list just shows nothing
      });
  }, []);

  const items = useMemo(() => {
    if (query.trim().length < 3) return [];
    return authors
      .filter((author) =>
        startsWithFilterRA(author.family_name || author.single_name || '', query),
      )
      .map((author) => ({
        value: author.person_id.toString(),
        label: formatPerson(author),
      }));
  }, [authors, query]);

  return (
    <ComboBox
      className="author-filter"
      inputValue={query}
      onInputChange={setQuery}
      onChange={(key) => {
        if (key) router.push(`/books/all?author=${key}`);
      }}
      allowsEmptyCollection
    >
      <Label>Autor:in suchen</Label>
      <Input placeholder="Gib mindestens 3 Buchstaben ein, um die Suche zu starten" />
      <Text slot="description">
        Sobald du einen Namen aus einer Liste anklickst, werden die Ergebnisse
        auf diese Person eingeschränkt.
      </Text>
      <Popover>
        <ListBox
          items={items}
          renderEmptyState={() => (
            <div className="author-filter-empty">
              Gib mindestens 3 Buchstaben ein
            </div>
          )}
        >
          {(item) => (
            <ListBoxItem id={item.value} textValue={item.label}>
              {item.label}
            </ListBoxItem>
          )}
        </ListBox>
      </Popover>
    </ComboBox>
  );
}
