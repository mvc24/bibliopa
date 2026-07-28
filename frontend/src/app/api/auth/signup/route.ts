import { NextResponse } from 'next/server';
import { hash } from 'bcryptjs';
import { z } from 'zod';

import { createUser } from '@/lib/queries/users';
import { createToken } from '@/lib/tokens';
import { sendVerifyEmail } from '@/lib/email';

const schema = z.object({
  username: z.string().trim().min(1, 'Bitte gib einen Benutzernamen ein.'),
  email: z.email('Bitte gib eine gültige E-Mail-Adresse ein.'),
  password: z.string().min(8, 'Das Passwort muss mindestens 8 Zeichen lang sein.'),
});

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: parsed.error.issues[0].message },
      { status: 400 },
    );
  }

  const { username, email, password } = parsed.data;

  try {
    const password_hash = await hash(password, 10);
    // New viewer starts inactive; the verify-email link flips is_active to true.
    const user = await createUser(username, email, password_hash, 'viewer');

    const token = createToken(
      user.user_id,
      'verify-email',
      String(user.is_active),
      60 * 24, // 24 hours
    );
    const link = `${process.env.NEXTAUTH_URL}/verify-email?token=${token}`;
    await sendVerifyEmail(email, link);

    if (process.env.NODE_ENV !== 'production') {
      console.log('[verify-email link]', link);
    }

    return NextResponse.json({ ok: true });
  } catch (err) {
    // 23505 = Postgres unique_violation (username or email already taken)
    if ((err as { code?: string }).code === '23505') {
      return NextResponse.json(
        { error: 'Benutzername oder E-Mail ist bereits vergeben.' },
        { status: 409 },
      );
    }
    console.error('Signup error:', err);
    return NextResponse.json(
      { error: 'Konto konnte nicht erstellt werden.' },
      { status: 500 },
    );
  }
}
