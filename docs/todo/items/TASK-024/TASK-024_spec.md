# TASK-024 — Spec: Hooks für aktuellen Notes-Kopf und Protokoll-Reminder

Grundlage: STORY-051_spec.md (Absicherung des Kopfs). Nutzt die Funktionen
aus TASK-022 und den Session-State aus TASK-023.

## Umfang

- Stop-Hook Kopf (API-Modus; der Files-Modus läuft schon über
  `check_backlog.py` aus TASK-022): Für Items, deren Notes in der Session
  geändert wurden, Zustand beim Viewer abfragen; bei `stale` oder `missing`
  das Turn-Ende blockieren mit der Anweisung, den Kopf anzusehen und
  anzupassen (`put-state`) oder zu bestätigen (`confirm-state`). Kann der
  Viewer keine Köpfe oder ist er nicht erreichbar: nicht blockieren, einmal
  Hinweis ausgeben. Endlosschleife ausgeschlossen, weil Bestätigen den Zustand
  immer auf `current` setzt; zusätzlich `stop_hook_active` beachten wie die
  anderen Stop-Hooks.
- Reminder B (beide Modi): Ein Hook zählt die Turns seit dem letzten
  Notes-Eintrag zum aktiven Item; nach 5 Turns eine Erinnerung ("Aktives Item
  TASK-x, seit 5 Turns kein Notes-Eintrag"). Nie blockierend, höchstens einmal
  pro 5 Turns. Ereignis (UserPromptSubmit oder Stop) nach dem Muster der
  vorhandenen Reminder wählen.
- Registrierung in `plugin/hooks/hooks.json`; nur aktiv, wenn
  `[modules].todo = true`.
- Doku: Techdocs (Hooks), todo-Skill (was die Meldungen bedeuten).

## Abnahme

- Unit-Tests: blockiert bei `stale`/`missing` nur für in der Session
  geänderte Notes, nicht bei `current`, nicht ohne Viewer-Unterstützung;
  Reminder nach 5 Turns, nicht davor, nie blockierend.
