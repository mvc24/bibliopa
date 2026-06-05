import {
  Person,
  BookDetail,
  AuthorListItem,
  CreatePersonInput,
} from '@/types/database';

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
  const afterComma = [
    person.name_prefix,
    person.given_names,
    person.name_particles,
    person.name_suffix,
  ]
    .filter(Boolean)
    .join(' ');

  if (afterComma) {
    return `${familyName}, ${afterComma}`;
  }
  return familyName;
}

function removeDiacritics(str: string): string {
  return str
    .replace(/ä/g, 'a')
    .replace(/Ä/g, 'A')
    .replace(/ö/g, 'o')
    .replace(/Ö/g, 'O')
    .replace(/ü/g, 'u')
    .replace(/Ü/g, 'U')
    .replace(/ß/g, 'ss')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

export function generateUnifiedId(person: CreatePersonInput): string {
  const clean = (s: string) =>
    removeDiacritics(s)
      .toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^a-z-]/g, '');

  let base: string;

  if (person.single_name) {
    base = removeDiacritics(person.single_name)
      .toLowerCase()
      .replace(/\s+/g, '_')
      .replace(/[^a-z_]/g, '');
  } else {
    const family = clean(person.family_name ?? '');
    const given = clean(person.given_names ?? '');
    base = given ? `${family}_${given}` : family;
  }

  return `${base}_FE`;
}

export function formatDate(date: Date | string): string {
  return new Date(date).toLocaleDateString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}
