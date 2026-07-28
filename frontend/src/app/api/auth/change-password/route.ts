import { NextResponse } from 'next/server';
import { hash, compare } from 'bcryptjs';
import { z } from 'zod';

import { getCurrentSession } from '@/lib/auth';
import { getUserById, setPassword } from '@/lib/queries/users';

const schema = z.object({
  currentPassword: z.string().min(1, 'Bitte gib dein aktuelles Passwort ein.'),
  newPassword: z
    .string()
    .min(8, 'Das neue Passwort muss mindestens 8 Zeichen lang sein.'),
});

export async function POST(request: Request) {
  const session = await getCurrentSession();
  if (!session?.user) {
    return NextResponse.json({ error: 'Nicht angemeldet.' }, { status: 401 });
  }

  const body = await request.json().catch(() => null);
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: parsed.error.issues[0].message },
      { status: 400 },
    );
  }

  const { currentPassword, newPassword } = parsed.data;

  const user = await getUserById(session.user.id);
  if (!user) {
    return NextResponse.json(
      { error: 'Benutzer nicht gefunden.' },
      { status: 404 },
    );
  }

  const currentValid = await compare(currentPassword, user.password_hash);
  if (!currentValid) {
    return NextResponse.json(
      { error: 'Das aktuelle Passwort ist falsch.' },
      { status: 400 },
    );
  }

  const password_hash = await hash(newPassword, 10);
  await setPassword(user.user_id, password_hash);

  return NextResponse.json({ ok: true });
}
