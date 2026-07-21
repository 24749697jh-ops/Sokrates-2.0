# Sokrates 2.1.2 – iPad Edition

## Behobener Fehler

In Version 2.1.0 wurden JavaScript und CSS des eigenen Mathematik-Editors
mit absoluten Pfaden eingebunden. Innerhalb des Streamlit-Komponentenfensters
konnten diese Dateien deshalb nicht geladen werden. Sichtbar war nur ein
leerer grauer Bereich.

Version 2.1.1 verwendet relative Asset-Pfade. Dadurch werden Textfeld und
Mathematik-Tastatur korrekt im Streamlit-Komponentenfenster geladen.

## Upload

Alle Dateien direkt ins Hauptverzeichnis hochladen und ersetzen.

Besonders wichtig:

- `app.py`
- `requirements.txt`
- `sokrates_math_editor-0.1.1-py3-none-any.whl`

Die alte Datei

`सokrates_math_editor-0.1.0-py3-none-any.whl`

wird nicht mehr benötigt. Falls sie noch im Repository liegt, kann sie
gelöscht werden.

Danach in Streamlit **Reboot app** ausführen.

Oben muss stehen:

`Installierte Version: 2.1.1`


## Korrektur in 2.1.2

- Der Button **„Aufgabe an Sokrates senden“** steht jetzt unmittelbar unter
  dem Mathematik-Editor.
- GoodNotes- und Datei-Upload stehen darunter und verdecken den Startbutton
  nicht mehr.
- Der Button wird aktiv, sobald Text im Editor vorhanden ist.
