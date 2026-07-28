import { NextResponse } from 'next/server';
import { z } from 'zod';

import { getUserByEmail } from '@/lib/queries/users';
import { createToken } from '@/lib/tokens';
import { sendResetEmail } from '@/lib/email';

const schema = z.object({ email: z.email() });

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  const parsed = schema.safeParse(body);

  // Always respond OK, even on bad input or unknown email, so this endpoint
  // never reveals which addresses have an account.
  if (!parsed.success) return NextResponse.json({ ok: true });

  const { email } = parsed.data;
  const user = await getUserByEmail(email);

  if (user && user.is_active) {
    const token = createToken(
      user.user_id,
      'set-password',
      user.password_hash, // binding: old reset links die once the password changes
      60, // 1 hour
    );
    const link = `${process.env.NEXTAUTH_URL}/reset-password?token=${token}`;
    await sendResetEmail(email, link);

    if (process.env.NODE_ENV !== 'production') {
      console.log('[reset link]', link);
    }
  }

  return NextResponse.json({ ok: true });
}
