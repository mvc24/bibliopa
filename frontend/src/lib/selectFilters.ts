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
export const startsWithFilter: OptionsFilter = ({ options, search }) => {
  const query = search.trim().toLowerCase();
  if (query.length === 0) return options;

  return (options as ComboboxItem[]).filter((option) =>
    option.label.toLowerCase().startsWith(query),
  );
};
