'use client';
import { AppShell } from '../../components/layout/AppShell';

const REPO = 'https://github.com/mvc24/bibliopa';
const DOCS = `${REPO}/blob/main/docs`;
const PIPELINE = `${REPO}/tree/main/pipeline`;

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
              href={REPO}
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
              <strong>Selbstständiges Datenprojekt | 09/2025–09/2026</strong>
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

            <h3 className="section-heading">Zwei Durchläufe</h3>
            <p>
              Die Migration wurde zweimal durchgeführt. Im ersten Durchlauf
              (09/2025–01/2026) mussten zwei nicht identische Versionen des
              Katalogs – eine mit Preisen, eine ohne – vor dem Parsing
              zusammengeführt werden. 11.544 Einträge konnten exakt zugeordnet
              werden, 1.156 bepreiste Einträge nicht. Ein zweiter Schritt fand
              935 davon per Fuzzy Matching, seine Ergebnisse wurden aber nie
              zurückgeschrieben. Die Datenbank ging mit diesen Lücken online.
            </p>
            <p>
              Im zweiten Durchlauf (04/2026–08/2026) korrigierte mein Großvater
              stattdessen einen einzigen Datenstand und markierte jede
              geänderte Zeile mit „! “ und jede entfernte mit „AUS! “. Dieser
              Stand wurde neu extrahiert, mit einem überarbeiteten Prompt neu
              geparst und auf einen Datenbank-Branch geladen, weil die erste
              Version bereits in Benutzung war. Die Personendaten wurden auf
              die bestehende Personentabelle abgeglichen statt neu
              dedupliziert.
            </p>
            <p>
              Beide Durchläufe sind im Repository so erhalten, wie sie gelaufen
              sind – mit Code, Zählungen und Logs:{' '}
              <a href={PIPELINE} target="_blank" rel="noopener noreferrer">
                pipeline/
              </a>
              . Ein einzelnes Buch ist von der Word-Zeile bis zur
              Datenbankzeile nachverfolgt:{' '}
              <a
                href={`${DOCS}/trace.md`}
                target="_blank"
                rel="noopener noreferrer"
              >
                docs/trace.md
              </a>
              .
            </p>

            <h3 className="section-heading">Zahlen</h3>
            <table className="numbers-table">
              <tbody>
                <tr>
                  <td>Word-Dokumente</td>
                  <td>49</td>
                </tr>
                <tr>
                  <td>Tabellenzeilen in den Dokumenten</td>
                  <td>12.614</td>
                </tr>
                <tr>
                  <td>Datensätze nach der Extraktion</td>
                  <td>12.492</td>
                </tr>
                <tr>
                  <td>Datensätze nach dem Parsing (ohne Querverweise)</td>
                  <td>11.498</td>
                </tr>
                <tr>
                  <td>Bücher in der Datenbank</td>
                  <td>10.919</td>
                </tr>
                <tr>
                  <td>Im August 2026 als fehlend erkannt, neu geparst</td>
                  <td>1.008</td>
                </tr>
                <tr>
                  <td>Personennennungen in den geparsten Daten</td>
                  <td>17.722</td>
                </tr>
                <tr>
                  <td>Personen in der Datenbank</td>
                  <td>8.947</td>
                </tr>
                <tr>
                  <td>API-Kosten für das Parsing (beide Durchläufe)</td>
                  <td>ca. 200 $</td>
                </tr>
              </tbody>
            </table>

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
            <p>
              Drei Monate nach dem zweiten Durchlauf fehlten in der Datenbank
              1.008 Bücher. Die Ursache ließ sich über Mengenvergleiche der IDs
              pro Verarbeitungsstufe eingrenzen: Die Batch-API hatte einzelne
              Einträge innerhalb erfolgreich abgeschlossener Batches mit
              Fehlern zurückgegeben, und die Abholung hatte sie ohne Log
              übersprungen. Die Einträge wurden neu geparst; die Zählkette
              steht in{' '}
              <a
                href={`${DOCS}/data-quality.md`}
                target="_blank"
                rel="noopener noreferrer"
              >
                docs/data-quality.md
              </a>
              .
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
              Das Splink-Modell ist nicht fertig: Exakte Nachnamen-Treffer
              tragen ein negatives Gewicht, die Ursache und der Stand sind in{' '}
              <a
                href={`${DOCS}/entity-resolution.md`}
                target="_blank"
                rel="noopener noreferrer"
              >
                docs/entity-resolution.md
              </a>{' '}
              dokumentiert.
            </p>

            <h3 className="section-heading">Arbeiten mit KI</h3>
            <p>
              KI kommt in diesem Projekt an zwei Stellen vor, die getrennt zu
              beurteilen sind.
            </p>
            <p>
              <strong>Als Bestandteil der Pipeline:</strong> Jeder
              Katalogeintrag wurde über die Claude Batch API in ein
              JSON-Objekt mit rund 30 Feldern überführt. Der Prompt des
              zweiten Durchlaufs ersetzt einen unbrauchbaren Confidence-Score
              durch sechs Flags mit Begründungspflicht. Das Modell darf
              offensichtliche Tippfehler korrigieren, muss das aber
              kennzeichnen; bei Unsicherheit gilt: markieren statt korrigieren.
              Preise, Themenzuordnung und die Aufteilung von Namen wurden
              bewusst aus dem Prompt herausgehalten.
            </p>
            <p>
              <strong>Als Werkzeug:</strong> Ich habe Python an diesem Projekt
              gelernt. Für die Datenpipeline durfte das Modell erklären, aber
              keinen Code schreiben; Matching-Regeln, IDs, SQL und alle
              Entscheidungen über die Daten sind meine. Den Großteil der
              Webanwendung habe ich dagegen delegiert und geprüft. Die Regeln
              dafür stehen versioniert im Repository, und jede festgestellte
              Abweichung wurde zu einer neuen Regel. Was delegiert wurde, wie
              die Kontrolle funktioniert hat und wo sie versagt hat:{' '}
              <a
                href={`${DOCS}/working-with-ai.md`}
                target="_blank"
                rel="noopener noreferrer"
              >
                docs/working-with-ai.md
              </a>
              .
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
              Die Anwendung wurde ausgeliefert und mehrere Monate lang von
              meinem Großvater selbst benutzt – zum Suchen, Blättern und
              Erfassen neuer Bücher. 2026 hat er sich entschieden, die Sammlung
              zu verkaufen. Die Anwendung ist jetzt der Katalog, der den
              Verkauf begleitet; der Fokus hat sich damit von der strukturierten
              Detailanzeige zu „jedes Buch ist sichtbar, mit seinem
              Originaleintrag“ verschoben.
            </p>
            <p>
              Offen sind: das Laden der 1.008 neu geparsten Bücher nach dem
              Abgleich ihrer Personen, die Bereinigung von 20 doppelten
              Personenzuordnungen vor dem Setzen eines Unique-Constraints, und
              das Splink-Modell.
            </p>

            <h3 className="section-heading">Dokumentation</h3>
            <ul className="doc-links">
              <li>
                <a href={REPO} target="_blank" rel="noopener noreferrer">
                  README
                </a>{' '}
                – Überblick, Entscheidungen, Zahlen
              </li>
              <li>
                <a href={PIPELINE} target="_blank" rel="noopener noreferrer">
                  pipeline/
                </a>{' '}
                – beide Durchläufe, Stufe für Stufe, mit Logs
              </li>
              <li>
                <a
                  href={`${DOCS}/trace.md`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  trace.md
                </a>{' '}
                – ein Buch, von der Word-Zeile bis zur App
              </li>
              <li>
                <a
                  href={`${DOCS}/data-quality.md`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  data-quality.md
                </a>{' '}
                – die fehlenden 1.008 Bücher
              </li>
              <li>
                <a
                  href={`${DOCS}/entity-resolution.md`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  entity-resolution.md
                </a>{' '}
                – Personen-Deduplizierung, Splink
              </li>
              <li>
                <a
                  href={`${DOCS}/schema.md`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  schema.md
                </a>{' '}
                – Tabellen und Schemaänderungen
              </li>
              <li>
                <a
                  href={`${DOCS}/working-with-ai.md`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  working-with-ai.md
                </a>{' '}
                – KI in der Pipeline und als Werkzeug
              </li>
            </ul>
          </section>

          {/* English */}
          <section className="panel stack lang-card">
            <h2 className="section-heading">
              From a card catalogue to a database
            </h2>
            <p className="meta">
              <strong>Self-directed data project | 09/2025–09/2026</strong>
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

            <h3 className="section-heading">Two runs</h3>
            <p>
              The migration was done twice. In the first run (09/2025–01/2026),
              two non-identical versions of the catalogue – one with prices,
              one without – had to be collated before parsing. 11,544 entries
              matched exactly; 1,156 priced entries did not. A second stage
              located 935 of them by fuzzy matching, but its results were never
              written back. The database went live with those gaps.
            </p>
            <p>
              In the second run (04/2026–08/2026), my grandfather corrected a
              single set of documents instead, marking every edited row with
              &ldquo;! &rdquo; and every removed row with &ldquo;AUS! &rdquo;.
              That set was re-extracted, re-parsed with a rewritten prompt and
              loaded onto a database branch, because the first version was
              already in use. Person data was matched onto the existing people
              table rather than deduplicated again.
            </p>
            <p>
              Both runs are kept in the repository as they were run – code,
              counts and logs:{' '}
              <a href={PIPELINE} target="_blank" rel="noopener noreferrer">
                pipeline/
              </a>
              . One book is followed from its Word row to its database row:{' '}
              <a
                href={`${DOCS}/trace.md`}
                target="_blank"
                rel="noopener noreferrer"
              >
                docs/trace.md
              </a>
              .
            </p>

            <h3 className="section-heading">Numbers</h3>
            <table className="numbers-table">
              <tbody>
                <tr>
                  <td>Word documents</td>
                  <td>49</td>
                </tr>
                <tr>
                  <td>Table rows in the documents</td>
                  <td>12,614</td>
                </tr>
                <tr>
                  <td>Records after extraction</td>
                  <td>12,492</td>
                </tr>
                <tr>
                  <td>Records after parsing (cross-references dropped)</td>
                  <td>11,498</td>
                </tr>
                <tr>
                  <td>Books in the database</td>
                  <td>10,919</td>
                </tr>
                <tr>
                  <td>Found missing in August 2026, re-parsed</td>
                  <td>1,008</td>
                </tr>
                <tr>
                  <td>Person mentions in the parsed data</td>
                  <td>17,722</td>
                </tr>
                <tr>
                  <td>People in the database</td>
                  <td>8,947</td>
                </tr>
                <tr>
                  <td>API cost for parsing (both runs)</td>
                  <td>about $200</td>
                </tr>
              </tbody>
            </table>

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
            <p>
              Three months after the second run, 1,008 books were missing from
              the database. Set comparisons of the IDs at each stage narrowed
              the cause down: the Batch API had returned per-entry errors inside
              batches that had completed successfully, and retrieval skipped
              them without logging. The entries were re-parsed; the count chain
              is in{' '}
              <a
                href={`${DOCS}/data-quality.md`}
                target="_blank"
                rel="noopener noreferrer"
              >
                docs/data-quality.md
              </a>
              .
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
              combined into a single record. The Splink model is not finished:
              exact surname matches carry a negative weight; the cause and
              current state are documented in{' '}
              <a
                href={`${DOCS}/entity-resolution.md`}
                target="_blank"
                rel="noopener noreferrer"
              >
                docs/entity-resolution.md
              </a>
              .
            </p>

            <h3 className="section-heading">Working with AI</h3>
            <p>
              AI appears in two places in this project, and they should be
              judged separately.
            </p>
            <p>
              <strong>As a component of the pipeline:</strong> every catalogue
              entry was turned into a JSON object with about 30 fields through
              the Claude Batch API. The second run&apos;s prompt replaces an
              unusable confidence score with six flags, each requiring a
              written reason. The model may correct obvious typos but must mark
              that it did; when in doubt, it flags instead of correcting.
              Prices, topic assignment and name splitting were deliberately
              kept out of the prompt.
            </p>
            <p>
              <strong>As a tool:</strong> I learned Python on this project. For
              the data pipeline the model was allowed to explain but not to
              write code; matching rules, IDs, SQL and every decision about the
              data are mine. Most of the web application, by contrast, I
              delegated and reviewed. The rules for this are versioned in the
              repository, and every violation I caught became a new rule. What
              was delegated, how control worked and where it failed:{' '}
              <a
                href={`${DOCS}/working-with-ai.md`}
                target="_blank"
                rel="noopener noreferrer"
              >
                docs/working-with-ai.md
              </a>
              .
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
              The application was delivered and used by my grandfather himself
              for several months – searching, browsing and adding new books. In
              2026 he decided to sell the collection. The application is now the
              catalogue that accompanies the sale, and the focus has shifted from
              structured detail to &ldquo;every book is visible, with its
              original entry&rdquo;.
            </p>
            <p>
              Still open: loading the 1,008 re-parsed books once their people
              are matched, merging 20 duplicate person assignments before adding
              a unique constraint, and the Splink model.
            </p>

            <h3 className="section-heading">Documentation</h3>
            <ul className="doc-links">
              <li>
                <a href={REPO} target="_blank" rel="noopener noreferrer">
                  README
                </a>{' '}
                – overview, decisions, numbers
              </li>
              <li>
                <a href={PIPELINE} target="_blank" rel="noopener noreferrer">
                  pipeline/
                </a>{' '}
                – both runs, stage by stage, with logs
              </li>
              <li>
                <a
                  href={`${DOCS}/trace.md`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  trace.md
                </a>{' '}
                – one book, from Word row to app
              </li>
              <li>
                <a
                  href={`${DOCS}/data-quality.md`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  data-quality.md
                </a>{' '}
                – the 1,008 missing books
              </li>
              <li>
                <a
                  href={`${DOCS}/entity-resolution.md`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  entity-resolution.md
                </a>{' '}
                – people deduplication, Splink
              </li>
              <li>
                <a
                  href={`${DOCS}/schema.md`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  schema.md
                </a>{' '}
                – tables and schema changes
              </li>
              <li>
                <a
                  href={`${DOCS}/working-with-ai.md`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  working-with-ai.md
                </a>{' '}
                – AI in the pipeline and as a tool
              </li>
            </ul>
          </section>
        </div>
      </div>
    </AppShell>
  );
}
