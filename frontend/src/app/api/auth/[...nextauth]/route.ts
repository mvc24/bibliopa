import NextAuth from 'next-auth';

import { authOptions } from '@/lib/authOptions';

const handler = NextAuth(authOptions);

// Export GET and POST handlers for Next.js App Router
export { handler as GET, handler as POST };
