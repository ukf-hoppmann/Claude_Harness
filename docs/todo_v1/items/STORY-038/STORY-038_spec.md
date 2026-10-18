# Spec: Modulschalter notes in Config und Session-Start

## Was und warum

Das Modul `notes` wird wie `todo` oder `daily` ein- und ausschaltbar. Es hat
keine eigenen Einstellungen: Prüf-Intervall und Uhrzeiten entscheidet der
Viewer beziehungsweise Claude im Gespräch. Der Session-Start nennt nur, dass
das Modul aktiv ist und welcher Skill gilt.

## Betroffene Dateien

- `plugin/scripts/harness_config.py`: `notes` als bekanntes Modul (Validierung,
  Architekturregel 4).
- `plugin/scripts/session_start.py`: Konstante `NOTES_HINT` nach dem Muster von
  `TODO_HINT`: "Notes: via ToDo-Viewer API; rules in skill claude-harness:notes
  (load it when asked to remember, remind, or look at due notes)". Einzelprojekt:
  eine Zeile mit API-URL aus `[todo].api_url`; mehrere Projekte: der Hinweis
  einmal, Modul in der Projektzeile.
- `plugin/templates/config.toml`: Schalter mit Kommentar, standardmäßig aus.
- `plugin/scripts/config_update.py` und Skills `init`, `update`: Schalter
  anbieten beziehungsweise abgleichen.
- `docs/techdocs/configuration.md`: Zeile `modules.notes`.
- Tests: `tests/implementation/unit/test_config.py`, Tests des Session-Starts.

## Grenzen

- Kein Hook außer der vorhandenen Session-Start-Zeile, kein Netzwerkzugriff
  (Architekturregel 2), keine Abfrage von Fälligem.
- Der Skill selbst entsteht in STORY-040; bis dahin darf der Hinweis nicht auf
  einen fehlenden Skill zeigen: Die Zeile erst aktivieren, wenn der Skill im
  Release liegt, oder beide Stories in einem Release zusammen ausliefern.

## Abnahme

`python3 -m unittest discover -s tests/implementation -t tests` grün;
`notes = true` ergibt die Zeile, `false` oder fehlend keine; ein unbekanntes
Modul bleibt ein Fehler.
