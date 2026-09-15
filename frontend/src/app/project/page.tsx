'use client';
import { AppShell } from '../../components/layout/AppShell';

export default function ProjectPage() {
  return (
    <AppShell>
      <div className="stack project-page">
        <div className="stack">
          <h1 className="project-title">bibliopa – die Bibliographie vom Opa</h1>
          <h2 className="project-subtitle">
            bibliopa – bibliography + Opa (German: grandfather)
          </h2>
          <p>
            <a
              className="project-repo-link"
              href="https://github.com/mvc24/bibliopa"
              target="_blank"
              rel="noopener noreferrer"
            >
              View on GitHub
            </a>
          </p>
        </div>

        <div className="lang-grid">
          {/* Deutsch */}
          <section className="panel stack lang-card">
            <h2 className="section-heading">Vom Zettelkatalog zur Datenbank</h2>
            <p className="meta">
              <strong>Selbstständiges Datenprojekt | 09/2025–aktuell</strong>
            </p>

            <h3 className="section-heading">Das Projekt</h3>
            <p>
              bibliopa ist ein selbst initiiertes Projekt, um die über
              Jahrzehnte gewachsene Büchersammlung meines Großvaters – eines
              pensionierten Bibliothekars – aus knapp 50 Word-Dokumenten in eine
              strukturierte, durchsuchbare Datenbank und Webanwendung zu
              überführen.
            </p>
            <p>
              Die Ausgangsdaten sind nicht für eine Datenbank strukturiert: Die
              Dokumente unterscheiden sich in Aufbau und Formatierung,
              Informationen sind teilweise unvollständig oder inkonsistent, und
              im Laufe der Zeit entstanden mehrere unterschiedliche Datenstände.
            </p>
            <p>
              Ich habe mir die dafür notwendigen Kenntnisse selbst erarbeitet
              und den gesamten Prozess von der Rohdatenaufbereitung über die
              Datenverarbeitung und Datenbank bis zur Webanwendung eigenständig
              aufgebaut.
            </p>

            <h3 className="section-heading">Von Word zur Datenbank</h3>
            <p className="flow-line">
              Word-Dokumente → Extraktion &amp; Bereinigung → strukturiertes
              Parsing → Abgleich &amp; Zusammenführung → Entity Resolution →
              PostgreSQL → Webanwendung
            </p>
            <p>
              Der Schwerpunkt des Projekts liegt auf der Datenpipeline. Sie
              extrahiert die Inhalte aus den ursprünglichen Dokumenten, bereitet
              die Rohdaten auf, strukturiert die bibliografischen Angaben und
              führt die Ergebnisse in einem relationalen Datenmodell zusammen.
            </p>
            <p>
              Der Prozess wird iterativ weiterentwickelt: Die Ergebnisse eines
              Verarbeitungsschritts dienen dazu, Probleme in den Quelldaten und
              im eigenen Vorgehen zu erkennen und die nächsten Durchläufe
              gezielt zu verbessern.
            </p>

            <h3 className="section-heading">Arbeiten mit gewachsenen Daten</h3>
            <p>
              Eine besondere Herausforderung ist die Zusammenführung mehrerer
              Datenstände und die Rückverfolgbarkeit einzelner Datensätze zu
              ihrer ursprünglichen Quelle.
            </p>
            <p>
              Für rund 13.000 bibliografische Datensätze wurden daher
              sprechende, deterministische IDs entwickelt. Beim erneuten
              Einlesen eines aktualisierten Datenstands konnten neue und bereits
              verarbeitete Datensätze miteinander abgeglichen und vorhandene
              Arbeit soweit wie möglich weiterverwendet werden.
            </p>

            <h3 className="section-heading">Entity Resolution</h3>
            <p>
              Ein großer Teil der Arbeit entfällt auf die Bereinigung und
              Zusammenführung von Personenangaben. Unterschiedliche
              Schreibweisen, nicht standardisierte Transliteration, fehlende
              Vornamen und uneindeutige Angaben machen es notwendig,
              verschiedene Verfahren miteinander zu kombinieren.
            </p>
            <p>
              Der Matching-Prozess wurde schrittweise erweitert – von manueller
              Prüfung und Normalisierung über Fuzzy Matching mit RapidFuzz bis
              zum Einsatz von Splink für probabilistisches Record Linkage.
              Ergänzend kommen regelbasierte Verfahren, manuelle Validierung und
              Recherche in den Originaldaten zum Einsatz.
            </p>
            <p>
              Dabei wurden auch weitere Datenqualitätsprobleme sichtbar, etwa
              Organisationen, die zunächst als Personen erfasst wurden, oder
              mehrere Personen, die in einem Datensatz zusammengefasst waren.
            </p>

            <h3 className="section-heading">Technischer Schwerpunkt</h3>
            <p>
              <strong>Daten:</strong> Python · PostgreSQL · ETL ·
              Datenbereinigung · Datenmodellierung · Entity Resolution · Record
              Linkage
            </p>
            <p>
              <strong>Verarbeitung:</strong> Claude API · Claude Batch API ·
              RapidFuzz · Splink · Jupyter
            </p>
            <p>
              <strong>Datenbank:</strong> PostgreSQL · Alembic · Neon · DBeaver
            </p>
            <p>
              <strong>Anwendung:</strong> Next.js · React · TypeScript · React
              Aria
            </p>

            <h3 className="section-heading">Aktueller Stand</h3>
            <p>
              bibliopa ist ein laufendes Projekt. Die Datenbank und die
              Webanwendung sind funktional; gleichzeitig werden Datenpipeline
              und Entity-Resolution-Prozesse weiter verfeinert, da die Arbeit
              mit den gewachsenen Quelldaten fortlaufend neue
              Datenqualitätsprobleme sichtbar macht.
            </p>
          </section>

          {/* English */}
          <section className="panel stack lang-card">
            <h2 className="section-heading">
              From a card catalogue to a database
            </h2>
            <p className="meta">
              <strong>Self-directed data project | 09/2025–present</strong>
            </p>

            <h3 className="section-heading">The project</h3>
            <p>
              bibliopa is a self-initiated project to turn my grandfather&apos;s
              decades-old catalogue of his private library – he is a retired
              librarian – from almost 50 Word documents into a structured,
              searchable database and web application.
            </p>
            <p>
              The source data was not designed for database use: the documents
              differ in structure and formatting, information is sometimes
              incomplete or inconsistent, and several different versions of the
              data have emerged over time.
            </p>
            <p>
              I taught myself the skills required for the project and built the
              process independently, from preparing the raw data and processing
              it through to the database and web application.
            </p>

            <h3 className="section-heading">From Word to database</h3>
            <p className="flow-line">
              Word documents → extraction &amp; cleaning → structured parsing →
              reconciliation &amp; merging → entity resolution → PostgreSQL →
              web application
            </p>
            <p>
              The core of the project is the data pipeline. It extracts
              information from the original documents, prepares the raw data,
              structures the bibliographic information and brings the results
              together in a relational data model.
            </p>
            <p>
              The process is iterative: the results of each processing stage are
              analysed to identify problems in the source data and in my own
              approach, which then informs the next iteration.
            </p>

            <h3 className="section-heading">Working with evolving source data</h3>
            <p>
              A significant challenge has been reconciling multiple versions of
              the source data while maintaining traceability back to the original
              records.
            </p>
            <p>
              For around 13,000 bibliographic records, I therefore developed
              meaningful, deterministic IDs. When importing an updated version of
              the source data, new and previously processed records could be
              compared and existing work reused wherever possible.
            </p>

            <h3 className="section-heading">Entity resolution</h3>
            <p>
              A substantial part of the project involves cleaning and
              consolidating person data. Different spellings, inconsistent
              transliterations, missing first names and ambiguous information
              require several approaches to be combined.
            </p>
            <p>
              The matching process has evolved step by step – from manual
              inspection and normalisation to fuzzy matching with RapidFuzz and,
              most recently, Splink for probabilistic record linkage. Rule-based
              approaches, manual validation and research using the original
              records complement the automated matching.
            </p>
            <p>
              This process has also exposed further data-quality problems, such
              as organisations initially treated as people or multiple people
              combined into a single record.
            </p>

            <h3 className="section-heading">Technical focus</h3>
            <p>
              <strong>Data:</strong> Python · PostgreSQL · ETL · data cleaning ·
              data modelling · entity resolution · record linkage
            </p>
            <p>
              <strong>Processing:</strong> Claude API · Claude Batch API ·
              RapidFuzz · Splink · Jupyter
            </p>
            <p>
              <strong>Database:</strong> PostgreSQL · Alembic · Neon · DBeaver
            </p>
            <p>
              <strong>Application:</strong> Next.js · React · TypeScript · React
              Aria
            </p>

            <h3 className="section-heading">Current status</h3>
            <p>
              bibliopa is an ongoing project. The database and web application
              are functional, while the data pipeline and entity-resolution
              processes continue to be refined as working with the evolving
              source data reveals further data-quality issues.
            </p>
          </section>
        </div>
      </div>
    </AppShell>
  );
}
