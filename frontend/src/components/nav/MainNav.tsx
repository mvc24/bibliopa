"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Group, Anchor } from "@mantine/core";

const links = [
  { href: "/", label: "Landing" },
  { href: "/bibliography", label: "Bibliography" },
  { href: "/login", label: "Login" },
  { href: "/project", label: "Project Overview" },
  { href: "/contact", label: "Contact" },
];

export function MainNav() {
  const pathname = usePathname();

  return (
    <Group gap="md" role="navigation">
      {links.map((link) => {
        const active = pathname === link.href;
        return (
          <Anchor
            key={link.href}
            component={Link}
            href={link.href}
            underline={active ? "always" : "hover"}
            aria-current={active ? "page" : undefined}
          >
            {link.label}
          </Anchor>
        );
      })}
    </Group>
  );
}
