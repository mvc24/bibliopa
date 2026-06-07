'use client';

import { useEffect, useState } from 'react';
import {
  Modal,
  Dialog,
  Heading,
  NumberField,
  TextField,
  Label,
  Input,
  Button,
} from 'react-aria-components';
import { useAddPrice } from '@/lib/hooks/useAddPrice';

// Shared price-entry dialog used by both the bibliography list and the book
// detail page. Controlled open state lives in the parent; `bookId` is the
// book to price (null = nothing selected), and `onSaved` refetches.
interface PriceDialogProps {
  bookId: number | null;
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  onSaved: () => void;
}

export function PriceDialog({
  bookId,
  isOpen,
  onOpenChange,
  onSaved,
}: PriceDialogProps) {
  const [priceAmount, setPriceAmount] = useState<number | string>('');
  const [priceSource, setPriceSource] = useState('');

  const { addPrice, isLoadingPrice } = useAddPrice(() => {
    onSaved();
    onOpenChange(false);
  });

  // Start fresh each time the dialog opens.
  useEffect(() => {
    if (isOpen) {
      setPriceAmount('');
      setPriceSource('');
    }
  }, [isOpen]);

  return (
    <Modal
      isDismissable
      isOpen={isOpen}
      onOpenChange={onOpenChange}
    >
      <Dialog className="price-dialog">
        <Heading slot="title">Preis hinzufügen</Heading>
        <NumberField
          value={priceAmount === '' ? NaN : Number(priceAmount)}
          onChange={(v) => setPriceAmount(Number.isNaN(v) ? '' : v)}
        >
          <Label>Betrag</Label>
          <Input />
        </NumberField>
        <TextField
          value={priceSource}
          onChange={setPriceSource}
        >
          <Label>Quelle</Label>
          <Input />
        </TextField>
        <p>
          Hier kannst du mit <kbd>Strg</kbd> + <kbd>C</kbd> die Adresse der
          Website kopieren, auf der du den Preis gefunden hast.
        </p>
        <p>
          Du kannst aber auch nur eine Notiz hinzufügen, oder das Feld leer
          lassen.
        </p>
        <Button
          onPress={() => {
            if (bookId === null) return;
            addPrice(bookId, priceAmount, priceSource);
          }}
          isDisabled={isLoadingPrice}
        >
          Speichern
        </Button>
        <Button onPress={() => onOpenChange(false)}>Abbrechen</Button>
      </Dialog>
    </Modal>
  );
}
