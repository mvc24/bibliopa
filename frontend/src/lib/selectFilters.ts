import type { ComboboxItem, OptionsFilter } from '@mantine/core';

/**
 * Shared filter for Mantine Select / Autocomplete / MultiSelect.
 *
 * Default Mantine behaviour is "contains" (substring). This restricts
 * matches to the START of the option label, which matches how Opa
 * expects a search to behave. Case-insensitive so lowercase typing
 * still finds capitalised names.
 *
 * Usage:  <Select searchable filter={startsWithFilter} ... />
 */
/**
 * Lowercase and fold German umlauts to their digraph spelling, so
 * "Aesop" and "Äsop" both become "aesop" (and ß becomes ss). Applied to
 * both the typed query and the option label before comparing.
 *
 *
 * function normalizeGerman(value: string): string {
  return value
    .toLowerCase()
    .replace(/ä/g, 'ae')
    .replace(/ö/g, 'oe')
    .replace(/ü/g, 'ue')
    .replace(/ß/g, 'ss');
}

export const startsWithFilter: OptionsFilter = ({ options, search }) => {
  const query = normalizeGerman(search.trim());
  if (query.length === 0) return options;

  return (options as ComboboxItem[]).filter((option) =>
    normalizeGerman(option.label).startsWith(query),
  );
};
 */
function normalizeGerman(value: string): string {
  return value
    .toLowerCase()
    .replace(/ä/g, 'ae')
    .replace(/ö/g, 'oe')
    .replace(/ü/g, 'ue')
    .replace(/ß/g, 'ss');
}

export const startsWithFilter: OptionsFilter = ({ options, search }) => {
  const query = normalizeGerman(search.trim());
  if (query.length === 0) return options;

  return (options as ComboboxItem[]).filter((option) =>
    normalizeGerman(option.label).startsWith(query),
  );
};
