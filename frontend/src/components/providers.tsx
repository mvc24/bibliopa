'use client';

import {
  MantineColorsTuple,
  MantineProvider,
  createTheme,
} from '@mantine/core';
import { SessionProvider } from 'next-auth/react';
import '@mantine/core/styles.css';

const myColor: MantineColorsTuple = [
  '#f2f8f7',
  '#e6edec',
  '#c7dbd9',
  '#a5c8c4',
  '#89b8b2',
  '#77aea7',
  '#6ca9a2',
  '#5a948d',
  '#4d847d',
  '#264a46',
];

const theme = createTheme({
  focusRing: 'always',
  // primaryColor: 'green',
  colors: {
    myColor,
  },
  primaryColor: 'myColor',
  defaultRadius: 'md',
  fontFamily:
    'var(--font-geist-sans), system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  // Larger default font sizes for accessibility (90-year-old user)
  fontSizes: {
    xs: '12px',
    sm: '14px',
    md: '16px',
    lg: '20px',
    xl: '24px',
  },
  // Larger default button sizes
  components: {
    Button: {
      defaultProps: {
        size: 'md',
      },
    },
    NavLink: {
      styles: {
        label: {
          fontSize: 'var(--mantine-font-size-md)',
        },
        root: {
          padding: '4px 4px',
        },
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
