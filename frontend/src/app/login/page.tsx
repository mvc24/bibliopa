'use client';
import { AppShell } from '../../components/layout/AppShell';
import {
  Card,
  Title,
  Stack,
  Button,
  PasswordInput,
  TextInput,
} from '@mantine/core';

import { signIn } from 'next-auth/react';
import { useState } from 'react';

export default function LoginPage() {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const handleLogin = async () => {
    await signIn('credentials', {
      username: username,
      password: password,
      callbackUrl: '/books/all',
    });
  };

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
            label="Benutzername oder E-Mail"
            placeholder="Dein Benutzername ist opa"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.currentTarget.value)}
            required
          />
          <PasswordInput
            label="Passwort"
            placeholder="Gib dein Passwort ein"
            value={password}
            onChange={(e) => setPassword(e.currentTarget.value)}
            required
          />
          <Button onClick={handleLogin}>Einloggen</Button>
        </Stack>
      </Card>
    </AppShell>
  );
}
