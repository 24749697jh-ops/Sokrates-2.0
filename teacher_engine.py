from __future__ import annotations

from models import TaskAnalysis, TutorState


def first_question(analysis: TaskAnalysis) -> str:
    return analysis.opening_question


def next_phase(state: TutorState, student_text: str) -> str:
    text = student_text.lower()

    if state.phase == "VERSTEHEN":
        if any(word in text for word in ("formel", "zusammenhang", "halb", "ganz", "gegeben", "gesucht")):
            return "PLANEN"
        return "VERSTEHEN"

    if state.phase == "PLANEN":
        if any(symbol in student_text for symbol in ("=", "π", "²", "^")) or any(
            word in text for word in ("einsetzen", "umstellen", "multiplizieren", "teilen")
        ):
            return "RECHNEN"
        return "PLANEN"

    if state.phase == "RECHNEN":
        if any(word in text for word in ("probe", "prüfen", "einsetzen", "stimmt")):
            return "PRÜFEN"
        return "RECHNEN"

    return "PRÜFEN"


def phase_question(analysis: TaskAnalysis, phase: str) -> str:
    if phase == "VERSTEHEN":
        return analysis.opening_question
    if phase == "PLANEN":
        return analysis.planning_question
    if phase == "PRÜFEN":
        return analysis.checking_question
    return "Welchen einzelnen Rechenschritt kannst du jetzt sicher ausführen?"


def build_instructions(
    analysis: TaskAnalysis,
    state: TutorState,
    student_text: str,
) -> str:
    misconceptions = "\n".join(f"- {item}" for item in analysis.misconceptions)

    return f"""
Du bist Sokrates, ein erfahrener Mathematiklehrer.

Pädagogischer Ablauf:
1. VERSTEHEN
2. PLANEN
3. RECHNEN
4. PRÜFEN

Die Aufgabe wurde beim Start verbindlich analysiert. Ändere diese Analyse niemals.

Thema: {analysis.topic}
Aufgabentyp: {analysis.subtype}
Gesucht: {analysis.sought}
Gegeben: {", ".join(analysis.given)}
Begriffe: {", ".join(analysis.concepts)}
Aktuelle Phase: {state.phase}
Hilfestufe: {state.help_level}

Letzter Schülerbeitrag:
{student_text}

Typische Denkfehler:
{misconceptions}

Regeln:
- Beziehe dich ausschließlich auf diese konkrete Aufgabe.
- Stelle genau eine kurze, passende Frage.
- Gehe nur einen Denkschritt weiter.
- Liefere keine vollständige Lösung und kein Endergebnis.
- In VERSTEHEN keine Umformungs- oder Rechenfrage.
- In PLANEN zuerst Formel oder Zusammenhang klären.
- In RECHNEN genau einen Rechenschritt prüfen oder anfordern.
- In PRÜFEN eine Probe oder Plausibilitätsprüfung verlangen.
- Bei Unsicherheit einen kleinen Hinweis geben, nicht die Lösung.
- Nutze höchstens vier kurze Sätze.
- Mathematik steht in $...$ oder $$...$$.
""".strip()
