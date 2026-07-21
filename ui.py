from __future__ import annotations

import streamlit as st

from formula_library import formulas_for
from models import TaskAnalysis


def inject_theme() -> None:
    st.markdown(
        """
        <style>
        .block-container {max-width: 980px; padding-top: 1rem;}
        .task-card {
            border: 1px solid rgba(128,128,128,.25);
            border-radius: 18px;
            padding: 1rem 1.2rem;
            margin: .5rem 0 1rem 0;
        }
        .phase {
            display: inline-block;
            padding: .25rem .7rem;
            border-radius: 999px;
            border: 1px solid rgba(128,128,128,.3);
            margin-right: .3rem;
            font-size: .85rem;
        }
        div[data-testid="stButton"] button {min-height: 2.65rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_task_card(task_text: str, analysis: TaskAnalysis, phase: str) -> None:
    st.markdown(
        f"""
        <div class="task-card">
          <h3>📌 Deine Aufgabe</h3>
          <p>{task_text}</p>
          <hr>
          <p><strong>Erkannt:</strong> {analysis.subtype}</p>
          <p><strong>Gesucht:</strong> {analysis.sought}</p>
          <span class="phase">Aktuelle Phase: {phase}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_formulas(analysis: TaskAnalysis, target_math_key: str) -> None:
    st.subheader("📚 Passende Formeln")
    formulas = formulas_for(analysis.formula_keys)
    if not formulas:
        st.caption("Für diese Aufgabe ist noch keine feste Formel hinterlegt.")
        return

    for formula in formulas:
        with st.container(border=True):
            st.markdown(f"**{formula.title}**")
            st.markdown(f"### {formula.display}")
            st.caption(formula.explanation)
            if st.button(
                "In Mathefeld übernehmen",
                key=f"formula_{formula.key}",
                use_container_width=True,
            ):
                st.session_state[target_math_key] = formula.display
                st.rerun()


def render_chat(messages: list[dict]) -> None:
    for message in messages:
        avatar = "🧭" if message["role"] == "assistant" else "🧑‍🎓"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
