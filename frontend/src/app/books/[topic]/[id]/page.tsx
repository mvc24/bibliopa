'use client';
import { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'next/navigation';
import { AppShell } from '@/components/layout/AppShell';
import { Card, Title, Stack, Text, Breadcrumbs, Anchor } from '@mantine/core';
import { BookDetail } from '@/types/database';
import Link from 'next/link';

export default function SingleBookPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const bookId = params.id as string;
  const topic = params.topic as string;
  const page = searchParams.get('page') || '1';
  const [book, setBook] = useState<BookDetail | null>(null);

  useEffect(() => {
    if (bookId) {
      fetch(`/api/books/${bookId}`)
        .then((response) => response.json())
        .then((data) => setBook(data));
    }
  }, [bookId]);

  return (
    <AppShell>
      <Stack gap="md">
        <Breadcrumbs>
          <Anchor
            component={Link}
            href="/"
          >
            Home
          </Anchor>
          <Anchor
            component={Link}
            href={`/books/${topic}?page=${page}`}
          >
            {book?.topic?.topic_name || topic}
          </Anchor>
          {/* <Text>{book?.title || 'Loading...'}</Text> */}
        </Breadcrumbs>
        <Title order={3}>{book?.title}</Title>
        <Text>Diese Seite ist noch nicht fertig.</Text>
        <Card
          shadow="sm"
          padding="lg"
        >
          <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
            {JSON.stringify(book, null, 2)}
          </pre>
        </Card>
      </Stack>
    </AppShell>
  );
}
