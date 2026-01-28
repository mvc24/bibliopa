import { query, sql } from '@/lib/db';
import { Topic, TopicWithCount } from '@/types/database';

export async function getAllTopics() {
  const result = await query<Topic>(
    sql`
  SELECT * FROM topics
  ORDER by topic_name
  `,
    [],
  );

  return result.rows;
}
