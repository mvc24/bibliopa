'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { NavLink, Stack } from '@mantine/core';
import { TOPICS } from '../topics';

export function TopicsNav() {
  const pathname = usePathname();

  return (
    <Stack
      gap="0px"
      style={{
        maxHeight: 'calc(100vh - 140px)',
        overflow: 'auto',
      }}
    >
      <NavLink
        component={Link}
        href="/books/all"
        label="Alle Daten"
        variant="subtle"
        active={pathname === 'Alle Daten'}
      ></NavLink>
      {TOPICS.map((topic) => (
        <NavLink
          key={topic.topic_id}
          component={Link}
          href={`/books/${topic.topic_normalised}`}
          label={topic.topic_name}
          variant="Active filled"
          autoContrast
          active={pathname === `/books/${topic.topic_normalised}`}
        ></NavLink>
      ))}
    </Stack>
  );
}
