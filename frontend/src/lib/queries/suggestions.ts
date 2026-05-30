import { query, sql } from '@/lib/db';

export async function findPublishers(search: string) {
  const result = await query<{ publisher: string }>(
    sql`
    SELECT DISTINCT publisher
    FROM books
    WHERE publisher ILIKE $1
      AND publisher IS NOT NULL
    ORDER BY publisher
    LIMIT 20
    `,
    [`${search}%`],
  );
  return result.rows;
}

export async function findLanguages() {
  const result = await query<{ original_language: string; count: number }>(
    sql`
    SELECT original_language, COUNT(*) AS count
    FROM books
    WHERE original_language IS NOT NULL
    GROUP BY original_language
    ORDER BY count DESC
    LIMIT 100
    `,
    [],
  );
  return result.rows;
}

export async function findPlaces(publisher: string) {
  const result = await query<{ place_of_publication: string; count: number }>(
    sql`
    SELECT place_of_publication, COUNT(*) AS count
    FROM books
    WHERE publisher = $1
      AND place_of_publication IS NOT NULL
    GROUP BY place_of_publication
    ORDER BY count DESC
    LIMIT 10
    `,
    [publisher],
  );
  return result.rows;
}

export async function getAllPeople() {
  const result = await query<{
    person_id: number;
    family_name: string | null;
    given_names: string | null;
    name_prefix: string | null;
    name_particles: string | null;
    name_suffix: string | null;
    single_name: string | null;
    is_organisation: boolean;
  }>(
    sql`
    SELECT
      person_id,
      family_name,
      given_names,
      name_prefix,
      name_particles,
      name_suffix,
      single_name,
      is_organisation
    FROM people
    ORDER BY COALESCE(family_name, single_name), given_names
    `,
    [],
  );
  return result.rows;
}
