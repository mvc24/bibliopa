import { AuthorFilter } from '@/components/elements/AuthorFilter';
import { AppShell } from '../components/layout/AppShell';
import { Card, Stack, Title, Text, Button, Group } from '@mantine/core';

export default function LandingPage() {
  return (
    <AppShell>
      <Stack gap="lg">
        <Card
          shadow="sm"
          padding="lg"
        >
          <Stack gap="sm">
            <AuthorFilter />

            {/* <Group>
              <Button component={Link} href="/bibliography" variant="filled">
                Browse Bibliography
              </Button>
              <Button component={Link} href="/login" variant="light">
                Login / Create Account
              </Button>
            </Group> */}
          </Stack>
        </Card>

        {/* <Card
          shadow="sm"
          padding="lg"
        >
          <Stack>
            <Title order={3}>What you can do</Title>
            <Text>
              - Search, filter, and download bibliography entries (PDF/CSV).
            </Text>
            <Text>- Add, edit, or remove entries with guided forms.</Text>
            <Text>- Track price history with sources and timestamps.</Text>
            <Text>- Flag issues for review and manage authority records.</Text>
          </Stack>
        </Card> */}
      </Stack>
    </AppShell>
  );
}
