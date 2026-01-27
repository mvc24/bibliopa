'use client';
import { AppShell } from '../../components/layout/AppShell';
import {
  Card,
  Title,
  Text,
  Stack,
  Button,
  PasswordInput,
  TextInput,
  Anchor,
} from '@mantine/core';

export default function LoginPage() {
  return (
    <AppShell>
      <Card
        shadow="sm"
        padding="lg"
        maw={480}
      >
        <Stack gap="md">
          <Title order={2}>Login</Title>
          <TextInput
            label="Email"
            placeholder="you@example.com"
            required
          />
          <PasswordInput
            label="Password"
            placeholder="Your password"
            required
          />
          <Button type="submit">Sign in</Button>
          <Text
            size="sm"
            c="dimmed"
          >
            No account? <Anchor href="/account">Create a guest account</Anchor>
          </Text>
        </Stack>
      </Card>
    </AppShell>
  );
}
