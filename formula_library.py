from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Formula:
    key: str
    title: str
    display: str
    explanation: str


FORMULAS = {
    "semicircle_area": Formula(
        "semicircle_area",
        "Halbkreis – Fläche",
        "A = ½ · π · r²",
        "Die Fläche eines Halbkreises ist die Hälfte der Kreisfläche.",
    ),
    "circle_area": Formula(
        "circle_area",
        "Kreis – Fläche",
        "A = π · r²",
        "Fläche eines ganzen Kreises.",
    ),
    "circle_circumference": Formula(
        "circle_circumference",
        "Kreis – Umfang",
        "U = 2 · π · r",
        "Umfang eines ganzen Kreises.",
    ),
    "sector_area": Formula(
        "sector_area",
        "Kreisausschnitt – Fläche",
        "Aₛ = α : 360° · π · r²",
        "Winkelanteil mal Kreisfläche.",
    ),
    "arc_length": Formula(
        "arc_length",
        "Kreisbogen – Länge",
        "b = α : 360° · 2 · π · r",
        "Winkelanteil mal Kreisumfang.",
    ),
    "pythagoras": Formula(
        "pythagoras",
        "Satz des Pythagoras",
        "a² + b² = c²",
        "c ist die Hypotenuse.",
    ),
    "percent_value": Formula(
        "percent_value",
        "Prozentwert",
        "W = G · p : 100",
        "Berechnet den Prozentwert.",
    ),
    "percentage": Formula(
        "percentage",
        "Prozentsatz",
        "p = W : G · 100",
        "Berechnet den Prozentsatz.",
    ),
    "base_value": Formula(
        "base_value",
        "Grundwert",
        "G = W · 100 : p",
        "Berechnet den Grundwert.",
    ),
    "linear_equation": Formula(
        "linear_equation",
        "Lineare Gleichung",
        "a · x + b = c",
        "Allgemeine Form einer linearen Gleichung.",
    ),
    "triangle_area": Formula(
        "triangle_area",
        "Dreieck – Fläche",
        "A = g · h : 2",
        "Grundseite mal Höhe, geteilt durch 2.",
    ),
}


def formulas_for(keys: tuple[str, ...]) -> tuple[Formula, ...]:
    return tuple(FORMULAS[key] for key in keys if key in FORMULAS)
