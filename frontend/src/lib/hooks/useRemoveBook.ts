'use client';
import { useState } from 'react';

export function useRemoveBook(onSuccess?: () => void) {
  const [isLoading, setIsLoading] = useState(false);

  const removeBook = async (bookId: number) => {
    if (!confirm('Willst du das Buch wirklich aus dem Bestand nehmen?')) {
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`/api/books?id=${bookId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_removed: true }),
      });
      if (response.ok) {
        onSuccess?.();
      } else {
        alert('Fehler beim Abschreiben');
      }
    } catch (error) {
      console.error('Error removing book:', error);
      alert('Fehler beim Abschreiben');
    } finally {
      setIsLoading(false);
    }
  };

  return { removeBook, isLoading };
}
