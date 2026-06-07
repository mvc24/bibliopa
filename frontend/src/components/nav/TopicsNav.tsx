'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { TOPICS } from '../topics';

// The ~50 topics, modelled on his Word documents — his primary index into
// the data. Plain list of links; the sidebar's scroll/collapse lives in
// AppShell.
export function TopicsNav() {
  const pathname = usePathname();

  return (
    <ul className="topics-nav">
      <li>
        <Link
          href="/books/all"
          aria-current={pathname === '/books/all' ? 'page' : undefined}
        >
          Alle Daten
        </Link>
      </li>
      {TOPICS.map((topic) => {
        const href = `/books/${topic.topic_normalised}`;
        return (
          <li key={topic.topic_id}>
            <Link
              href={href}
              aria-current={pathname === href ? 'page' : undefined}
            >
              {topic.topic_name}
            </Link>
          </li>
        );
      })}
    </ul>
  );
}
