import { query, sql } from '@/lib/db';
import { Topic, TopicWithCount } from '@/types/database';

export async function getAllTopics() {
  const result = await query<Topic>(`SELECT * FROM topics`, []);

  return result.rows;
}
