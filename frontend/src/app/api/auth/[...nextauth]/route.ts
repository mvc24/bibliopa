import NextAuth, { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import { compare } from 'bcryptjs';
import { query } from '@/lib/db';
import { User } from '@/types/database';

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        username: { label: 'Username', type: 'text' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.username || !credentials?.password) {
          throw new Error('Please provide both username and password');
        }

        try {
          // Query user from database
          const result = await query<User>(
            'SELECT * FROM users WHERE username = $1 AND is_active = true',
            [credentials.username]
          );

          const user = result.rows[0];

          if (!user) {
            throw new Error('Invalid username or password');
          }

          // Verify password
          const isPasswordValid = await compare(
            credentials.password,
            user.password_hash
          );

          if (!isPasswordValid) {
            throw new Error('Invalid username or password');
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
