'use client';

import {
  AppShell as MantineAppShell,
  AppShellHeader,
  AppShellMain,
  AppShellNavbar,
  Burger,
  Group,
  Title,
  Box,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { MainNav } from '../nav/MainNav';
import { TopicsNav } from '../nav/TopicsNav';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export function AppShell({ children }: { children: React.ReactNode }) {
  const [mobileOpened, { toggle: toggleMobile }] = useDisclosure();
  const [desktopOpened] = useDisclosure(true);
  const pathname = usePathname();
  const isOnBooksPage = pathname.startsWith('/books');

  return (
    <MantineAppShell
      header={{ height: 64 }}
      navbar={{
        width: 260,
        breakpoint: 'sm',
        collapsed: { mobile: !mobileOpened, desktop: !desktopOpened },
      }}
      padding="md"
    >
      <AppShellHeader>
        <Group
          h="100%"
          px="md"
          justify="space-between"
        >
          <Group>
            <Burger
              opened={mobileOpened}
              onClick={toggleMobile}
              hiddenFrom="sm"
              size="sm"
              aria-label="Toggle navigation"
            />
            <Link
              href="/"
              style={{ cursor: 'pointer' }}
            >
              <Title
                order={2}
                fw={700}
              >
                Bibliopa
              </Title>
            </Link>
          </Group>
          <Group visibleFrom="sm">
            <MainNav />
          </Group>
        </Group>
      </AppShellHeader>
      <AppShellNavbar p="md">
        <Box>{isOnBooksPage ? <TopicsNav /> : <MainNav />}</Box>
      </AppShellNavbar>

      <AppShellMain>{children}</AppShellMain>
    </MantineAppShell>
  );
}
