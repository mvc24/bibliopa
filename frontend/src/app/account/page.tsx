'use client';
import { AppShell } from '@/components/layout/AppShell';
import { TextField, Label, Input, Button } from 'react-aria-components';
import { useState } from 'react';

export default function AccountPage() {
  const [currentPassword, setCurrentPassword] = useState<string>('');
  const [newPassword, setNewPassword] = useState<string>('');
  const [confirm, setConfirm] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [done, setDone] = useState<boolean>(false);

  const handleSubmit = async () => {
    setError('');
    if (newPassword !== confirm) {
      setError('Die neuen Passwörter stimmen nicht überein.');
      return;
    }
    setSubmitting(true);
    const res = await fetch('/api/auth/change-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ currentPassword, newPassword }),
    });
    setSubmitting(false);

    if (res.ok) {
      setDone(true);
      setCurrentPassword('');
      setNewPassword('');
      setConfirm('');
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
        <form
          className="stack"
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit();
          }}
        >
          <h2 className="page-title">Profil</h2>
          <TextField
            value={currentPassword}
            onChange={setCurrentPassword}
            isRequired
          >
            <Label>Aktuelles Passwort</Label>
            <Input
              type="password"
              placeholder="Dein aktuelles Passwort"
            />
          </TextField>
          <TextField
            value={newPassword}
            onChange={setNewPassword}
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
            <Label>Neues Passwort wiederholen</Label>
            <Input
              type="password"
              placeholder="Neues Passwort erneut eingeben"
            />
          </TextField>
          {error && <p style={{ color: 'crimson' }}>{error}</p>}
          {done && <p style={{ color: 'green' }}>Passwort geändert.</p>}
          <Button
            type="submit"
            isDisabled={submitting}
          >
            {submitting ? 'Wird gespeichert…' : 'Passwort ändern'}
          </Button>
        </form>
      </div>
    </AppShell>
  );
}
