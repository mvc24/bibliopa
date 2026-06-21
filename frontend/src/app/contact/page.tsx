'use client';
import { AppShell } from '../../components/layout/AppShell';
import { TextField, Label, Input, TextArea, Button } from 'react-aria-components';

export default function ContactPage() {
  return (
    <AppShell>
      <div
        className="panel"
        style={{ maxWidth: 540 }}
      >
        <div className="stack">
          <h2 className="page-title">Impressum / Contact</h2>
          <TextField isRequired>
            <Label>Your name</Label>
            <Input placeholder="Name" />
          </TextField>
          <TextField isRequired>
            <Label>Your email</Label>
            <Input
              type="email"
              placeholder="you@example.com"
            />
          </TextField>
          <TextField isRequired>
            <Label>Message</Label>
            <TextArea
              placeholder="How can we help?"
              rows={4}
            />
          </TextField>
          <Button type="submit">Send</Button>
          <p
            style={{
              fontFamily: 'var(--font-sans)',
              fontSize: 'var(--text-sm)',
              color: 'var(--color-muted)',
            }}
          >
            Quick flag button for grandpa will live here as well.
          </p>
        </div>
      </div>
    </AppShell>
  );
}
