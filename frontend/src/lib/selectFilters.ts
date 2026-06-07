import type { ComboboxItem, OptionsFilter } from '@mantine/core';

/**
 * Lowercase and fold German umlauts to their digraph spelling, so
 * "Aesop" and "Äsop" both become "aesop" (and ß becomes ss). Applied to
 * both the typed query and the option label before comparing.
 */
function normalizeGerman(value: string): string {
  return value
    .toLowerCase()
    .replace(/ä/g, 'ae')
    .replace(/ö/g, 'oe')
    .replace(/ü/g, 'ue')
    .replace(/ß/g, 'ss');
}

/**
 * Mantine Select / Autocomplete filter. Restricts to starts-with matches.
 * Usage: <Select searchable filter={startsWithFilter} ... />
 */
export const startsWithFilter: OptionsFilter = ({ options, search }) => {
  const query = normalizeGerman(search.trim());
  if (query.length === 0) return options;

  return (options as ComboboxItem[]).filter((option) =>
    normalizeGerman(option.label).startsWith(query),
  );
};

/**
 * React Aria ComboBox filter. Called per item; return true = keep.
 * Usage: <ComboBox defaultFilter={startsWithFilterRA} ... />
 */
export function startsWithFilterRA(textValue: string, inputValue: string): boolean {
  const query = normalizeGerman(inputValue.trim());
  if (query.length === 0) return true;
  return normalizeGerman(textValue).startsWith(query);
}
