'use client';
import { AppShell } from '@/components/layout/AppShell';
import { Button } from 'react-aria-components';
import { Suspense, useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

function VerifyInner() {
  const token = useSearchParams().get('token');
  const router = useRouter();
  const [status, setStatus] = useState<'pending' | 'ok' | 'error'>('pending');

  useEffect(() => {
    if (!token) {
      setStatus('error');
      return;
    }
    fetch('/api/auth/verify-email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token }),
    })
      .then((res) => setStatus(res.ok ? 'ok' : 'error'))
      .catch(() => setStatus('error'));
  }, [token]);

  if (status === 'pending') {
    return <p>Wird bestätigt…</p>;
  }

  if (status === 'ok') {
    return (
      <div className="stack">
        <h2 className="page-title">E-Mail bestätigt</h2>
        <p>Dein Konto ist jetzt aktiv. Du kannst dich anmelden.</p>
        <Button onPress={() => router.push('/login')}>Zum Login</Button>
      </div>
    );
  }

  return (
    <div className="stack">
      <h2 className="page-title">Link ungültig</h2>
      <p>Dieser Bestätigungslink ist ungültig oder abgelaufen.</p>
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <AppShell>
      <div
        className="panel"
        style={{ maxWidth: 480 }}
      >
        <Suspense fallback={<p>Wird geladen…</p>}>
          <VerifyInner />
        </Suspense>
      </div>
    </AppShell>
  );
}
