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

export function AppShell({ children }: { children: React.ReactNode }) {
  const [opened, { toggle }] = useDisclosure();

  return (
    <MantineAppShell
      header={{ height: 64 }}
      navbar={{ width: 260, breakpoint: 'sm', collapsed: { mobile: !opened } }}
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
              opened={opened}
              onClick={toggle}
              hiddenFrom="sm"
              size="sm"
              aria-label="Toggle navigation"
            />
            <Title
              order={3}
              fw={700}
            >
              Bibliopa
            </Title>
          </Group>
          <MainNav />
        </Group>
      </AppShellHeader>

      <AppShellNavbar p="md">
        <MainNav />
      </AppShellNavbar>

      <AppShellMain>{children}</AppShellMain>
    </MantineAppShell>
  );
}
