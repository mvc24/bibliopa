'use client';
import { AppShell } from '../../../components/layout/AppShell';
import {
  Card,
  Title,
  Stack,
  TextInput,
  Select,
  Group,
  Button,
  Checkbox,
  Textarea,
} from '@mantine/core';

export default function NewEntryPage() {
  return (
    <AppShell>
      <Card
        shadow="sm"
        padding="lg"
      >
        <Stack gap="md">
          <Title order={2}>Create New Entry</Title>
          <TextInput
            label="Title"
            placeholder="Book title"
            required
          />
          <Group grow>
            <TextInput
              label="Author"
              placeholder="Select or type"
            />
            <TextInput
              label="Year"
              placeholder="1950"
            />
          </Group>
          <Group grow>
            <TextInput
              label="Publisher"
              placeholder="Publisher"
            />
            <TextInput
              label="Place"
              placeholder="Place of publication"
            />
          </Group>
          <Group grow>
            <Select
              label="Condition"
              data={[{ value: 'good', label: 'Good' }]}
              placeholder="Select"
            />
            <Select
              label="Binding"
              data={[{ value: 'hardcover', label: 'Hardcover' }]}
              placeholder="Select"
            />
          </Group>
          <Checkbox
            label="Cross-check people info"
            defaultChecked
          />
          <Textarea
            label="Notes"
            placeholder="Any notes"
            minRows={2}
          />
          <Group justify="flex-end">
            <Button variant="light">Cancel</Button>
            <Button>Create entry</Button>
          </Group>
        </Stack>
      </Card>
    </AppShell>
  );
}
