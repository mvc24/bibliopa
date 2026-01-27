"use client";

import { MantineProvider, createTheme } from "@mantine/core";
import { SessionProvider } from "next-auth/react";
import "@mantine/core/styles.css";

const theme = createTheme({
  focusRing: "always",
  primaryColor: "blue",
  defaultRadius: "md",
  fontFamily:
    'var(--font-geist-sans), system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  // Larger default font sizes for accessibility (90-year-old user)
  fontSizes: {
    xs: '14px',
    sm: '16px',
    md: '18px',
    lg: '20px',
    xl: '24px',
  },
  // Larger default button sizes
  components: {
    Button: {
      defaultProps: {
        size: 'lg',
      },
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      <MantineProvider theme={theme}>{children}</MantineProvider>
    </SessionProvider>
  );
}
