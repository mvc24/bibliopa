'use client';

import {
  AppShell as MantineAppShell,
  AppShellHeader,
  AppShellMain,
  AppShellNavbar,
  Burger,
  Group,
  Title,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { MainNav } from '../nav/MainNav';
import Link from 'next/link';
export function AppShell({ children }: { children: React.ReactNode }) {
  const [mobileOpened, { toggle: toggleMobile }] = useDisclosure();
  const [desktopOpened, { toggle: toggleDesktop }] = useDisclosure(false);

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
        <MainNav />
      </AppShellNavbar>

      <AppShellMain>{children}</AppShellMain>
    </MantineAppShell>
  );
}
