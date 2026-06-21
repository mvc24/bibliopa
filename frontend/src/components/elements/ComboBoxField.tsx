'use client';

import { type KeyboardEvent } from 'react';
import {
  ComboBox,
  Label,
  Input,
  Button,
  Popover,
  ListBox,
  ListBoxItem,
} from 'react-aria-components';
import { startsWithFilterRA } from '@/lib/selectFilters';

interface Item {
  value: string;
  label: string;
}

// Enter-to-select: when the typed text narrows the list to exactly one
// match, Enter picks it (RAC ComboBox doesn't auto-highlight the first
// match). Capture phase + stopPropagation so this runs before RAC's own
// Enter handling — but only when there's a single match. For any other
// count we do nothing and let RAC / the form handle Enter as usual.
export function selectSingleMatch(items: Item[], select: (value: string) => void) {
  return (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key !== 'Enter') return;
    const typed = e.currentTarget.value;
    if (!typed.trim()) return;
    const matches = items.filter((item) =>
      startsWithFilterRA(item.label, typed),
    );
    if (matches.length === 1) {
      e.preventDefault();
      e.stopPropagation();
      select(matches[0].value);
    }
  };
}

interface ComboBoxFieldProps {
  label: string;
  items: Item[];
  placeholder?: string;
  isRequired?: boolean;
  isClearable?: boolean;
  // When the popover opens (RAC `menuTrigger`); defaults to 'input'.
  // 'focus' opens it as soon as the field is focused.
  menuTrigger?: 'focus' | 'input' | 'manual';
  // Enforced-list mode: the value must be one of `items`.
  value?: string | null;
  onChange?: (key: string | null) => void;
  // Free-text mode: `allowsCustomValue` lets the user keep typed text
  // that isn't in `items`.
  inputValue?: string;
  onInputChange?: (value: string) => void;
  allowsCustomValue?: boolean;
}

export function ComboBoxField({
  label,
  items,
  placeholder,
  isRequired,
  isClearable,
  menuTrigger,
  value,
  onChange,
  inputValue,
  onInputChange,
  allowsCustomValue,
}: ComboBoxFieldProps) {
  // Free-text fields hold their value as input text; enforced-list
  // fields as a selected key. Selecting and clearing follow suit.
  const select = allowsCustomValue
    ? (v: string) => onInputChange?.(v)
    : (v: string) => onChange?.(v);

  const clear = allowsCustomValue
    ? () => onInputChange?.('')
    : () => onChange?.(null);

  const hasValue = allowsCustomValue ? !!inputValue : value != null;

  return (
    <ComboBox
      defaultFilter={startsWithFilterRA}
      menuTrigger={menuTrigger}
      value={value}
      onChange={
        allowsCustomValue
          ? undefined
          : (key) => onChange?.(key ? String(key) : null)
      }
      inputValue={inputValue}
      onInputChange={onInputChange}
      allowsCustomValue={allowsCustomValue}
      isRequired={isRequired}
    >
      <Label>{label}</Label>
      <div className="flex items-center gap-1">
        <Input
          placeholder={placeholder}
          onKeyDownCapture={selectSingleMatch(items, select)}
        />
        {isClearable && hasValue && (
          <Button aria-label="Feld leeren" onPress={clear}>
            ×
          </Button>
        )}
      </div>
      <Popover>
        <ListBox items={items}>
          {(item) => (
            <ListBoxItem
              id={item.value}
              textValue={item.label}
            >
              {item.label}
            </ListBoxItem>
          )}
        </ListBox>
      </Popover>
    </ComboBox>
  );
}
