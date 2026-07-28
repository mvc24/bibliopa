'use client';
import { AppShell } from '@/components/layout/AppShell';
import { TextField, Label, Input, Button } from 'react-aria-components';
import { useState } from 'react';
import Link from 'next/link';

export default function SignupPage() {
  const [username, setUsername] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [done, setDone] = useState<boolean>(false);

  const handleSignup = async () => {
    setError('');
    setSubmitting(true);
    const res = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password }),
    });
    setSubmitting(false);

    if (res.ok) {
      setDone(true);
    } else {
      const data = await res.json().catch(() => ({}));
      setError(data.error ?? 'Etwas ist schiefgelaufen.');
    }
  };

  return (
    <AppShell>
      <div
        className="panel"
        style={{ maxWidth: 480 }}
      >
        {done ? (
          <div className="stack">
            <h2 className="page-title">Fast geschafft</h2>
            <p>
              Wir haben dir eine E-Mail an <strong>{email}</strong> geschickt.
              Klicke auf den Link darin, um dein Konto zu aktivieren.
            </p>
          </div>
        ) : (
          <form
            className="stack"
            onSubmit={(e) => {
              e.preventDefault();
              handleSignup();
            }}
          >
            <h2 className="page-title">Konto erstellen</h2>
            <TextField
              value={username}
              onChange={setUsername}
              isRequired
            >
              <Label>Benutzername</Label>
              <Input
                name="username"
                placeholder="Wähle einen Benutzernamen"
              />
            </TextField>
            <TextField
              value={email}
              onChange={setEmail}
              isRequired
            >
              <Label>E-Mail</Label>
              <Input
                name="email"
                type="email"
                placeholder="deine@email.de"
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
                placeholder="Mindestens 8 Zeichen"
              />
            </TextField>
            {error && <p style={{ color: 'crimson' }}>{error}</p>}
            <Button
              type="submit"
              isDisabled={submitting}
            >
              {submitting ? 'Wird erstellt…' : 'Konto erstellen'}
            </Button>
            <p style={{ fontSize: 14 }}>
              Schon ein Konto? <Link href="/login">Einloggen</Link>
            </p>
          </form>
        )}
      </div>
    </AppShell>
  );
}
