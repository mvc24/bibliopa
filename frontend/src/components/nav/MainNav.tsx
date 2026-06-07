'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { MenuTrigger, Menu, MenuItem, Popover, Button } from 'react-aria-components';
import { useSession, signOut } from 'next-auth/react';
import { UserRole } from '@/types/database';

const links = [
  { href: '/books', label: 'Bibliographie' },
  { href: '/project', label: 'Projekt' },
  { href: '/contact', label: 'Kontakt' },
];

export function MainNav() {
  const pathname = usePathname();
  const { data: session, status } = useSession();
  const role = (session?.user as { role?: UserRole })?.role;
  const canAddBooks = role === 'admin' || role === 'family';

  const getInitial = () => {
    if (session?.user?.name) {
      return session.user.name[0].toUpperCase();
    }
    if (session?.user?.email) {
      return session.user.email[0].toUpperCase();
    }
    return '?';
  };
  const handleLogout = () => {
    signOut({ callbackUrl: '/' });
  };

  return (
    <nav aria-label="Hauptmenü" className="main-nav">
      {canAddBooks && (
        <Link
          href="/books/new"
          aria-current={pathname === '/books/new' ? 'page' : undefined}
        >
          Katalogisieren
        </Link>
      )}
      {links.map((link) => {
        const active = pathname === link.href;
        return (
          <Link
            key={link.href}
            href={link.href}
            aria-current={active ? 'page' : undefined}
          >
            {link.label}
          </Link>
        );
      })}
      {status === 'authenticated' ? (
        <MenuTrigger>
          <Button aria-label="Konto" className="main-nav-avatar">
            {getInitial()}
          </Button>
          <Popover>
            <Menu>
              <MenuItem onAction={handleLogout}>Logout</MenuItem>
            </Menu>
          </Popover>
        </MenuTrigger>
      ) : (
        <Link
          href="/login"
          aria-current={pathname === '/login' ? 'page' : undefined}
        >
          Login
        </Link>
      )}
    </nav>
  );
}
