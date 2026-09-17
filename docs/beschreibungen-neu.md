# bibliopa beschreibungen

Problem: Das Projekt ist zu groß und ich weiß nicht was wichtig ist, und was nicht!!!

[Getting portfolio ready](https://app.notion.com/p/Getting-portfolio-ready-3dccfc57f3c080f1b7bfec723d347c2d?pvs=21)

## Prozess

- knapp 50 Word-Dokumente, nach Themenbereichen geordnet, ~15000 Datensätze (inklusive Querverweise etc.)
- **Rohdaten-Version 1**:
    - es mussten im 1. Durchgang zwei verschiedene Versionen der gleichen Dokumente konsolidiert werden, eine Version mit Auspreisungen, eine ohne. Es waren nicht alle Dokumente gleich, zum Teil wurden Einträge zwischen Themen verschoben oder in einer Version geändert, in der anderen nicht.
        - Erster Parsing-Durchgang beruhte auf diesen Dokumenten, erste Runde der Personen-Deduplizierung ebenfalls
        - Erstellung einer `composite_id` in der Form `record["composite_id"] = f"{topic_normalised}_{index}_{batch_id}_{total_batches}"`  → dadurch ist eine exakte Rückverfolgung zum Originaldatensatz möglich, war im Lauf des Projekts eine der besten Enschreidungen
        - Probleme:
            - durch die Konsolidierung gab es ~3000 Datensätze, die nicht exakt gematcht werden konnten
            - Anführungszeichen in Originaldaten haben zum Teil die Parsing-Resultate korrumpiert
- **Rohdaten-Version 2**:
    - in der Zwischenzeit wurde mit den Daten weiter gearbeitet, etwas verspätet wurde eine Kennzeichnung mit “! …“ für geänderte Daten vereinbart. Allerdings wurden auch zahlreiche Bücher “still” ausgeschieden, sie wurden (für mich nicht rückverfolgbar) gelöscht, auch hier konnten wir uns verspätet auf eine Kennzeichnung mit “AUS “einigen. Es wurde nur in der Version mit Preisen gearbeitet, eine Datenhoheit für diese Version wurde vereinbart.
    - Daten wurden mit neuer composite_id eingelesen
    - Ich wollte die bereits geparsten Ergebnisse nicht verlieren, daher Datenabgleich und matching zu existierenden Daten
- **Personen deduplizieren**
    - Der für mich langwierigste und wohl komplexeste Teil des Projekts
    - Einsatz von Fuzzy-Matching Algorithmen
- **Parser**
    - Ergebnisse aus Durchgang 1 analysiert um zu sehen, wie der Prompt-Text verbessert werden kann um exaktere Ergebnisse zu erhalten
    - Bessere Bereinigung der Daten im Vorfeld

## Beschreibung

Im Rahmen meines Webdevelopment-Bootcamp stellte ich fest, dass mich der Umgang mit Daten und Datenbanken viel mehr interessiert als die Webentwicklung selbst, und daher war bereits in meinem dortigen Abschlussprojekt die Datenbank der eigentlich zentrale Aspekt meiner Arbeit. 

Ich habe daraufhin in meinem privaten Umfeld ein perfektes Projekt gefunden: die bis dato in einem Quasi-Zettelkatalog (wenngleich in Word-Dokumenten erstellt) katalogisierte Büchersammlung meines Großvaters, ein pensionierter Bibliothekar. Er hat über Jahre hinweg seine stetig wachsende Sammlung in thematisch sortierten Word-Dokumenten katalogisiert, Preise geschätzt und Daten überarbeitet.

Ich beschloss daraufhin, Python zu lernen und mit Hilfe einer API-Anbindung zu Claude aus seinen Dokumenten eine Datenbank mit dazugehöriger Webanwendung zu erstellen. Ich habe mir alle dafür notwendigen Kompetenzen autodidaktisch mit Hilfe von KI erarbeitet. Mir war und ist es besonders wichtig ein Verständnis für die Abläufe und den Code zu entwickeln, und mir nicht nur Lösungen geben zu lassen. Der Prozess war langwierig und immer nach der Trial-and-Error-Methode, wo ich aus Problemen und Fehlern der vorangehenden Schritte lerne und versuche es in der nächsten Iteration besser zu machen. 

Das war für alle Schritte der ETL-Pipeline relevant. Ein Beispiel dafür war die Entscheidung, die (zwischendurch von meinem Großvater bearbeiteten) Rohdaten neu einzuspielen. Zu diesem Zeitpunkt hatte ich bereits eine mehr oder weniger funktionstüchtige Version meiner Applikation in der Datenbank, jedoch hatte ich zu viele Datensätze, die aufgrund der Notwendigkeit, zwei nicht idente aber sehr ähnliche Versionen der Rohdaten zusammenzuführen, nicht klar einzuordnen waren, und es aber wichtig war möglichst alle Datensätze zu erfassen.

Dabei wurde etwa beim “extract”-Schritt darauf geachtet, gewisse Sonderzeichen oder Encoding-Probleme, die zuvor zu korrumpierten Outputs führten, bereits bei der Vorbereitung der Daten zu bereinigen. Für den zweiten Parsing-Durchgang war es mir wichtig, die bereits zuvor transformierte Daten möglichst weiterverwenden zu können um die API-Kosten möglichst niedrig zu halten. Das Datenschema wurde angepasst um die Datentransformation durch die KI zu verbessern, und es wurden differenzierte Flags gesetzt, um etwa der KI zu erlauben, offensichtliche Tippfehler eigenständig auszubessern, diese jedoch als Bearbeitung durch die KI zu markieren.

Auch das Beladen der Datenbank selbst war von Lernprozessen begleitet, wie etwa die Tatsache, dass ich durch ein unbeabsichtigtes neu Laden der Personendaten nun drei verschiedene mögliche `person_ids`  hatte - zum Glück habe ich sowohl für Bücher als auch Personen beschlossen, parallel zu automatisch erstellten numerischen IDs auch sprechende IDs zu erstellen, die im Fall der Bücher genau zum Index im Original-(Word)-Dokument führte, und bei den Personen eine eindeutige, normalisierte Version des Namens ist. Aufgrund dieser Entscheidung war auch das erneute Laden (inklusive Neuerstellung der `composite_id` für jedes Buch) der Daten und eine Zusammenführen von alten und neuen Daten möglich. 

Der Prozess des Deduplizieren der Personen war wesentlich zeitaufwendiger und mühseliger als erwartet - und das, obwohl mir von vornherein klar war, dass es sich hierbei um eine komplexe Problematik handelt. Das Ziel wäre, dass jede Person nur einen Eintrag in der Personentabelle hat, und abweichende Schreibweisen erfasst werden und trotzdem mit der richtigen Person verknüpft werden können. Hinzu kommt, dass die Sammlung auch sehr viel russische und andere slawische Literatur enthält, und dass die Transliteration dieser Namen keineswegs standardisiert sind. Zahlreiche Katalogisate enthielten auch nur Nachnamen, hier musste zugeordnet und oft manuell recherchiert werden, um welche Person es sich (bei mehrfach vorkommenden Namen) handelt. 

Für den Reload der Daten habe ich mit einem eigenen Datenbank-Branch gearbeitet, um während des Umbaus die Seite weiterhin anzeigen zu können, und auch um sicherzugehen, dass ich nichts zerstöre. Für die Versionierung habe ich mit alembic gearbeitet, um so Schemaveränderungen nachverfolgen zu können.

Eine Idee, für die ich jedoch keine Zeit hatte, wäre die Personentabelle mit Open Source Daten wie der Gemeinsamen Normdatei der Deutschen Nationalbibliothek zu verknüpfen und da einen Datenabgleich herzustellen um Personendaten korrekt ablegen zu können - vielleicht kommt dieser Schritt ja noch irgendwann.

Die Webapplikation selbst habe ich mit Next.js/React erstellt, da dies Frameworks sind, die mir bereits bekannt waren. Für diesen Bereich habe ich jedoch zunehmend Schritte an die KI delegiert, da ich wirklich merkte, dass mein Interesse an diesem Bereich der Arbeit wesentlich geringer ist, und es für mich genug ist, wenn ich den Code verstehe und die Applikation meinen Vorstellungen entspricht und funktioniert. Hier ist jedoch hervorzuheben, dass ich hier viele wichtige Aspekte zur Arbeit mit KI-Agenten gelernt habe. 

Die Gegebenheiten zu den Funktionalitäten der Webapplikation haben sich zwischenzeitlich verändert, und während am Anfang die Idee war, dass mein Großvater selbst noch fehlende Werke katalogisieren wird und sich weiterhin mit der Preisrecherche/Schätzung auseinandersetzen wird, und er den Katalog erweitern wird, steht nun der Wunsch zum Verkauf der Sammlung im Vordergrund. Daher hat sich der Fokus dahingehend verschoben, dass wirklich alle Bücher der Sammlung angezeigt werden, und die möglichst korrekte Strukturierung und Anzeige der Daten weniger wichtig ist. Der (unstrukturierte) Originaldatensatz wird bei jedem Eintrag angezeigt, jedoch fehlen zum Teil noch die Verknüpfungen zu den korrekten Personen, und auch der Mechanismus zur Anzeige mehrbändiger Werke ist noch nicht korrekt ausgearbeitet. 

Allerdings hat nun mein Großvater endlich begriffen, dass eine strukturierte Verfügbarkeit der Daten doch Vorteile hat, nachdem ich ihm direkt über Datenbankabfragen Statistiken oder nach bestimmten Kriterien sortierte Listen erstellen kann.

Momentaner Stand: ich habe festgestellt, dass ~1000 Datensätze in der Datenbank fehlen. Komplette Rückverfolgung der Pipeline - die Datensätze wurden von der API nicht korrekt verarbeitet. In den Logs war das auch feststellbar, allerdings habe ich diese nicht genau geckeckt. Daraus lerne ich. Die Datensätze sind nun geparst, allerdings muss ich nun wieder die Personen für diese Datensätze korrekt mit vorhandenen Einträgen verknüpfen.

## claude beschreibungen

**Variante 1 — Ich-Form, mit Großvater (~75 Wörter)**

Mein Großvater, ein pensionierter Bibliothekar, hatte seine private Büchersammlung über Jahre in rund 50 Word-Dokumenten nach RAK-Standard katalogisiert. Aus diesen Dokumenten habe ich ehrenamtlich eine strukturierte Datenbank aufgebaut und daraus eine vollständige Webanwendung mit Front- und Backend, Datenbank und Login entwickelt. Python und die nötigen Grundlagen habe ich mir dafür autodidaktisch erarbeitet. Die Anwendung ist so gestaltet, dass auch ein 90-jähriger Nutzer ohne technische Vorkenntnisse damit arbeiten kann.

---

**Variante 2 — Ich-Form, Privatbibliothek (~120 Wörter)**

Ausgangspunkt war der über Jahre gewachsene Katalog einer privaten Büchersammlung, den ein pensionierter Bibliothekar in rund 50 Word-Dokumenten nach dem älteren RAK-Standard geführt hatte. Über mein wachsendes Interesse an der Arbeit mit Daten habe ich beschlossen, diesen Katalog als eigenes Projekt aufzuarbeiten. Ehrenamtlich und autodidaktisch habe ich mir dafür Python erarbeitet und die unstrukturierten Dokumente Schritt für Schritt in eine strukturierte Datenbank überführt. Darauf aufbauend entstand eine vollständige Webanwendung mit Datenbank, Front- und Backend sowie Login-Funktion. Das gesamte Projekt habe ich allein umgesetzt. Ein besonderer Anspruch war die Bedienbarkeit: Die Anwendung kann auch von einem 90-jährigen Endnutzer ohne technische Vorkenntnisse verwendet werden.

---

**Variante 3 — unpersönlich, mit Großvater (~95 Wörter)**

Über Jahre hatte ein pensionierter Bibliothekar seine private, stetig wachsende Büchersammlung in rund 50 Word-Dokumenten nach RAK-Standard katalogisiert. Aus diesem Bestand entstand ein ehrenamtliches Projekt: die Überführung der unstrukturierten Dokumente in eine strukturierte Datenbank. Die dafür nötigen Python-Kenntnisse wurden autodidaktisch erarbeitet. Auf Basis der Datenbank wurde eine vollständige Webanwendung mit Front- und Backend sowie Login-Funktion entwickelt, vollständig in Eigenregie umgesetzt. Ein zentrales Gestaltungsziel war die Zugänglichkeit für einen 90-jährigen Endnutzer ohne technische Vorkenntnisse.

---

**Variante 4 — unpersönlich, Privatbibliothek (~140 Wörter)**

Grundlage des Projekts war der Katalog einer privaten Büchersammlung, der über Jahre in rund 50 Word-Dokumenten nach dem älteren RAK-Standard geführt worden war. Das aus persönlichem Interesse an der Arbeit mit Daten entstandene, ehrenamtliche Vorhaben hatte zum Ziel, diesen gewachsenen Bestand aus unstrukturierten Dokumenten in eine strukturierte Datenbank zu überführen. Die dafür erforderlichen Python-Kenntnisse wurden autodidaktisch erarbeitet. Auf Basis der Datenbank entstand eine vollständige Webanwendung mit Datenbank, Front- und Backend sowie Login-Funktion. Von der Datenmodellierung über das Backend bis zur Benutzeroberfläche wurde das gesamte Projekt eigenständig umgesetzt. Besonderes Augenmerk lag auf der Benutzerfreundlichkeit: Die Anwendung ist so gestaltet, dass auch ein 90-jähriger Endnutzer ohne technische Vorkenntnisse damit arbeiten kann.

## Bullets für CV

### IT allgemein

bibliopa – von Word zur Datenbank
Autodidaktische Weiterbildung | 09/2025–aktuell

- Konzeption und Umsetzung einer vollständigen ETL-Pipeline (Python), die ~13.000 bibliografische Datensätze aus ~50 unstrukturierten Word-Dokumenten in eine relationale PostgreSQL-Datenbank überführt
- Anbindung der Claude API zum strukturierten Parsen der Rohdaten; iterative Verbesserung von Prompts und Datenschema zur Erhöhung der Ergebnisqualität
- Entwurf des Datenbankschemas inkl. sprechender IDs zur exakten Rückverfolgbarkeit jedes Datensatzes zum Originaldokument
- Deduplizierung von ~17.500 Personen-Rohdatensätzen mittels Fuzzy-Matching, inkl. Umgang mit nicht standardisierten Transliterationen slawischer Namen
- Versionierte Schema-Migrationen (Alembic) und Branch-basiertes Arbeiten für sichere Umbauten im laufenden Betrieb
- Full-Stack-Webanwendung (Next.js, TypeScript, React) zur Anzeige und Verwaltung der Sammlung; autodidaktisch erarbeitet, laufend in Weiterentwicklung

### Data Engineering

bibliopa – von Word zur Datenbank
Autodidaktische Weiterbildung | 09/2025–aktuell

- Design und Implementierung einer ETL-Pipeline (Python) für ~13.000 bibliografische
Datensätze aus ~50 heterogenen Word-Dokumenten in ein normalisiertes PostgreSQL-Schema
- Konsolidierung zweier divergierender Rohdaten-Versionen inkl. Encoding-Bereinigung im Extract-Schritt zur Vermeidung korrumpierter Outputs
- LLM-gestütztes Parsing über die Claude Batch API; datengetriebene Iteration von
Prompt und Schema, KI-Korrekturen über differenzierte Flags nachvollziehbar markiert
- Entity Resolution: Deduplizierung von ~17.500 Personen-Rohdatensätzen per
Fuzzy-Matching; staged Matching und normalisierte Schlüssel zur Reduktion von
False Positives
- Sprechende, deterministische IDs (composite_id) für vollständige Data Lineage vom
Datenbankeintrag zurück zum Originaldokument
- Versionierte Migrationen mit Alembic; Neon-Branching für gefahrlose destruktive
Operationen am Datenbestand

<aside>
💡

I took a messy, real-world data problem, designed and built the whole process myself, learned the necessary technologies along the way, and iteratively improved the pipeline as I discovered problems in the data and in my own approach.

I can operate at the boundary between domain expert and technical system, even when neither side naturally speaks the other's language.

</aside>

## ChatGPT

### Conversation

- **What is the actual current technical stack of bibliopa?**
    
    From the material I have, I understand:
    
    - Python
    - PostgreSQL
    - Claude API / Claude Batch API
    - Alembic
    - database branching (Neon?)
    - Next.js / React / TypeScript for the application
    - Jupyter somewhere in the workflow
    
    Is that accurate, and is there anything important missing, particularly Python libraries you actually used for parsing, matching or data processing?
    
    - rapidfuzz
    - Neon
    - dBeaver
    - react-aria
- **How much do you want the bullets to emphasise that this is a self-directed learning project?** Your current CV says *„Autodidaktische Weiterbildung“*. I think that's useful context, but I don't think the bullets themselves need to repeatedly say that you taught yourself. Is that how you see it?
    
    I don’t think that needs to be repeated too much - the main issue is that I don’t have any formal qualifications for data engineering or anything in the sector but I think that in this area I really have finally found something I could be good at. I need to convey that I can and have created a project of this dimension all on my own, learning all of the necessary things to get it to work, failed and failed better, etc. I have no idea how to do this, but this needs to be the salient point. In the project page of the web app I can go into a bit more depth as well.
    
- **For the IT-general version, how much should the web application count?** My initial instinct is that it should get **one bullet at most**, because the interesting differentiator of this project is clearly the data work rather than “I also built a Next.js app”. But if you're applying to general software-development roles, we could give it slightly more weight.
    
    Yes, that is what I tend towards as well. I really noticed that I found the web app building not interesting at all - and while at the beginning I did find it important to make sure I understand the structure, I mostly delegated writing that code to AI - on the data side, I really tried to do as much as possible on my own (using AI to teach me how to do that), and I’m a lot more motivated and interested in learning the ins and outs, even when I hit rough patches.
    
- **For the Data Engineering version, are you comfortable presenting this explicitly as an ETL/data pipeline project even though it is a personal project and not production infrastructure?**
I think yes, but I want to distinguish between *“I designed and implemented an ETL pipeline”* and inflated formulations such as *“production-grade data engineering pipeline”*, which I would avoid.
Yes, the ETL/data pipeline really is the heart of the entire project, and the deduplication and entity resolution has proved to be a complicated and time consuming part where I’d really like to learn how to better do that. And definitely avoid inflated formulations - my project is not “production-grade” but somewhat messy work in progress (also not how I’d put it in a CV)
- One potentially important distinction: **the ~13,000 / ~15,000 figures.**
Your brain dump says ~15,000 records including cross-references, while the example says ~13,000 bibliographic records. Which figure should we use on the CV, and what exactly does it represent?
Let’s go with ~13000.
- **Fuzzy matching:** did you actually implement the matching logic yourself in Python (e.g. using a library/algorithm and your own matching stages/thresholds), or was it primarily a library/API that you configured and then manually reviewed?This affects how strongly I'd describe the entity-resolution work.
The process was arduous, over a number of jupyter notebooks, and mainly manual at the beginning (e.g. checking whether the name was stored as “first last” or “last, first” etc.), then I added rapidfuzz and played around with different thresholds to try and find spelling variants of the same names (e.g. Tolstoy, Dostojewsky), then a lot of manual research to resolve last names with missing first names to map them to the correct person in contrast to single names like “Aristotle”, a keyword-based identification of organisations, … And now I need to do the same thing again for the missing 1000 records…
- **The current ~1,000 missing records:** I would **not mention this on the CV**. It is useful evidence for your own understanding of the project and a good interview story about data lineage/log monitoring, but “I discovered 1,000 records were missing” is not a useful CV bullet unless framed very carefully. Are you happy for me to leave that entirely out?
Yes, that was added as information only, it doesn’t need to be in the CV.
- Finally, **how many bullets do you actually have room for under bibliopa?** My recommendation would be around **4–5 bullets per version**, rather than trying to squeeze six or seven into it.
Yes. 4-5 sound good.

## ChatGPT Bullets

version 10000000004023121408315379

- Unterschiedliche und sich verändernde Datenstände aus rund 50 Quelldokumenten abgleichen und für die Verarbeitung aufbereiten.
- Deterministische IDs entwickeln, um Datensätze eindeutig zuzuordnen und über mehrere Verarbeitungsschritte hinweg nachvollziehbar zu halten.

Mehrfaches Aufbereiten und Abgleichen der uneinheitlichen Quelldaten; iterative Anpassung des Datenschemas für den LLM-gestützten Parsingprozess

Deterministische IDs für Bücher und Personen entwickeln, um die Rückverfolgbarkeit der Datensätze durchwegs zu gewährleisten; parallele Verwendung autogenerierter numerischer IDs für bessere Performance

Weiterentwicklung des Parsers für den Re-Import eines aktualisierten Datenstandes, z. B. eigenständiges Ausbessern von Tippfehlern in Kombination mit Kontroll-Flags

Zusammenführung bereits bestehender deduplizierter Personendaten mit neu verarbeiteten Daten, um unnötige Kosten zu vermeiden

Entity Resolution auf Basis programmatischer und probabilistischer Methoden (splink, RapidFuzz)

- Verarbeitungsergebnisse analysieren und Datenbereinigung, Parser und Datenschema gezielt weiterentwickeln.
- Neue Datenstände mit bereits verarbeiteten Daten und bestehenden Beziehungen abgleichen und zusammenführen.
- Unterschiedliche Personenangaben normalisieren, mögliche Dubletten über verschiedene Verfahren erkennen und uneindeutige Fälle durch manuelle Recherche prüfen.

## IT allgemein — latest

**bibliopa – vom Zettelkatalog zur Datenbank**

*Autodidaktische Weiterbildung | 09/2025–aktuell*

- Eigenständige Konzeption und schrittweise Umsetzung eines Softwareprojekts zur Überführung einer über Jahre gewachsenen Büchersammlung in eine relationale Datenbank – von der Rohdatenaufbereitung bis zur Webanwendung
- Entwicklung einer Python-basierten Datenpipeline für rund 13.000 bibliografische Datensätze; Verarbeitungsergebnisse analysiert und Parsing, Datenaufbereitung und Datenmodell in mehreren Durchläufen gezielt verbessert
- Konsolidierung und Re-Import mehrerer, nicht vollständig übereinstimmender Datenstände; Entwicklung sprechender, deterministischer IDs zur Rückverfolgung von Datensätzen und zum Abgleich neuer Daten mit bereits verarbeiteten Informationen
- Schrittweise Bereinigung und Zusammenführung von Personendaten mit Normalisierung, RapidFuzz und manueller Recherche; dabei wiederholt neue Datenqualitätsprobleme identifiziert und die Verarbeitungslogik entsprechend erweitert
- Übersetzung der gewachsenen Arbeitsweise und fachlichen Anforderungen eines pensionierten Bibliothekars in eine digitale Anwendung; technische Möglichkeiten verständlich vermittelt und die Anwendung gemeinsam mit dem Nutzer an die tatsächliche Verwendung angepasst

## IT allgemein — version A

**bibliopa – von Word zur Datenbank**

*Autodidaktische Weiterbildung | 09/2025–aktuell*

- Eigenständige Konzeption und Entwicklung einer Datenpipeline, die rund 13.000 bibliografische Datensätze aus knapp 50 heterogenen Word-Dokumenten extrahiert, aufbereitet und in eine PostgreSQL-Datenbank überführt
- Iterative Weiterentwicklung des Parsings mit Python und der Claude API: Fehler aus vorherigen Durchläufen analysiert, Rohdatenaufbereitung und Datenschema angepasst und bestehende Ergebnisse gezielt weiterverwendet
- Entwicklung eines nachvollziehbaren Datenmodells mit sprechenden, deterministischen IDs, das die Rückverfolgung von Datenbankeinträgen zu den ursprünglichen Dokumenten ermöglicht und auch das Zusammenführen neu eingelesener Daten unterstützt
- Aufwändige Konsolidierung und Deduplizierung von Personendaten: Normalisierung unterschiedlicher Schreibweisen, Fuzzy-Matching mit RapidFuzz sowie manuelle Recherche und Zuordnung uneindeutiger Datensätze
- Aufbau einer Webanwendung mit Next.js, React und TypeScript zur Suche und Darstellung der Daten; Datenbankschema und Migrationen mit Alembic, Entwicklung und Tests auf separatem Neon-Branch

### IT allgemein — version B

This one puts slightly more emphasis on **independent problem-solving and learning**, which I think may actually be the stronger version for your particular CV.

- Konzeption und schrittweise Umsetzung eines eigenen Softwareprojekts zur Überführung einer über Jahre gewachsenen, unstrukturierten Büchersammlung in eine relationale Datenbank – von der Rohdatenaufbereitung bis zur Webanwendung
- Entwicklung einer Python-basierten Datenpipeline für rund 13.000 bibliografische Datensätze; dabei wiederholt Probleme in Quelldaten, Parsing und Datenmodell analysiert und die einzelnen Verarbeitungsschritte iterativ verbessert
- Verarbeitung der Rohdaten über die Claude API und Entwicklung eines Schemas zur kontrollierten Weiterverwendung bereits verarbeiteter Daten, einschliesslich nachvollziehbarer Kennzeichnung automatisierter Korrekturen
- Entwicklung eigener Verfahren zur Bereinigung und Zusammenführung von Personendaten mit RapidFuzz; Kombination aus automatisiertem Matching, regelbasierten Verfahren und manueller Recherche bei mehrdeutigen oder unvollständigen Angaben
- Selbstständiger Aufbau der dafür notwendigen Kenntnisse in Python, Datenmodellierung und Datenbankmigrationen sowie Entwicklung einer ergänzenden Webanwendung mit Next.js/React

---

# Data Engineering — edited version

**bibliopa – ETL & Datenmodellierung**

*Autodidaktische Weiterbildung | 09/2025–aktuell*

- Konzeption und Implementierung einer Python-basierten ETL-Pipeline für ~13.000 bibliografische Datensätze aus knapp 50 heterogenen Word-Dokumenten mit Überführung in ein relationales PostgreSQL-Datenmodell
- Iterative Weiterentwicklung der Pipeline auf Basis realer Verarbeitungsergebnisse: Bereinigung von Rohdaten und Encoding-Problemen, Anpassung von Datenschema und LLM-gestütztem Parsing sowie vollständiger Re-Import eines aktualisierten Quelldatenstands
- Abgleich und Zusammenführung mehrerer Datenstände über neu erzeugte und bestehende `composite_id`s, um bereits transformierte Daten und Beziehungen weiter verwenden zu können
- Entity Resolution für Personendaten: Normalisierung von Namensvarianten, Fuzzy-Matching mit RapidFuzz, regelbasierte Identifikation von Organisationen und Erkennung zusammengeführter oder unvollständiger Personeneinträge, ergänzt durch manuelle Recherche
- Entwicklung eines schrittweise verfeinerten Datenbereinigungs- und Matching-Prozesses; Versionierung des Datenbankschemas mit Alembic und Verwendung von separaten Neon-Branches für Re-Imports und strukturelle Änderungen

# Data Engineering — latest AI version

**bibliopa – ETL & Datenmodellierung**

*Autodidaktische Weiterbildung | 09/2025–aktuell*

- Konzeption und Implementierung einer Python-basierten ETL-Pipeline für rund 13.000 bibliografische Datensätze aus knapp 50 heterogenen Word-Dokumenten mit Überführung in ein relationales PostgreSQL-Datenmodell
- Iterative Weiterentwicklung der Pipeline auf Basis realer Verarbeitungsergebnisse: Bereinigung von Rohdaten und Encoding-Problemen, Anpassung von Datenschema und LLM-gestütztem Parsing sowie vollständiger Re-Import eines aktualisierten Quelldatenstands
- Abgleich und Zusammenführung mehrerer Datenstände über neu erzeugte und bestehende `composite_id`s, um bereits transformierte Daten und Beziehungen wiederzuverwenden und nicht bei jedem Re-Import vollständig neu aufzubauen
- Entity Resolution für Personen- und Organisationsdaten: Normalisierung von Namensvarianten, Fuzzy-Matching mit RapidFuzz, regelbasierte Identifikation von Organisationen und Erkennung zusammengeführter oder unvollständiger Personeneinträge, ergänzt durch manuelle Recherche
- Entwicklung eines schrittweise verfeinerten Datenbereinigungs- und Matching-Prozesses; Versionierung des Datenbankschemas mit Alembic und Arbeiten auf separaten Neon-Branches für Re-Imports und strukturelle Änderungen

# Data Engineering — version A

**bibliopa – von Word zur Datenbank**

*Autodidaktische Weiterbildung | 09/2025–aktuell*

- Konzeption und Implementierung einer Python-basierten ETL-Pipeline für rund 13.000 bibliografische Datensätze aus knapp 50 heterogenen Word-Dokumenten mit Überführung in ein normalisiertes PostgreSQL-Datenmodell
- Konsolidierung und wiederholtes Einlesen veränderter Rohdaten: Bereinigung von Encoding- und Formatierungsproblemen im Extract-Schritt sowie Abgleich neuer Daten mit bereits transformierten Datensätzen zur Vermeidung unnötiger Neuverarbeitung
- LLM-gestütztes Parsing über die Claude API; Analyse der Ergebnisse aus mehreren Durchläufen und iterative Anpassung von Datenaufbereitung, Schema und Prompting, um die Qualität der strukturierten Daten zu verbessern
- Entity Resolution für rund 17.500 Personen-Rohdatensätze: Normalisierung unterschiedlicher Namensformen, Fuzzy-Matching mit RapidFuzz, regelbasierte Identifikation von Organisationen sowie manuelle Recherche bei fehlenden oder mehrdeutigen Angaben
- Entwicklung deterministischer, sprechender IDs zur Data Lineage und zum sicheren Zusammenführen und Reprozessieren von Daten; Versionierung des Schemas mit Alembic und Arbeiten auf separaten Neon-Datenbank-Branches

### Data Engineering — version B

- Aufbau einer eigenen ETL-Pipeline in Python, um rund 13.000 bibliografische Datensätze aus knapp 50 unterschiedlich strukturierten Word-Dokumenten in ein relationales PostgreSQL-Schema zu überführen
- Entwicklung eines reproduzierbaren Prozesses für die Verarbeitung mehrerer, nicht vollständig identischer Rohdatenstände; inklusive Datenbereinigung, Matching bereits verarbeiteter Datensätze und gezieltem Reprocessing statt vollständiger Neuverarbeitung
- Einsatz der Claude Batch API für die Strukturierung unstrukturierter bibliografischer Angaben; Verarbeitungsergebnisse systematisch ausgewertet und Datenvorbereitung, Schema und Prompt iterativ angepasst
- Entity Resolution als eigenständiger Verarbeitungsschritt: schrittweise Entwicklung von Normalisierungs- und Matching-Verfahren mit RapidFuzz, ergänzt durch regelbasierte Zuordnung und manuelle Validierung bei komplexen Fällen wie nicht standardisierten Transliterationen oder fehlenden Vornamen
- Aufbau von Mechanismen für Nachvollziehbarkeit und sichere Datenänderungen: deterministische IDs mit Rückbezug auf die Quelldaten, Alembic-Migrationen und separate Neon-Branches für Umbauten und Reprocessing

## für Anschreiben