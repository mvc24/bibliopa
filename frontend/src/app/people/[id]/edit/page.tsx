import { AppShell } from "../../../../components/layout/AppShell";
import { Card, Title, Stack, TextInput, Button, Textarea } from "@mantine/core";

export default function EditPersonPage() {
  return (
    <AppShell>
      <Card shadow="sm" padding="lg">
        <Stack gap="md">
          <Title order={2}>Edit Person</Title>
          <TextInput label="Name" placeholder="Full name" required />
          <TextInput
            label="Authority record"
            placeholder="Authority ID or URL"
          />
          <Textarea label="Notes" placeholder="Notes" minRows={2} />
          <Button>Save person</Button>
        </Stack>
      </Card>
    </AppShell>
  );
}
