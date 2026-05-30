'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Group, Anchor, Menu, Avatar } from '@mantine/core';
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
    <Group
      gap="md"
      role="navigation"
    >
      {canAddBooks && (
        <Anchor
          component={Link}
          href="/books/new"
          underline={pathname === '/books/new' ? 'always' : 'hover'}
        >
          Katalogisieren
        </Anchor>
      )}
      {links.map((link) => {
        const active = pathname === link.href;
        return (
          <Anchor
            key={link.href}
            component={Link}
            href={link.href}
            underline={active ? 'always' : 'hover'}
            aria-current={active ? 'page' : undefined}
          >
            {link.label}
          </Anchor>
        );
      })}
      {status === 'authenticated' ? (
        <Menu>
          <Menu.Target>
            <Avatar style={{ cursor: 'pointer' }}>{getInitial()}</Avatar>
          </Menu.Target>
          <Menu.Dropdown>
            <Menu.Item onClick={handleLogout}>Logout</Menu.Item>
          </Menu.Dropdown>
        </Menu>
      ) : (
        <Anchor
          component={Link}
          href="/login"
          underline={pathname === '/login' ? 'always' : 'hover'}
        >
          Login
        </Anchor>
      )}
    </Group>
  );
}
