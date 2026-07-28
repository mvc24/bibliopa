import { NextResponse } from 'next/server';
import { hash } from 'bcryptjs';
import { z } from 'zod';

import { getUserById, setPassword } from '@/lib/queries/users';
import { readUserId, verifyToken } from '@/lib/tokens';

const schema = z.object({
  token: z.string().min(1),
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

  const { token, password } = parsed.data;

  const userId = readUserId(token);
  if (!userId) {
    return NextResponse.json(
      { error: 'Dieser Link ist ungültig oder abgelaufen.' },
      { status: 400 },
    );
  }

  const user = await getUserById(userId);
  if (!user) {
    return NextResponse.json(
      { error: 'Dieser Link ist ungültig oder abgelaufen.' },
      { status: 400 },
    );
  }

  const valid = verifyToken(token, 'set-password', user.password_hash);
  if (!valid) {
    return NextResponse.json(
      { error: 'Dieser Link ist ungültig oder abgelaufen.' },
      { status: 400 },
    );
  }

  const password_hash = await hash(password, 10);
  // setPassword also flips is_active to true, activating new accounts.
  await setPassword(user.user_id, password_hash);

  return NextResponse.json({ ok: true });
}
