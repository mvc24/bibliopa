'use client';
import { useState } from 'react';

export function useAddPrice(onSuccess?: () => void) {
  const [isLoadingPrice, setIsLoadingPrice] = useState(false);

  const addPrice = async (
    bookId: number,
    amount: number | string,
    source?: string,
  ) => {
    setIsLoadingPrice(true);

    try {
      const response = await fetch('/api/prices', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          book_id: bookId,
          amount: typeof amount === 'string' ? parseFloat(amount) : amount,
          source: source || null,
        }),
      });

      if (response.ok) {
        onSuccess?.();
      } else {
        alert('Fehler beim Speichern');
      }
    } catch (error) {
      console.error('Error saving price:', error);
      alert('Fehler beim Speichern');
    } finally {
      setIsLoadingPrice(false);
    }
  };
  return { addPrice, isLoadingPrice };
}
