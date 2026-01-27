import { AppShell } from "../../../../components/layout/AppShell";
import {
  Card,
  Title,
  Stack,
  TextInput,
  Select,
  Group,
  Button,
  Textarea,
} from "@mantine/core";

export default function EditEntryPage() {
  return (
    <AppShell>
      <Card shadow="sm" padding="lg">
        <Stack gap="md">
          <Title order={2}>Edit Entry</Title>
          <TextInput label="Title" placeholder="Book title" required />
          <Group grow>
            <TextInput label="Author" placeholder="Select or type" />
            <TextInput label="Year" placeholder="1950" />
          </Group>
          <Group grow>
            <TextInput label="Publisher" placeholder="Publisher" />
            <TextInput label="Place" placeholder="Place of publication" />
          </Group>
          <Group grow>
            <Select
              label="Condition"
              data={[{ value: "good", label: "Good" }]}
              placeholder="Select"
            />
            <Select
              label="Binding"
              data={[{ value: "hardcover", label: "Hardcover" }]}
              placeholder="Select"
            />
          </Group>
          <Textarea label="Notes" placeholder="Any notes" minRows={2} />
          <Group justify="flex-end">
            <Button variant="light">Cancel</Button>
            <Button>Save changes</Button>
          </Group>
        </Stack>
      </Card>
    </AppShell>
  );
}
