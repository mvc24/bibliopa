'use client';
import { AppShell } from '../../components/layout/AppShell';

export default function ProjectPage() {
  return (
    <AppShell>
      <div className="panel">
        <div className="stack">
          <h2 className="page-title">Project Overview</h2>
          <p>
            Portfolio-friendly overview of the tech stack, pipelines, and data
            quality processes behind Bibliopa.
          </p>
          <ul>
            <li>Backend: FastAPI, PostgreSQL, Alembic migrations</li>
            <li>
              ETL & data quality: validation, people normalization, discrepancy
              review flows
            </li>
            <li>Frontend: Next.js 15, Mantine, Refine for CRUD and data grids</li>
            <li>Auth: NextAuth sessions with role-based UI states</li>
            <li>Exports: PDF/CSV for search results and single entries</li>
          </ul>
        </div>
      </div>
    </AppShell>
  );
}
