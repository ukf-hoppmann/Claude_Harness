# STORY-052 — Branch-Stand beim Start einer Cloud-Session mit origin abgleichen

## State

- Goal/Status: Cloud-Session gleicht beim Start den Branch mit origin ab oder meldet die Abweichung. Umgesetzt und released (v0.12.8). Vom Owner am 2026-11-12 abgeschlossen; Kriterium 7 nur als Schweigen bei gleichem Stand gesehen, Vorspul-Fall nicht belegt.
- Next step: keiner; der Owner meldet sich, falls der Abgleich in der Praxis nicht funktioniert.
- Open:
  - Autoren-Hinweis eines Hooks in der Cloud-Session (Umschreiben mit --reset-author): welcher Hook, nicht aus dieser Story (2026-11-05)
- Decided:
  - Logik in cloud_sync.py, Aufruf zu Beginn von session_start.py (2026-11-04)
  - Abschaltbar über cloud.sync, Standard true (2026-11-04)
  - Nie überschreiben, reset --hard nur auf Rückfrage, kein --unshallow (2026-11-04)
  - Ausnahme von Architekturregel 2 und 5 für Cloud-Sessions freigegeben (2026-11-04)
  - Release als Patch v0.12.8 (2026-11-04)
  - Ursache in ezf-ui: alter Cache, kein Rebase/Force-Push; 85/73 und 'forced' sind Shallow-Artefakte (2026-11-05)
  - Abschluss durch den Owner ohne Beleg des Vorspul-Falls (2026-11-12)
- References: STORY-052_spec.md; EPIC-010; STORY-047; Merge 5968aba; docs/daily/2026-11-04_daily.md

State confirmed after entry 2026-11-12 — Kriterium 7 und Abschluss durch den Owner (04ec53028518)

## 2026-11-04 — Anlass, Ort der Lösung und Architektur-Ausnahme

### Discussed

- Anlass: Cloud-Session von ezf-ui startete auf gecachtem Shallow Clone vom 2026-11-02, origin 86 Commits weiter, kein gemeinsamer Vorfahr. Der Session-Start der Kopie gleicht den Branch nicht ab.
- Ort: eigener Hook in hooks.json (läuft parallel zu session_start.py, Reihenfolge nicht gesichert) gegen Aufruf als erster Schritt in session_start.py (Reihenfolge gesichert). Setup-Skript der Cloud-Umgebung verworfen: pro Projekt von Hand, nicht im Plugin.
- Konflikt: git fetch verletzt Architekturregel 2 (kein Netz), git merge --ff-only Regel 5 (nicht ins Projekt schreiben).

### Decided

- Abgleich in plugin/scripts/cloud_sync.py, aufgerufen zu Beginn von session_start.py, nur in Cloud-Sessions beim Start.
- Abschaltbar über cloud.sync (Standard true).
- Nie überschreiben; git reset --hard nur nach Rückfrage beim Nutzer; kein --unshallow.
- Der Besitzer gibt die auf Cloud-Sessions begrenzte Ausnahme von Regel 2 und 5 frei; sie wird in architecture.md festgehalten.

### Open

- Ursache in ezf-ui belegen (Rebase/Force-Push oder alter Cache): Commit-Texte beider Stände vergleichen.

## 2026-11-04 — Umgesetzt und released (v0.12.8)

### Discussed

- Umsetzung im Worktree in vier Abschnitten: Architektur-Ausnahme (6afacad), cloud.sync (76278f1), cloud_sync.py mit Tests gegen ein lokales Bare-Repo (dda7deb), Einbindung in session_start.py samt Techdocs und README (a7da016), Ende-zu-Ende-Test des exportierten SessionStart-Befehls (4db25ec). Merge 5968aba, Release v0.12.8 (6c8b9f1), nicht gepusht.
- Abweichung vom Plan: Patch statt Minor, weil die SemVer-Regeln eine neue Einstellung und Teilfunktion einer bestehenden Funktion als Patch einstufen.
- Detail: Nach einem Abgleich liest der Session-Start Config und Dokumente neu, damit seine Zeilen den neuen Stand zeigen. Git läuft in einer eigenen Prozessgruppe, damit ein Zeitlimit auch ssh oder https-Helfer beendet.

### Decided

- Kriterien 1 bis 6 erfüllt und mit Tests belegt (Suite 667 Tests OK, dazu 2 Ende-zu-Ende-Tests).

### Open

- Kriterium 7: Lauf in einer echten Cloud-Session; braucht Push des Harness und /claude-harness:update in ezf-ui.

## 2026-11-05 — Befund aus einer Cloud-Session von ezf-ui: Ursache belegt

### Discussed

- Der Owner hat in einer neuen Cloud-Session von ezf-ui gefragt, wie aktuell der Container ist. Antwort: lokal modularRefactor auf 0f5fc36 (Daily 2026-11-02, Cloud-Kopie des Harness-Plugins), origin auf 88f5829 (Merge vom 2026-11-05), Arbeitsbaum sauber.
- git merge-base nennt 0f5fc36 als gemeinsamen Vorfahren: origin ist nur vorausgelaufen, kein Rebase und kein Force-Push. Die Zahlen 85/73 und die Anzeige 'forced' sind Artefakte des Shallow Clones.
- Die Session hat nichts abgeglichen, weil die Cloud-Kopie des Plugins vom 2026-11-02 stammt und cloud_sync.py (v0.12.8) dort noch fehlt. Das ist das erwartete Verhalten und kein Fehler der Umsetzung.
- Der Fall (sauberer Baum, HEAD Vorfahr von origin) ist genau der Fall von Kriterium 2: cloud_sync.py würde per --ff-only vorspulen, sofern git merge-base nach dem flachen Fetch den Vorfahren findet.

### Decided

- Ursache in ezf-ui ist belegt: alter Cache der Cloud-Umgebung, kein Rebase oder Force-Push.

### Open

- Kriterium 7: Harness pushen, in ezf-ui /claude-harness:update ausführen und committen, neue Cloud-Session starten; erwartet wird die Vorspul-Zeile (oder bei Shallow-Problemen die Abweichungsmeldung).
- Der Autoren-Hinweis eines Hooks in der Cloud-Session (Umschreiben von 85 Commits mit --reset-author) stammt nicht aus dieser Story; zu klären, welcher Hook das ist.

## 2026-11-12 — Kriterium 7 und Abschluss durch den Owner

### Discussed

- Ausgabe einer frischen Cloud-Session (2026-11-12): REMOTE=true, cloud.sync=true, Plugin-Kopie 0.14.0 im Repo, HEAD gleich origin, keine Abgleichszeile. Das ist das erwartete Schweigen bei gleichem Stand (Kriterium 2), belegt aber nicht, dass der Abgleich lief.
- Der Vorspul-Fall ist nicht in einer echten Cloud-Session gezeigt worden. Ein manueller Hook-Lauf nach git reset --hard HEAD~1 wurde vorgeschlagen, nicht ausgeführt.

### Decided

- Der Owner schließt die Story ab, obwohl Kriterium 7 nicht im Vorspul-Fall belegt ist. Er meldet sich, falls der Abgleich in der Praxis nicht funktioniert (2026-11-12).
