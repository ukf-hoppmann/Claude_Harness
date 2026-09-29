# STORY-037 — Testkonventionen: Ablage, Gliederung, Test-Arten

## 2026-09-28 — Anforderungen des Owners und Gliederungsvorschlag

### Discussed

- Bisher ist nur geregelt, wann der Test zuerst entsteht und wie viel nach einer Änderung getestet wird (Skill decomposition). Ablage, Namen, Test-Arten und Testebenen fehlen; die Testebenen aus EPIC-004 wurden nie umgesetzt.
- Owner-Anforderung: alle Tests liegen in einem Testordner, keine Inline-Tests, weil der Owner sie sonst nicht findet.
- Owner-Anforderung: der Testordner bekommt eine ordentliche Gliederung.
- Owner-Anforderung: Trennung in Implementierungstests (baut der Agent für sich) und Funktionalitätstests (für den Owner). Beispiele aus EZF-Backend: prüfen, ob die integrierten Filter richtig umgesetzt sind; nach Einführung von Load und Cache prüfen, ob eine größere Sequenz die richtigen Daten liefert.
- Vorschlag Gliederung: tests/implementation/unit/ (eine Einheit, spiegelt die Quellstruktur), tests/implementation/integration/ (mehrere Komponenten, echte Dateien, lokaler Testserver), tests/functional/<funktion>/ (je fachliche Funktion ein Ordner, z. B. filters/, load_cache/, Dateien nach Szenario benannt: test_<szenario>), tests/fixtures/ (gemeinsame Testdaten), tests/helpers/ (gemeinsamer Testcode).
- Vorschlag Funktionalitätstests: fachlich benannt statt nach Modul; jeder Test sagt in einem Satz, welches Verhalten er prüft; Ausgabe bei Fehlschlag zeigt erwartete und erhaltene Daten; eigenes Kommando, um nur sie oder nur eine Funktion laufen zu lassen; der Agent schreibt sie auf Wunsch des Owners oder schlägt sie bei neuen fachlichen Funktionen vor.
- Abgelehnter Anhänger an EPIC-004: der Server nimmt unter dem abgeschlossenen Epic kein Kind an, auch kein optionales. Die Story steht deshalb vorerst ohne Parent.

### Decided

- Alle Tests liegen in einem Testordner je Projekt (bei Teilprojekten je Teilprojekt); keine Inline-Tests.
- Zwei Test-Arten: Implementierungstests und Funktionalitätstests.

### Open

- Gliederungsvorschlag bestätigen oder anpassen.
- Laufen Funktionalitätstests im normalen Gesamtlauf mit, oder nur auf Aufruf (z. B. weil sie echte Daten oder Dienste brauchen)?
- Wie werden Testordner und Kommandos je Projekt festgehalten: fest im Plugin, in der Harness-Config oder in einer Projektvorlage?
- Umgang mit Frameworks, die eine eigene Ablage erwarten (z. B. __tests__ neben dem Code bei Jest).
- EPIC-004 wiedereröffnen und die Story als optionales Kind einhängen?

## 2026-09-28 — Unter EPIC-004 eingehängt

### Decided

- Auf Wunsch des Owners EPIC-004 wieder geöffnet und die Story als optionales Kind (Required for parent: No) eingehängt; die offene Frage dazu ist damit erledigt.

## 2026-09-29 — Offene Fragen geklärt

### Discussed

- Der Owner hat die vier offenen Fragen und den vermuteten Widerspruch beim Feld Required for parent beantwortet.

### Decided

- Die vorgeschlagene Gliederung gilt: tests/implementation/unit/, tests/implementation/integration/, tests/functional/<funktion>/ mit Dateien test_<szenario>, tests/fixtures/, tests/helpers/.
- Funktionalitätstests gehören dem Owner. Sie laufen nicht im normalen Gesamtlauf mit, sondern nur auf Aufruf, und werden in der Regel auf Wunsch des Owners gebaut.
- Funktionalitätstests sind so gebaut, dass sich mit wenig Aufwand verschiedene Szenarien prüfen lassen: Die Eingaben (z. B. die Filtereinstellungen beim VariantFilter) lassen sich über Parameter setzen, und der Test zeigt den Output, damit der Owner das Verhalten selbst beurteilen kann.
- Der Testordner liegt in der Regel neben src/. Das ist der Standard in der Harness-Config und gilt auch, wenn dort nichts eingetragen ist.
- Besonderheiten eines Frameworks (z. B. eigene Test-Ablage wie __tests__ bei Jest) werden erwähnt, sobald sie in einem Projekt auftreten. Dann wird im Einzelfall entschieden; das Plugin regelt sie nicht im Voraus.
- Required for parent ist bewusst Yes; der Owner hat es so gesetzt. Der Eintrag vom 2026-09-28 zu 'No' ist damit überholt.

## 2026-09-29 — Abschlusskriterien ergänzt

### Decided

- Mit Zustimmung des Owners ergänzt: Funktionalitätstests laufen nicht im Gesamtlauf mit, ihre Szenarien lassen sich über Parameter setzen, und sie zeigen den Output.
