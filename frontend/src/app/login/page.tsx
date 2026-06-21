'use client';
import { AppShell } from '../../components/layout/AppShell';
import { TextField, Label, Input, Button } from 'react-aria-components';

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
      <div
        className="panel"
        style={{ maxWidth: 480 }}
      >
        <form
          className="stack"
          onSubmit={(e) => {
            e.preventDefault();
            handleLogin();
          }}
        >
          <h2 className="page-title">Login</h2>
          <TextField
            value={username}
            onChange={setUsername}
            isRequired
          >
            <Label>Benutzername oder E-Mail</Label>
            <Input
              name="username"
              placeholder="Dein Benutzername ist opa"
            />
          </TextField>
          <TextField
            value={password}
            onChange={setPassword}
            isRequired
          >
            <Label>Passwort</Label>
            <Input
              type="password"
              placeholder="Gib dein Passwort ein"
            />
          </TextField>
          <Button type="submit">Einloggen</Button>
        </form>
      </div>
    </AppShell>
  );
}
