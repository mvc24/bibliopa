'use client';

import { useRouter } from 'next/navigation';
import { AppShell } from '@/components/layout/AppShell';
import { Box, Stack, Title } from '@mantine/core';
import { BookForm } from '@/components/forms/BookForm';
import { TOPICS } from '@/components/topics';

export default function NewBookPage() {
  const router = useRouter();

  return (
    <AppShell>
      <Stack gap="md">
        <Title order={3}>Buch katalogisieren</Title>
        <Box maw="80%">
          <BookForm
            onCancel={() => router.back()}
            onSave={async (data) => {
              const response = await fetch('/api/books', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
              });
              const result = await response.json();
              if (!response.ok) {
                console.error('Speichern fehlgeschlagen:', result.message);
                return;
              }
              const topic = TOPICS.find((t) => t.topic_id === data.topic_id);
              router.push(
                `/books/${topic?.topic_normalised}/${result.data.book_id}`,
              );
            }}
          />
        </Box>
      </Stack>
    </AppShell>
  );
}
