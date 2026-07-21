from __future__ import annotations

import re

from models import TaskAnalysis


def _contains(text: str, *words: str) -> bool:
    return any(word in text for word in words)


def analyze_task(task_text: str) -> TaskAnalysis:
    """
    Analyse exactly once when a task starts.
    Later student messages never change the mathematical topic.
    """
    text = " ".join(task_text.lower().split())

    # Specific rules always come before general rules.
    if "halbkreis" in text:
        given = []
        if match := re.search(r"a\s*=\s*([0-9]+(?:[.,][0-9]+)?)\s*cm\s*[²2]?", text):
            given.append(f"Fläche A = {match.group(1)} cm²")
        if not given:
            given.append("Fläche eines Halbkreises")

        return TaskAnalysis(
            topic="Geometrie",
            subtype="Halbkreis – Radius aus der Fläche",
            sought="Radius r",
            given=tuple(given),
            concepts=("Halbkreis", "Kreisfläche", "Radius", "Umstellen"),
            formula_keys=("semicircle_area", "circle_area"),
            opening_question=(
                "Gesucht ist der Radius eines Halbkreises. "
                "Was bedeutet „Halbkreis“ für die Fläche im Vergleich zu einem ganzen Kreis?"
            ),
            planning_question=(
                "Welche Flächenformel beschreibt deshalb den Halbkreis, bevor du nach dem Radius umstellst?"
            ),
            checking_question=(
                "Wie kannst du mit deinem Radius prüfen, ob wieder die vorgegebene Halbkreisfläche entsteht?"
            ),
            misconceptions=(
                "Formel des ganzen Kreises ohne Halbierung verwendet",
                "Radius und Durchmesser verwechselt",
                "cm² als Einheit des Radius übernommen",
            ),
        )

    if "kreisausschnitt" in text or "sektor" in text:
        return TaskAnalysis(
            topic="Geometrie",
            subtype="Kreisausschnitt",
            sought="Fläche oder Bogenlänge",
            given=("Mittelpunktswinkel und Kreisgröße",),
            concepts=("Winkelanteil", "Kreisfläche", "Kreisumfang"),
            formula_keys=("sector_area", "arc_length"),
            opening_question="Welche Größe ist gesucht: die Fläche des Kreisausschnitts oder die Länge des Kreisbogens?",
            planning_question="Welchen Anteil eines ganzen Kreises beschreibt der gegebene Mittelpunktswinkel?",
            checking_question="Ist dein Ergebnis kleiner als die entsprechende Größe des ganzen Kreises?",
            misconceptions=("Fläche und Bogenlänge verwechselt", "Winkelanteil vergessen"),
        )

    if "kreis" in text and _contains(text, "fläche", "umfang", "radius", "durchmesser"):
        return TaskAnalysis(
            topic="Geometrie",
            subtype="Kreis",
            sought="Kreisgröße",
            given=("Radius, Durchmesser, Fläche oder Umfang",),
            concepts=("Radius", "Durchmesser", "Kreisfläche", "Kreisumfang"),
            formula_keys=("circle_area", "circle_circumference"),
            opening_question="Welche Kreisgröße ist gegeben und welche Kreisgröße soll bestimmt werden?",
            planning_question="Welche Formel verbindet genau diese beiden Größen?",
            checking_question="Passt die Einheit zu einer Länge oder zu einer Fläche?",
            misconceptions=("Radius und Durchmesser verwechselt", "Fläche und Umfang verwechselt"),
        )

    if "pythagoras" in text or "hypotenuse" in text or "rechtwinklig" in text:
        return TaskAnalysis(
            topic="Geometrie",
            subtype="Satz des Pythagoras",
            sought="fehlende Seitenlänge",
            given=("rechtwinkliges Dreieck",),
            concepts=("Katheten", "Hypotenuse", "Quadrate"),
            formula_keys=("pythagoras",),
            opening_question="Wo liegt der rechte Winkel und welche Seite ist deshalb die Hypotenuse?",
            planning_question="Welche Seiten setzt du in a² + b² = c² ein?",
            checking_question="Ist die Hypotenuse länger als jede einzelne Kathete?",
            misconceptions=("falsche Seite als Hypotenuse", "Wurzel vergessen"),
        )

    if "prozent" in text or "%" in text or "rabatt" in text:
        return TaskAnalysis(
            topic="Prozentrechnung",
            subtype="Prozentrechnung",
            sought="Grundwert, Prozentwert oder Prozentsatz",
            given=("zwei der Größen G, W und p",),
            concepts=("Grundwert", "Prozentwert", "Prozentsatz"),
            formula_keys=("percent_value", "percentage", "base_value"),
            opening_question="Welche Zahl ist der Grundwert, welche der Prozentwert und welche Größe ist gesucht?",
            planning_question="Welche der drei Prozentformeln passt zu den gegebenen und gesuchten Größen?",
            checking_question="Ist das Ergebnis im Verhältnis zum Grundwert plausibel?",
            misconceptions=("Grundwert und Prozentwert vertauscht", "Prozentsatz nicht durch 100 geteilt"),
        )

    if re.search(r"\bx\b", text) and "=" in text:
        return TaskAnalysis(
            topic="Algebra",
            subtype="Lineare Gleichung",
            sought="Variable x",
            given=("eine Gleichung",),
            concepts=("Gegenoperation", "Äquivalenzumformung", "Probe"),
            formula_keys=("linear_equation",),
            opening_question="Welcher Term verhindert noch, dass x allein steht?",
            planning_question="Welche Gegenoperation musst du auf beiden Seiten zuerst ausführen?",
            checking_question="Ergibt das Einsetzen deines Wertes auf beiden Seiten dasselbe?",
            misconceptions=("Operation nur auf einer Seite", "Vorzeichenfehler"),
        )

    if "dreieck" in text and _contains(text, "fläche", "flächeninhalt"):
        return TaskAnalysis(
            topic="Geometrie",
            subtype="Dreiecksfläche",
            sought="Flächeninhalt A",
            given=("Grundseite und zugehörige Höhe",),
            concepts=("Grundseite", "senkrechte Höhe", "Flächeneinheit"),
            formula_keys=("triangle_area",),
            opening_question="Welche Grundseite und welche dazu senkrechte Höhe gehören zusammen?",
            planning_question="Wie lautet die Flächenformel für dieses Dreieck?",
            checking_question="Hast du durch 2 geteilt und eine quadratische Einheit verwendet?",
            misconceptions=("falsche Höhe gewählt", "Division durch 2 vergessen"),
        )

    return TaskAnalysis(
        topic="Mathematik",
        subtype="Allgemeine Aufgabe",
        sought="gesuchte Größe",
        given=("Angaben aus der Aufgabe",),
        concepts=("Gegebenes", "Gesuchtes", "Zusammenhang"),
        formula_keys=(),
        opening_question="Welche Größe soll am Ende bestimmt werden, und welche Angaben sind dafür unmittelbar wichtig?",
        planning_question="Welchen mathematischen Zusammenhang kannst du zuerst in Worten beschreiben?",
        checking_question="Wie kannst du das Ergebnis unabhängig prüfen?",
        misconceptions=("zu früh gerechnet", "Einheit vergessen"),
    )
