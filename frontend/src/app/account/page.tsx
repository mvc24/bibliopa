'use client';
import { AppShell } from '../../components/layout/AppShell';
import { TextField, Label, Input, Button } from 'react-aria-components';

export default function AccountCreatePage() {
  return (
    <AppShell>
      <div
        className="panel"
        style={{ maxWidth: 520 }}
      >
        <div className="stack">
          <h2 className="page-title">Create Guest Account</h2>
          <TextField isRequired>
            <Label>Full name</Label>
            <Input placeholder="Your name" />
          </TextField>
          <TextField isRequired>
            <Label>Email</Label>
            <Input
              type="email"
              placeholder="you@example.com"
            />
          </TextField>
          <TextField isRequired>
            <Label>Password</Label>
            <Input
              type="password"
              placeholder="Choose a strong password"
            />
          </TextField>
          <Button type="submit">Create account</Button>
          <p
            style={{
              fontFamily: 'var(--font-sans)',
              fontSize: 'var(--text-sm)',
              color: 'var(--color-muted)',
            }}
          >
            Special/family accounts are created by admin only.
          </p>
        </div>
      </div>
    </AppShell>
  );
}
