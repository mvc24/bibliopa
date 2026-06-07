// One label/value pair in the book detail description list (<dl>). Renders
// nothing when the value is empty. Arrays are joined with newlines (the
// pre-line keeps those breaks).
export function ConditionalTableFields({
  label,
  value,
}: {
  label: string;
  value?: string | number | null | (string | number)[];
}) {
  if (!value || (Array.isArray(value) && value.length === 0)) return null;

  return (
    <div className="field-row">
      <dt className="field-label">{label}</dt>
      <dd
        className="field-value"
        style={{ whiteSpace: 'pre-line' }}
      >
        {Array.isArray(value) ? value.join('\n') : value}
      </dd>
    </div>
  );
}
