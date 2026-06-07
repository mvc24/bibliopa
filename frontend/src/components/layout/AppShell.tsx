'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from 'react-aria-components';
import { MainNav } from '../nav/MainNav';
import { TopicsNav } from '../nav/TopicsNav';

// Classless — styling lives in globals.css under the semantic hooks
// (app-shell, app-topbar, app-sidebar, app-main, app-burger…). The sidebar
// holds the ~50 topics (his data index): visible by default, collapsible
// via the burger to give the catalogue full width; the same burger opens
// it on mobile.
export function AppShell({ children }: { children: React.ReactNode }) {
  const [navOpen, setNavOpen] = useState(true);

  return (
    <div className="app-shell">
      <header className="app-topbar">
        <div className="app-topbar-start">
          <Button
            onPress={() => setNavOpen((open) => !open)}
            aria-label="Themen ein- oder ausblenden"
            aria-expanded={navOpen}
            aria-controls="topics-sidebar"
            className="app-burger"
          >
            ☰
          </Button>
          <Link href="/" className="app-brand">
            Bibliopa
          </Link>
        </div>
        <MainNav />
      </header>

      <div className="app-body">
        {navOpen && (
          <nav id="topics-sidebar" aria-label="Themen" className="app-sidebar">
            <TopicsNav />
          </nav>
        )}
        <main className="app-main">{children}</main>
      </div>
    </div>
  );
}
