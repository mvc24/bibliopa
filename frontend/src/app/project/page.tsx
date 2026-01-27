import { AppShell } from "../../components/layout/AppShell";
import { Card, Title, Stack, Text, List } from "@mantine/core";

export default function ProjectPage() {
  return (
    <AppShell>
      <Card shadow="sm" padding="lg">
        <Stack gap="sm">
          <Title order={2}>Project Overview</Title>
          <Text>
            Portfolio-friendly overview of the tech stack, pipelines, and data
            quality processes behind Bibliopa.
          </Text>
          <List type="unordered" spacing="xs">
            <List.Item>
              Backend: FastAPI, PostgreSQL, Alembic migrations
            </List.Item>
            <List.Item>
              ETL & data quality: validation, people normalization, discrepancy
              review flows
            </List.Item>
            <List.Item>
              Frontend: Next.js 15, Mantine, Refine for CRUD and data grids
            </List.Item>
            <List.Item>
              Auth: NextAuth sessions with role-based UI states
            </List.Item>
            <List.Item>
              Exports: PDF/CSV for search results and single entries
            </List.Item>
          </List>
        </Stack>
      </Card>
    </AppShell>
  );
}
