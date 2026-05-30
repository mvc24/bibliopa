'use client';

import { useRouter } from 'next/navigation';
import { AppShell } from '@/components/layout/AppShell';
import { Stack, Title } from '@mantine/core';
import { BookForm } from '@/components/forms/BookForm';

export default function NewBookPage() {
  const router = useRouter();

  return (
    <AppShell>
      <Stack gap="md">
        <Title order={3}>Neues Buch</Title>
        <BookForm
          onCancel={() => router.back()}
          onSave={(data) => {
            console.log('Neues Buch:', data);
          }}
        />
      </Stack>
    </AppShell>
  );
}
