import crypto from 'crypto';

type Purpose = 'verify-email' | 'set-password';

/**
 * Signed-link tokens, no DB storage.
 *
 * The signature key is NEXTAUTH_SECRET plus a "binding" value taken from the
 * user's own row, so a link dies the moment that value changes:
 *   - set-password links bind to password_hash  -> single-use once the password is set
 *   - verify-email links bind to String(is_active) -> dead once the account activates
 */
function sign(payload: string, binding: string) {
  return crypto
    .createHmac('sha256', process.env.NEXTAUTH_SECRET! + binding)
    .update(payload)
    .digest('base64url');
}

export function createToken(
  userId: string,
  purpose: Purpose,
  binding: string,
  ttlMinutes: number,
) {
  const exp = Date.now() + ttlMinutes * 60_000;
  const payload = Buffer.from(
    JSON.stringify({ userId, purpose, exp }),
  ).toString('base64url');
  return `${payload}.${sign(payload, binding)}`;
}

/**
 * Read the userId out of the (still unverified) payload, so the caller can load
 * that user and fetch the binding value to pass back into verifyToken.
 */
export function readUserId(token: string): string | null {
  const [payload] = token.split('.');
  if (!payload) return null;
  try {
    return JSON.parse(Buffer.from(payload, 'base64url').toString()).userId;
  } catch {
    return null;
  }
}

export function verifyToken(
  token: string,
  purpose: Purpose,
  binding: string,
): string | null {
  const [payload, signature] = token.split('.');
  if (!payload || !signature) return null;
  if (sign(payload, binding) !== signature) return null;

  const data = JSON.parse(Buffer.from(payload, 'base64url').toString());
  if (data.purpose !== purpose || data.exp < Date.now()) return null;
  return data.userId as string;
}
