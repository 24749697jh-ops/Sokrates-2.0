# Sokrates 2.0 – iPad Edition

Sokrates 2.0 ist ein vollständiger Neustart der Kernarchitektur.

## Grundprinzip

Eine Aufgabe wird beim Start genau einmal analysiert:

1. Thema erkennen
2. Aufgabentyp erkennen
3. Gesuchtes bestimmen
4. Gegebenes bestimmen
5. passende Formeln festlegen
6. mit der Phase VERSTEHEN beginnen

Spätere Schülerantworten können die erkannte Aufgabenart nicht verändern.

## Getrennte Komponenten

- `task_analysis.py`: analysiert ausschließlich die ursprüngliche Aufgabe
- `teacher_engine.py`: steuert Verstehen → Planen → Rechnen → Prüfen
- `math_input.py`: stabile Text- und Mathematikeingabe
- `formula_library.py`: ausschließlich zur Analyse passende Formeln
- `ui.py`: Aufgabenkarte, Chat und Formeldarstellung
- `app.py`: verbindet die Komponenten

## Wichtige Verbesserungen

- Die Aufgabe bleibt während der Bearbeitung sichtbar.
- Die erste Frage gehört immer zur Phase Verstehen.
- Formelsammlung und Teacher Engine verwenden dieselbe gespeicherte Analyse.
- Normale Texteingabe und Mathematik-Tastatur haben getrennte Zustände.
- Keine Unterordner: vollständig für den GitHub-Upload auf dem iPad geeignet.

## Installation

1. Am besten ein neues GitHub-Repository erstellen, zum Beispiel `Sokrates-2.0`.
2. ZIP entpacken.
3. Alle Dateien direkt ins Hauptverzeichnis hochladen.
4. In Streamlit Community Cloud `app.py` auswählen.
5. Den bestehenden Secret verwenden:

```toml
OPENAI_API_KEY="dein-api-key"
```

6. Nach dem Start muss oben `Installierte Version: 2.0.0` stehen.
