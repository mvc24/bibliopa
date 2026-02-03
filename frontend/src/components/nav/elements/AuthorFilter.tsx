'use client';

import { useState, useEffect } from 'react';
import { Select } from '@mantine/core';
import { AuthorListItem } from '@/types/database';
import { formatPerson } from '@/lib/formatters';
import { useRouter } from 'next/navigation';

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
      placeholder="Tippe die ersten Buchstaben bis die richtige Person erscheint"
      data={authors.map((author) => ({
        value: author.person_id.toString(),
        label: formatPerson(author),
      }))}
      searchable
      onChange={(value) => {
        if (value) {
          router.push(`/books/all?author=${value}`);
        }
      }}
    />
  );
}
