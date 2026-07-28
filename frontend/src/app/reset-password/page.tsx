'use client';
import { AppShell } from '@/components/layout/AppShell';
import { TextField, Label, Input, Button } from 'react-aria-components';
import { Suspense, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

function ResetInner() {
  const token = useSearchParams().get('token');
  const router = useRouter();
  const [password, setPassword] = useState<string>('');
  const [confirm, setConfirm] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [done, setDone] = useState<boolean>(false);

  const handleSubmit = async () => {
    setError('');
    if (password !== confirm) {
      setError('Die Passwörter stimmen nicht überein.');
      return;
    }
    setSubmitting(true);
    const res = await fetch('/api/auth/reset-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, password }),
    });
    setSubmitting(false);

    if (res.ok) {
      setDone(true);
    } else {
      const data = await res.json().catch(() => ({}));
      setError(data.error ?? 'Etwas ist schiefgelaufen.');
    }
  };

  if (done) {
    return (
      <div className="stack">
        <h2 className="page-title">Passwort gespeichert</h2>
        <p>Du kannst dich jetzt mit deinem neuen Passwort anmelden.</p>
        <Button onPress={() => router.push('/login')}>Zum Login</Button>
      </div>
    );
  }

  return (
    <form
      className="stack"
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit();
      }}
    >
      <h2 className="page-title">Passwort festlegen</h2>
      <TextField
        value={password}
        onChange={setPassword}
        isRequired
      >
        <Label>Neues Passwort</Label>
        <Input
          type="password"
          placeholder="Mindestens 8 Zeichen"
        />
      </TextField>
      <TextField
        value={confirm}
        onChange={setConfirm}
        isRequired
      >
        <Label>Passwort wiederholen</Label>
        <Input
          type="password"
          placeholder="Passwort erneut eingeben"
        />
      </TextField>
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      <Button
        type="submit"
        isDisabled={submitting}
      >
        {submitting ? 'Wird gespeichert…' : 'Passwort speichern'}
      </Button>
    </form>
  );
}

export default function ResetPasswordPage() {
  return (
    <AppShell>
      <div
        className="panel"
        style={{ maxWidth: 480 }}
      >
        <Suspense fallback={<p>Wird geladen…</p>}>
          <ResetInner />
        </Suspense>
      </div>
    </AppShell>
  );
}
