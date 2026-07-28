'use client';
import { AppShell } from '@/components/layout/AppShell';
import { TextField, Label, Input, Button } from 'react-aria-components';
import { useState } from 'react';
import Link from 'next/link';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState<string>('');
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [done, setDone] = useState<boolean>(false);

  const handleSubmit = async () => {
    setSubmitting(true);
    await fetch('/api/auth/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    setSubmitting(false);
    // Always show the same message, whether or not the email exists.
    setDone(true);
  };

  return (
    <AppShell>
      <div
        className="panel"
        style={{ maxWidth: 480 }}
      >
        {done ? (
          <div className="stack">
            <h2 className="page-title">E-Mail unterwegs</h2>
            <p>
              Falls ein Konto mit dieser Adresse existiert, haben wir dir einen
              Link zum Zurücksetzen deines Passworts geschickt.
            </p>
          </div>
        ) : (
          <form
            className="stack"
            onSubmit={(e) => {
              e.preventDefault();
              handleSubmit();
            }}
          >
            <h2 className="page-title">Passwort vergessen</h2>
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
            <Button
              type="submit"
              isDisabled={submitting}
            >
              {submitting ? 'Wird gesendet…' : 'Link senden'}
            </Button>
            <p style={{ fontSize: 14 }}>
              <Link href="/login">Zurück zum Login</Link>
            </p>
          </form>
        )}
      </div>
    </AppShell>
  );
}
