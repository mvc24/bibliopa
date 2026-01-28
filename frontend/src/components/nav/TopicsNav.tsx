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
    <Stack gap="0px">
      {topics.map((topic) => (
        <NavLink
          key={topic.topic_id}
          component={Link}
          href={`/books/${topic.topic_normalised}`}
          label={topic.topic_name}
          variant="subtle"
          active={pathname === `/books/${topic.topic_normalised}`}
        ></NavLink>
      ))}
    </Stack>
  );
}
