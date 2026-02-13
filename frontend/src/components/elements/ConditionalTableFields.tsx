import { Table } from '@mantine/core';

export function ConditionalTableFields({
  label,
  value,
}: {
  label: string;
  value?: string | number | null | (string | number)[];
}) {
  if (!value || (Array.isArray(value) && value.length === 0)) return null;

  return (
    <Table.Tr>
      <Table.Td
        fw={700}
        w={120}
        style={{ verticalAlign: 'top', lineBreak: 'strict' }}
        fz="lg"
      >
        {label}
      </Table.Td>
      <Table.Td
        fz="lg"
        style={{ whiteSpace: 'pre-line' }}
      >
        {Array.isArray(value) ? value.join('\n') : value}
      </Table.Td>
    </Table.Tr>
  );
}
