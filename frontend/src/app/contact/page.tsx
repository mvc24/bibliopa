'use client';
import { AppShell } from '../../components/layout/AppShell';
import {
  Card,
  Title,
  Stack,
  TextInput,
  Textarea,
  Button,
  Text,
} from '@mantine/core';

export default function ContactPage() {
  return (
    <AppShell>
      <Card
        shadow="sm"
        padding="lg"
        maw={540}
      >
        <Stack gap="md">
          <Title order={2}>Impressum / Contact</Title>
          <TextInput
            label="Your name"
            placeholder="Name"
            required
          />
          <TextInput
            label="Your email"
            placeholder="you@example.com"
            required
          />
          <Textarea
            label="Message"
            placeholder="How can we help?"
            minRows={4}
            required
          />
          <Button type="submit">Send</Button>
          <Text
            size="sm"
            c="dimmed"
          >
            Quick flag button for grandpa will live here as well.
          </Text>
        </Stack>
      </Card>
    </AppShell>
  );
}
