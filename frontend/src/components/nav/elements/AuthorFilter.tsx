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
      label="Autor:in suchen"
      placeholder="Tippe den Namen, bis die richtige Person erscheint"
      data={authors.map((author) => ({
        value: author.person_id.toString(),
        label: formatPerson(author),
        searchField: author.family_name || author.single_name || '',
      }))}
      searchable
      filter={({ options, search }) => {
        const searchLower = search.toLowerCase().trim();
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
