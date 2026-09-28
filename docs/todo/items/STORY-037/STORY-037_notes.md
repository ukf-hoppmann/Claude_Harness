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
