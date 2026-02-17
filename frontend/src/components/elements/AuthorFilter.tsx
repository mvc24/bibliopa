'use client';

import { useState, useEffect } from 'react';
import { Select, ComboboxItem } from '@mantine/core';
import { AuthorListItem } from '@/types/database';
import { formatPerson } from '@/lib/formatters';
import { useRouter } from 'next/navigation';

interface AuthorComboboxItem extends ComboboxItem {
  searchField: string;
}

export function AuthorFilter() {
  const router = useRouter();
  const [authors, setAuthors] = useState<AuthorListItem[]>([]);

  useEffect(() => {
    fetch('/api/authors')
      .then((response) => response.json())
      .then((result) => {
        if (result.data) {
          setAuthors(result.data);
        }
      })
      .catch((error) => {
        console.error('Failed to load authors:', error);
        // authors stays as [] so .map() doesn't break
      });
  }, []);

  return (
    <Select
      size="lg"
      label="Autor:in suchen"
      description="Sobald du einen Namen aus einer Liste anklickst, werden die Ergebnisse auf diese Person eingeschränkt."
      placeholder="Die Suche beginnt nach 3 Buchstaben"
      data={authors.map((author) => ({
        value: author.person_id.toString(),
        label: formatPerson(author),
        searchField: author.family_name || author.single_name || '',
      }))}
      searchable
      nothingFoundMessage="Gib mindestens 3 Buchstaben ein"
      filter={({ options, search }) => {
        const searchLower = search.toLowerCase().trim();
        if (searchLower.length < 3) return [];
        return (options as AuthorComboboxItem[]).filter((option) => {
          const searchField = option.searchField.toLowerCase();
          return searchField.includes(searchLower);
        });
      }}
      onChange={(value) => {
        if (value) {
          router.push(`/books/all?author=${value}`);
        }
      }}
    />
  );
}
