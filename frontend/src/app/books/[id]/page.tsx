'use client';
import { use } from 'react';
import { BookDisplayRow } from '@/types/database';
import { useEffect, useState } from 'react';
import { AppShell } from '../../../components/layout/AppShell';
import {
  Card,
  Title,
  Stack,
  Text,
  TextInput,
  Select,
  Group,
  Button,
  Checkbox,
  Textarea,
} from '@mantine/core';

export default function BookPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params); // use() unwraps the Promise

  const [book, setBook] = useState<BookDisplayRow | null>(null);

  useEffect(() => {
    fetch(`/api/books/${id}`)
      .then((response) => response.json())
      .then((result) => setBook(result.data[0]));
  }, [id]);
  return (
    <AppShell>
      <Stack>
        <Card
          shadow="sm"
          padding="lg"
        >
          <Stack>
            <Title order={2}>Single Book</Title>
          </Stack>
        </Card>
        <Title>Title: {book?.title}</Title>
        {/* {book ? (
          <Card
            shadow="sm"
            padding="lg"
          >
            <Title>{book.title}</Title>
          </Card>
        ) : (
          <Card>
            <Text>Loading ...</Text>
          </Card>
        )} */}
      </Stack>
    </AppShell>
  );
}
