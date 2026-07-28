'use client';
import {
  TextField,
  Label,
  Input,
  Button,
  RadioGroup,
  Radio,
} from 'react-aria-components';
import { useState } from 'react';

export function CreateUserForm() {
  const [username, setUsername] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [role, setRole] = useState<string>('researcher');
  const [error, setError] = useState<string>('');
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [done, setDone] = useState<boolean>(false);

  const handleSubmit = async () => {
    setError('');
    setSubmitting(true);
    const res = await fetch('/api/admin/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, role }),
    });
    setSubmitting(false);

    if (res.ok) {
      setDone(true);
      setUsername('');
      setEmail('');
      setRole('researcher');
    } else {
      const data = await res.json().catch(() => ({}));
      setError(data.error ?? 'Etwas ist schiefgelaufen.');
    }
  };

  return (
    <form
      className="stack"
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit();
      }}
    >
      <h2 className="page-title">Konto anlegen</h2>
      <TextField
        value={username}
        onChange={setUsername}
        isRequired
      >
        <Label>Benutzername</Label>
        <Input
          name="username"
          placeholder="Benutzername"
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
          placeholder="person@email.de"
        />
      </TextField>
      <RadioGroup
        value={role}
        onChange={setRole}
      >
        <Label>Rolle</Label>
        <Radio value="researcher">Forscher</Radio>
        <Radio value="family">Familie</Radio>
        <Radio value="viewer">Betrachter</Radio>
      </RadioGroup>
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      {done && (
        <p style={{ color: 'green' }}>
          Konto angelegt. Die Person bekommt eine E-Mail, um ihr Passwort
          festzulegen.
        </p>
      )}
      <Button
        type="submit"
        isDisabled={submitting}
      >
        {submitting ? 'Wird angelegt…' : 'Konto anlegen und E-Mail senden'}
      </Button>
    </form>
  );
}
