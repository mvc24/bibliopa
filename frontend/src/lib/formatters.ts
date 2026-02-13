import { Person, BookDetail, AuthorListItem } from '@/types/database';

export function formatPerson(
  person: Person | AuthorListItem | BookDetail['people'][0],
): string {
  if (person.single_name) {
    if (
      person.single_name.toLocaleLowerCase() ===
      person.family_name?.toLocaleLowerCase()
    ) {
      return person.single_name.toUpperCase();
    }
    return person.single_name.toUpperCase();
  }

  const familyName = person.family_name?.toUpperCase() || '';

  if (
    familyName &&
    familyName.toLocaleLowerCase() === person.given_names?.toLocaleLowerCase()
  ) {
    return familyName;
  }

  if (
    person.given_names &&
    !person.family_name &&
    !person.single_name &&
    'is_author' in person &&
    person.is_author
  ) {
    return person.given_names.toUpperCase();
  }
  const afterComma = [person.given_names, person.name_particles]
    .filter(Boolean)
    .join(' ');

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
