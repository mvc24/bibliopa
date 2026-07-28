import { NextResponse } from 'next/server';

import { getUserById, activateUser } from '@/lib/queries/users';
import { readUserId, verifyToken } from '@/lib/tokens';

const invalid = () =>
  NextResponse.json(
    { error: 'Dieser Link ist ungültig oder abgelaufen.' },
    { status: 400 },
  );

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  const token = body?.token;
  if (!token) return invalid();

  const userId = readUserId(token);
  if (!userId) return invalid();

  const user = await getUserById(userId);
  if (!user) return invalid();

  // Binding is is_active: once the account activates, the link stops working.
  const valid = verifyToken(token, 'verify-email', String(user.is_active));
  if (!valid) return invalid();

  await activateUser(user.user_id);
  return NextResponse.json({ ok: true });
}
