from __future__ import annotations

import streamlit as st


SYMBOL_ROWS = (
    (("²", "²"), ("³", "³"), ("√", "√("), ("π", "π"),
     ("α", "α"), ("β", "β"), ("γ", "γ"), ("Δ", "Δ")),
    (("+", " + "), ("−", " − "), ("×", " · "), ("÷", " : "),
     ("=", " = "), ("≠", " ≠ "), ("≤", " ≤ "), ("≥", " ≥ ")),
)


def _append(key: str, value: str) -> None:
    st.session_state[key] = st.session_state.get(key, "") + value


def _delete(key: str) -> None:
    st.session_state[key] = st.session_state.get(key, "")[:-1]


def _clear(key: str) -> None:
    st.session_state[key] = ""


def render_input(
    prefix: str,
    title: str,
    text_placeholder: str,
    submit_label: str,
) -> str | None:
    """
    Prose and mathematical symbols use separate state keys.
    Keypad buttons never modify the prose widget.
    """
    prose_key = f"{prefix}_prose_v2"
    math_key = f"{prefix}_math_v2"
    st.session_state.setdefault(math_key, "")

    st.markdown(f"### {title}")
    prose = st.text_area(
        "Text",
        key=prose_key,
        placeholder=text_placeholder,
        height=110,
        label_visibility="collapsed",
    )

    st.caption("Mathematische Ergänzung")
    math = st.text_input(
        "Mathematik",
        key=math_key,
        placeholder="Zum Beispiel: A = 30 cm²",
        label_visibility="collapsed",
    )

    for row_index, row in enumerate(SYMBOL_ROWS):
        columns = st.columns(8)
        for index, (label, value) in enumerate(row):
            with columns[index]:
                st.button(
                    label,
                    key=f"{prefix}_symbol_{row_index}_{index}",
                    use_container_width=True,
                    on_click=_append,
                    args=(math_key, value),
                )

    combined = " ".join(part for part in (prose.strip(), math.strip()) if part).strip()

    if combined:
        st.markdown("**Vorschau**")
        st.markdown(combined)

    c1, c2, c3 = st.columns(3)
    with c1:
        submitted = st.button(
            submit_label,
            type="primary",
            use_container_width=True,
            disabled=not combined,
            key=f"{prefix}_submit_v2",
        )
    with c2:
        st.button(
            "⌫ Mathe",
            use_container_width=True,
            disabled=not math,
            key=f"{prefix}_delete_v2",
            on_click=_delete,
            args=(math_key,),
        )
    with c3:
        st.button(
            "Mathe löschen",
            use_container_width=True,
            disabled=not math,
            key=f"{prefix}_clear_v2",
            on_click=_clear,
            args=(math_key,),
        )

    return combined if submitted else None
