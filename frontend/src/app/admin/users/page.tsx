import { redirect } from 'next/navigation';

import { AppShell } from '@/components/layout/AppShell';
import { getCurrentSession } from '@/lib/auth';
import { CreateUserForm } from './CreateUserForm';

export default async function AdminUsersPage() {
  const session = await getCurrentSession();

  if (!session?.user) {
    redirect('/login');
  }
  if (session.user.role !== 'admin') {
    redirect('/');
  }

  return (
    <AppShell>
      <div
        className="panel"
        style={{ maxWidth: 480 }}
      >
        <CreateUserForm />
      </div>
    </AppShell>
  );
}
