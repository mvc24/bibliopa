'use client';
import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { AppShell } from '@/components/layout/AppShell';
import { Card, Title, Stack } from '@mantine/core';

export default function SingleBookPage() {
  const params = useParams();
  const bookId = params.id as string;
  const [book, setBook] = useState<any>(null);

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
        <Title order={1}>Book Details</Title>
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
