import NextAuth, { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import { compare } from 'bcryptjs';

import { getActiveUser } from '@/lib/queries/users';

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        username: { label: 'Username or email', type: 'text' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.username || !credentials?.password) {
          throw new Error('Gib einen Benutzernamen oder ein Passwort ein.');
        }

        try {
          // Query user from database
          const user = await getActiveUser(credentials.username);

          if (!user) {
            throw new Error('Benutzername oder Passwort ist falsch.');
          }

          // console.log('Password from form:', credentials.password);
          // console.log('Hash from database:', user.password_hash);
          // console.log(
          //   'Hash starts with $2b?',
          //   user.password_hash?.startsWith('$2b'),
          // );

          // Verify password
          const isPasswordValid = await compare(
            credentials.password,
            user.password_hash,
          );

          if (!isPasswordValid) {
            throw new Error('Benutzername oder Passwort ist falsch.');
          }

          // Return user object (will be stored in JWT)
          return {
            id: user.user_id,
            name: user.username,
            email: user.email,
            role: user.role,
          };
        } catch (error) {
          console.error('Authorization error:', error);
          throw new Error('Authentication failed');
        }
      },
    }),
  ],

  session: {
    strategy: 'jwt', // Use JWT for sessions (stateless)
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },

  callbacks: {
    // Add custom fields to JWT token
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.role = user.role;
      }
      return token;
    },

    // Add custom fields to session object
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.role = token.role as string;
      }
      return session;
    },
  },

  pages: {
    signIn: '/login', // Custom login page
    error: '/login', // Redirect errors to login page
  },

  secret: process.env.NEXTAUTH_SECRET,

  debug: process.env.NODE_ENV === 'development',
};

const handler = NextAuth(authOptions);

// Export GET and POST handlers for Next.js App Router
export { handler as GET, handler as POST };
