'use client';
import { AppShell } from '../../../../components/layout/AppShell';
import { TextField, Label, Input, TextArea, Button } from 'react-aria-components';

export default function EditPersonPage() {
  return (
    <AppShell>
      <div className="panel">
        <div className="stack">
          <h2 className="page-title">Edit Person</h2>
          <TextField isRequired>
            <Label>Name</Label>
            <Input placeholder="Full name" />
          </TextField>
          <TextField>
            <Label>Authority record</Label>
            <Input placeholder="Authority ID or URL" />
          </TextField>
          <TextField>
            <Label>Notes</Label>
            <TextArea
              placeholder="Notes"
              rows={2}
            />
          </TextField>
          <Button type="submit">Save person</Button>
        </div>
      </div>
    </AppShell>
  );
}
