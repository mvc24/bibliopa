'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { NavLink, Stack } from '@mantine/core';
import { Topic } from '@/types/database';
import { useEffect, useState } from 'react';

export function TopicsNav() {
  const [topics, setTopics] = useState<Topic[]>([]);
  const pathname = usePathname();

  useEffect(() => {
    fetch('/api/topics')
      .then((response) => response.json())
      .then((result) => {
        setTopics(result.data);
      });
  }, []);

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
      {topics.map((topic) => (
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
