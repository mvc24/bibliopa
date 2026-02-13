import { Table } from '@mantine/core';

export function ConditionalTableFields({
  label,
  value,
}: {
  label: string;
  value?: string | number | null;
}) {
  if (!value) return null;
  return (
    <Table.Tr>
      <Table.Td
        fw={500}
        w={200}
      >
        {label}
      </Table.Td>
      <Table.Td>{value}</Table.Td>
    </Table.Tr>
  );
}
