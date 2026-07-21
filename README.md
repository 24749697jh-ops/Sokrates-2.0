# Sokrates 2.1 – iPad Edition

Sokrates 2.1 enthält erstmals einen echten, eigenen Mathematik-Editor.

## Neue Eingabe

Es gibt nur noch ein einziges Eingabefeld.

- Normale Texteingabe und Mathematik stehen im selben Feld.
- `²`, `³`, `π`, `√`, Operatoren und griechische Buchstaben werden direkt
  an der aktuellen Cursorposition eingefügt.
- Markierter Text kann mit Bruch-, Potenz- und Wurzelvorlagen umschlossen werden.
- Die Eingabe wird nicht mehr zwischen zwei Feldern aufgeteilt.

## Technische Lösung

Die Mathematik-Eingabe ist als echtes Streamlit Custom Component gebaut.
Damit sie auf dem iPad ohne Ordner hochgeladen werden kann, ist sie in dieser
einzelnen Wheel-Datei verpackt:

`sokrates_math_editor-0.1.0-py3-none-any.whl`

Diese Datei muss zusammen mit den Python-Dateien direkt ins Hauptverzeichnis
des GitHub-Repositories hochgeladen werden.

## Installation

1. Alle Dateien aus dem ZIP direkt in das Hauptverzeichnis von `Sokrates-2.0`
   hochladen und gleichnamige Dateien ersetzen.
2. Unbedingt auch `sokrates_math_editor-0.1.0-py3-none-any.whl` hochladen.
3. `requirements.txt` ebenfalls ersetzen.
4. Streamlit vollständig rebooten.
5. Oben muss `Installierte Version: 2.1.0` stehen.

## Dateien

- app.py
- config.py
- formula_library.py
- models.py
- requirements.txt
- task_analysis.py
- teacher_engine.py
- ui.py
- sokrates_math_editor-0.1.0-py3-none-any.whl
