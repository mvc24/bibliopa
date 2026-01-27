'use client';
import { AppShell } from '../../../../components/layout/AppShell';
import {
  Card,
  Title,
  Stack,
  TextInput,
  Button,
  Table,
  Group,
} from '@mantine/core';

export default function EntryPricesPage() {
  return (
    <AppShell>
      <Stack gap="md">
        <Card
          shadow="sm"
          padding="lg"
        >
          <Stack gap="sm">
            <Title order={2}>Add Price</Title>
            <TextInput
              label="Price"
              placeholder="€45"
              required
            />
            <TextInput
              label="Source link"
              placeholder="https://example.com/listing"
              required
            />
            <Button>Add price</Button>
          </Stack>
        </Card>

        <Card
          shadow="sm"
          padding="lg"
        >
          <Title order={3}>Price history</Title>
          <Table>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Date</Table.Th>
                <Table.Th>Price</Table.Th>
                <Table.Th>Source</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              <Table.Tr>
                <Table.Td>2025-01-10</Table.Td>
                <Table.Td>€45</Table.Td>
                <Table.Td>
                  <a href="https://example.com">example.com</a>
                </Table.Td>
              </Table.Tr>
            </Table.Tbody>
          </Table>
        </Card>
      </Stack>
    </AppShell>
  );
}
