import { AppShell } from "../../components/layout/AppShell";
import {
  Card,
  Title,
  Stack,
  TextInput,
  PasswordInput,
  Button,
  Text,
} from "@mantine/core";

export default function AccountCreatePage() {
  return (
    <AppShell>
      <Card shadow="sm" padding="lg" maw={520}>
        <Stack gap="md">
          <Title order={2}>Create Guest Account</Title>
          <TextInput label="Full name" placeholder="Your name" required />
          <TextInput label="Email" placeholder="you@example.com" required />
          <PasswordInput
            label="Password"
            placeholder="Choose a strong password"
            required
          />
          <Button type="submit">Create account</Button>
          <Text size="sm" c="dimmed">
            Special/family accounts are created by admin only.
          </Text>
        </Stack>
      </Card>
    </AppShell>
  );
}
