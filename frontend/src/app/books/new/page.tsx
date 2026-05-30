'use client';

import { useRouter } from 'next/navigation';
import { AppShell } from '@/components/layout/AppShell';
import { Box, Stack, Title } from '@mantine/core';
import { BookForm } from '@/components/forms/BookForm';

export default function NewBookPage() {
  const router = useRouter();

  return (
    <AppShell>
      <Stack gap="md">
        <Title order={3}>Buch katalogisieren</Title>
        <Box maw="80%">
          <BookForm
            onCancel={() => router.back()}
            onSave={(data) => {
              console.log('Neues Buch:', data);
            }}
          />
        </Box>
      </Stack>
    </AppShell>
  );
}
