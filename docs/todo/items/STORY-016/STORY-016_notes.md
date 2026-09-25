# STORY-016 – Notizen

## Summary
Secrets landen nie im Code, sondern in einer zentralen, gitignorten Config;
eine Template-Datei zeigt, was konfigurierbar ist. Welche Config genutzt
wird, wird im Zweifel mit dem Owner geklärt.

## Discussed (2026-09-25)
- Ursprünglich als Erkennungs-/Scanning-Thema gedacht (Logs, Dateien,
  Git-Commits). Owner-Feedback: nicht relevant, da keine AWS-artigen
  Standard-Secrets im Einsatz sind, sondern eigene DB-/Service-Secrets.
- Kernpunkt ist Verhalten beim Schreiben von Code: Secrets nie hartkodieren,
  sondern in eine zentrale, nicht versionierte Config auslagern.
- Klargestellt: Der Code verweist zur Laufzeit auf die echte Config, nicht
  auf das Template. Das Template dient nur der Dokumentation möglicher Werte
  (z. B. `.env.example`).
- Klargestellt: Welche Config ein Secret bekommt, ist im Einzelfall zu
  klären, außer es gibt bereits eine eindeutige Zuordnung. Die KI weist
  aktiv darauf hin, bevor sie ein Secret irgendwo einträgt.
- Verwandtes, aber getrenntes Thema erkannt: hartkodierte Pfade/Config-Werte
  allgemein (Maintainability, nicht Security) — dafür wird eine eigene neue
  Story unter `EPIC-004` angelegt.

## Decided (2026-09-25)
- Regel als Abschnitt "7. Secrets" in `docs/development/architecture.md`
  aufgenommen (bindend, da vom Architecture-Hook vor jeder Code-Änderung
  gelesen).
- Status auf `Awaiting confirmation` gesetzt, da die Regel vollständig
  dokumentiert ist.

## Open
- Neue Story für "keine hartkodierten Pfade/Config-Werte" mit dem Owner
  umreißen.
