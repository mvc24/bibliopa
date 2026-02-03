import { Person, BookDetail, AuthorListItem } from '@/types/database';

export function formatPerson(
  person: Person | AuthorListItem | BookDetail['people'][0],
): string {
  if (person.single_name) {
    return person.single_name.toUpperCase();
  }

  const afterComma = [person.given_names, person.name_particles]
    .filter(Boolean)
    .join(' ');

  const familyName = person.family_name?.toUpperCase() || '';

  if (afterComma) {
    return `${familyName}, ${afterComma}`;
  }
  return familyName;
}

export function formatDate(date: Date | string): string {
  return new Date(date).toLocaleDateString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}
