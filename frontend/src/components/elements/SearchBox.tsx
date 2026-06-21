'use client';

import { SearchField, Label, Input, Button } from 'react-aria-components';

// Reusable full-text search box. Owns its own input; calls onSearch on Enter
// (RAC SearchField submit) and onSearch('') when cleared via the × button.
interface SearchBoxProps {
  onSearch: (term: string) => void;
  label?: string;
  placeholder?: string;
  defaultValue?: string;
}

export function SearchBox({
  onSearch,
  label = 'Suche',
  placeholder = 'Volltextsuche',
  defaultValue = '',
}: SearchBoxProps) {
  return (
    <SearchField
      defaultValue={defaultValue}
      onSubmit={onSearch}
      onClear={() => onSearch('')}
      className="search-box"
    >
      <Label>{label}</Label>
      <div className="input-clear-wrap">
        <Input placeholder={placeholder} />
        <Button className="input-clear">×</Button>
      </div>
    </SearchField>
  );
}
