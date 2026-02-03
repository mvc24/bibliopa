import { Person, BookDetail, AuthorListItem } from '@/types/database';

export function formatPerson(
  person: Person | AuthorListItem | BookDetail['people'][0],
): string {
  if (person.single_name) {
    return person.single_name.toUpperCase();
  }
  const formattedPerson = [
    person.given_names,
    person.name_particles,
    person.family_name?.toUpperCase(),
  ]
    .filter(Boolean)
    .join(' ');
  return formattedPerson;
}

export function formatDate(date: Date | string): string {
  return new Date(date).toLocaleDateString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}
