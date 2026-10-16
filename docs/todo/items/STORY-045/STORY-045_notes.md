# STORY-045 — Ablauf zwischen Cloud, Git und lokalem Viewer festlegen

## 2026-10-16 — Befund aus den Cloud-Tests: Branches und Zuordnung

### Discussed

- Eine Cloud-Sitzung arbeitet auf einem Sitzungs-Branch claude/<name> ohne Upstream (Test 2, 2026-10-16). Änderungen an docs/todo erreichen main erst nach einem Merge (Pull Request oder lokal); erst dann kann der lokale Viewer sie lesen. Ein Repository ist nur dann beschreibbar, wenn es der Sitzung zugeordnet ist.

### Open

- Der Ablauf muss den Merge des claude/*-Branches nach main vor dem Viewer-Sync enthalten. Welcher Weg (Pull Request auf GitHub oder lokales Merge) Standard wird, entscheidet der Besitzer.
