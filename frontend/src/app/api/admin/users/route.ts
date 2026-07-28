import { NextResponse } from 'next/server';
import { hash } from 'bcryptjs';
import { randomBytes } from 'crypto';
import { z } from 'zod';

import { getCurrentSession } from '@/lib/auth';
import { createUser } from '@/lib/queries/users';
import { createToken } from '@/lib/tokens';
import { sendSetPasswordEmail } from '@/lib/email';

const schema = z.object({
  username: z.string().trim().min(1, 'Bitte gib einen Benutzernamen ein.'),
  email: z.email('Bitte gib eine gültige E-Mail-Adresse ein.'),
  role: z.enum(['researcher', 'family', 'viewer']),
});

export async function POST(request: Request) {
  const session = await getCurrentSession();
  if (session?.user?.role !== 'admin') {
    return NextResponse.json({ error: 'Keine Berechtigung.' }, { status: 403 });
  }

  const body = await request.json().catch(() => null);
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: parsed.error.issues[0].message },
      { status: 400 },
    );
  }

  const { username, email, role } = parsed.data;

  try {
    // No password yet. password_hash is NOT NULL, so store an unguessable
    // placeholder; the set-password link replaces it and activates the account.
    const placeholder = await hash(randomBytes(32).toString('hex'), 10);
    const user = await createUser(username, email, placeholder, role);

    const token = createToken(
      user.user_id,
      'set-password',
      user.password_hash, // binding: link dies once the real password is set
      60 * 24 * 3, // 3 days
    );
    const link = `${process.env.NEXTAUTH_URL}/reset-password?token=${token}`;
    await sendSetPasswordEmail(email, link);

    if (process.env.NODE_ENV !== 'production') {
      console.log('[set-password link]', link);
    }

    return NextResponse.json({ ok: true });
  } catch (err) {
    if ((err as { code?: string }).code === '23505') {
      return NextResponse.json(
        { error: 'Benutzername oder E-Mail ist bereits vergeben.' },
        { status: 409 },
      );
    }
    console.error('Admin create user error:', err);
    return NextResponse.json(
      { error: 'Konto konnte nicht erstellt werden.' },
      { status: 500 },
    );
  }
}
