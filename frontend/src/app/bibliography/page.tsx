'use client';
import { AppShell } from '../../components/layout/AppShell';
import {
  Card,
  Title,
  Stack,
  TextInput,
  Button,
  Group,
  Table,
  Text,
  Checkbox,
} from '@mantine/core';

export default function BibliographyPage() {
  return (
    <AppShell>
      <Stack gap="md">
        <Card
          shadow="sm"
          padding="lg"
        >
          <Stack gap="xs">
            <Title order={2}>Bibliography</Title>
            <TextInput
              label="Search"
              placeholder="Title, author, keyword"
            />
            <Group gap="sm">
              <Checkbox label="Show prices (special/family)" />
              <Button variant="light">Advanced filters</Button>
              <Button>Search</Button>
            </Group>
            <Group gap="sm">
              <Button variant="default">Download CSV</Button>
              <Button variant="default">Download PDF</Button>
            </Group>
          </Stack>
        </Card>

        <Card
          shadow="sm"
          padding="lg"
        >
          <Table>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Title</Table.Th>
                <Table.Th>Author</Table.Th>
                <Table.Th>Year</Table.Th>
                <Table.Th>Actions</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              <Table.Tr>
                <Table.Td>Sample book</Table.Td>
                <Table.Td>Person Example</Table.Td>
                <Table.Td>1950</Table.Td>
                <Table.Td>
                  <Group gap="xs">
                    <Button
                      size="xs"
                      variant="subtle"
                    >
                      View
                    </Button>
                    <Button
                      size="xs"
                      variant="subtle"
                      color="green"
                    >
                      Add price
                    </Button>
                    <Button
                      size="xs"
                      variant="subtle"
                      color="yellow"
                    >
                      Edit
                    </Button>
                  </Group>
                </Table.Td>
              </Table.Tr>
            </Table.Tbody>
          </Table>
        </Card>
      </Stack>
    </AppShell>
  );
}
