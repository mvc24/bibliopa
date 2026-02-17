import { getServerSession } from 'next-auth';
import { authOptions } from '@/app/api/auth/[...nextauth]/route';
import { UserRole } from '@/types/database';
import { redirect } from 'next/navigation';

/**
 * Get current session in Server Components
 * Returns null if no session exists
 */
export async function getCurrentSession() {
  return await getServerSession(authOptions);
}

/**
 * Get current user or redirect to login
 * Use this in protected pages/API routes
 */
export async function requireAuth() {
  const session = await getCurrentSession();

  if (!session || !session.user) {
    redirect('/login');
  }

  return session;
}

/**
 * Check if user has required role
 * @param requiredRoles - Array of roles that are allowed
 */
export async function requireRole(requiredRoles: UserRole[]) {
  const session = await requireAuth();
  const userRole = session.user.role as UserRole;

  if (!requiredRoles.includes(userRole)) {
    throw new Error('Unauthorized: Insufficient permissions');
  }

  return session;
}

/**
 * Check if user has permission for an action
 * Admin has all permissions (including debug info)
 * Family can add/edit/delete entries and view prices
 * Researcher can view all content including prices (no edit functionality)
 * Viewer can only view (no prices)
 * Guest (no login) can only browse
 */
export function hasPermission(
  userRole: UserRole | undefined,
  action:
    | 'view'
    | 'add'
    | 'edit'
    | 'delete'
    | 'view_prices'
    | 'view_debug_info',
): boolean {
  if (!userRole) {
    // No login - can only view
    return action === 'view';
  }

  switch (userRole) {
    case 'admin':
      return true; // Admin can do everything

    case 'family':
      return ['view', 'add', 'edit', 'delete', 'view_prices'].includes(action);

    case 'researcher':
      return ['view', 'view_prices'].includes(action);

    case 'viewer':
      return ['view'].includes(action);

    case 'guest':
      return ['view'].includes(action);

    default:
      return false;
  }
}

/**
 * Get user role from session or undefined if no session
 */
export async function getUserRole(): Promise<UserRole | undefined> {
  const session = await getCurrentSession();
  return session?.user?.role as UserRole | undefined;
}

/**
 * Check if user can download content
 * Viewers and family can download, guests cannot
 */
export async function canDownload(): Promise<boolean> {
  const role = await getUserRole();
  return (
    role === 'admin' ||
    role === 'family' ||
    role === 'viewer' ||
    role === 'researcher'
  );
}

export async function canModify(): Promise<boolean> {
  if (process.env.NEXT_PUBLIC_DEV_MODE === 'true') return true;
  const role = await getUserRole();
  return role === 'admin' || role === 'family';
}

/**
 * Check if user can see prices
 * Admin, family, and researcher can see prices

*/
export async function canViewPrices(): Promise<boolean> {
  if (process.env.NEXT_PUBLIC_DEV_MODE === 'true') return true;
  const role = await getUserRole();
  return role === 'admin' || role === 'family' || role === 'researcher';
}

/**
 * Check if user can see debug information
 * Only admin can see composite_ids, unified_ids, and parsing metadata
 */
export async function canViewDebugInfo(): Promise<boolean> {
  if (process.env.NEXT_PUBLIC_DEV_MODE === 'true') return true;

  const role = await getUserRole();
  return role === 'admin';
}
