from __future__ import annotations

import base64
import io
import mimetypes
import os
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from sokrates_math_editor import math_editor
from streamlit_paste_button import paste_image_button

from config import (
    APP_ICON,
    APP_NAME,
    MAX_FILE_SIZE_MB,
    MAX_OUTPUT_TOKENS,
    MODEL,
    SUPPORTED_UPLOAD_TYPES,
)
from models import TaskAnalysis, TutorState
from task_analysis import analyze_task
from teacher_engine import (
    build_instructions,
    first_question,
    next_phase,
    phase_question,
)
from ui import inject_theme, render_chat, render_formulas, render_task_card

load_dotenv()

st.set_page_config(
    page_title=f"{APP_NAME} – Mathe-Lerncoach",
    page_icon=APP_ICON,
    layout="wide",
)
inject_theme()


def ensure_state() -> None:
    defaults = {
        "started_v21": False,
        "task_text_v21": "",
        "task_draft_v21": "",
        "task_reset_v21": 0,
        "reply_draft_v21": "",
        "reply_reset_v21": 0,
        "analysis_v21": None,
        "tutor_state_v21": TutorState(),
        "messages_v21": [],
        "uploaded_name_v21": None,
        "uploaded_bytes_v21": None,
        "uploaded_mime_v21": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_all() -> None:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    ensure_state()


def as_data_url(data: bytes, mime: str) -> str:
    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def store_pasted_image(image: Any) -> None:
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="PNG")
    st.session_state.uploaded_name_v21 = "goodnotes.png"
    st.session_state.uploaded_bytes_v21 = buffer.getvalue()
    st.session_state.uploaded_mime_v21 = "image/png"


def api_input(student_text: str) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = [{
        "type": "input_text",
        "text": (
            f"Ursprüngliche Aufgabe:\n{st.session_state.task_text_v21}\n\n"
            f"Letzter Schülerbeitrag:\n{student_text}"
        ),
    }]

    data = st.session_state.uploaded_bytes_v21
    mime = st.session_state.uploaded_mime_v21
    if data and mime:
        encoded = as_data_url(data, mime)
        if mime.startswith("image/"):
            content.append({"type": "input_image", "image_url": encoded, "detail": "high"})
        else:
            content.append({
                "type": "input_file",
                "filename": st.session_state.uploaded_name_v21,
                "file_data": encoded,
            })

    return [{"role": "user", "content": content}]


def ask_sokrates(student_text: str) -> str:
    analysis: TaskAnalysis = st.session_state.analysis_v21
    state: TutorState = st.session_state.tutor_state_v21
    state.phase = next_phase(state, student_text)
    state.turns += 1

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=MODEL,
        instructions=build_instructions(analysis, state, student_text),
        input=api_input(student_text),
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )
    answer = response.output_text.strip()
    return answer or phase_question(analysis, state.phase)


ensure_state()

st.title("🧭 Sokrates 2.1.1")
st.caption("Ich begleite dich – denken musst du selbst.")
st.caption("Verstehen → Planen → Rechnen → Prüfen")
st.caption("Installierte Version: 2.1.1")

api_key = os.getenv("OPENAI_API_KEY")

with st.sidebar:
    st.header("Sokrates")
    if api_key:
        st.success("✅ Sokrates ist bereit")
    else:
        st.error("OpenAI-Schlüssel fehlt.")

    if st.button("Neue Aufgabe", use_container_width=True):
        reset_all()
        st.rerun()

    if st.session_state.started_v21 and st.session_state.analysis_v21:
        st.divider()
        render_formulas(
            st.session_state.analysis_v21,
            "reply_editor_value_v21",
        )


if not st.session_state.started_v21:
    st.markdown("### Aufgabe eingeben")
    task_result = math_editor(
        value=st.session_state.task_draft_v21,
        placeholder="Schreibe die Aufgabe hier hinein. Die Mathe-Tasten schreiben direkt an der Cursorposition.",
        reset_token=st.session_state.task_reset_v21,
        key="task_editor_v21",
    )
    st.session_state.task_draft_v21 = task_result.get("value", "")

    st.markdown("### Aus GoodNotes einfügen")
    paste_result = paste_image_button(
        label="📋 Aus Zwischenablage einfügen",
        key="goodnotes_v21",
        errors="raise",
    )
    if paste_result.image_data is not None:
        store_pasted_image(paste_result.image_data)
        st.success("GoodNotes-Aufgabe eingefügt.")

    upload = st.file_uploader(
        "Oder Datei hochladen",
        type=SUPPORTED_UPLOAD_TYPES,
    )
    if upload is not None:
        size_mb = len(upload.getvalue()) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            st.error(f"Die Datei ist größer als {MAX_FILE_SIZE_MB} MB.")
        else:
            st.session_state.uploaded_name_v21 = upload.name
            st.session_state.uploaded_bytes_v21 = upload.getvalue()
            st.session_state.uploaded_mime_v21 = (
                upload.type
                or mimetypes.guess_type(upload.name)[0]
                or "application/octet-stream"
            )
            st.success(f"Datei bereit: {upload.name}")

    if st.button("Mit Sokrates beginnen", type="primary", use_container_width=True):
        task = st.session_state.task_draft_v21.strip()
        if not api_key:
            st.error("Der OpenAI-Schlüssel fehlt.")
        elif not task and not st.session_state.uploaded_bytes_v21:
            st.error("Bitte gib eine Aufgabe ein oder lade eine Datei hoch.")
        else:
            st.session_state.task_text_v21 = task or "Aufgabe aus hochgeladener Datei"
            st.session_state.analysis_v21 = analyze_task(st.session_state.task_text_v21)
            st.session_state.tutor_state_v21 = TutorState()
            st.session_state.messages_v21 = [{
                "role": "assistant",
                "content": first_question(st.session_state.analysis_v21),
            }]
            st.session_state.started_v21 = True
            st.rerun()

else:
    analysis: TaskAnalysis = st.session_state.analysis_v21
    state: TutorState = st.session_state.tutor_state_v21

    render_task_card(st.session_state.task_text_v21, analysis, state.phase)
    render_chat(st.session_state.messages_v21)

    st.caption(f"Hilfestufe {state.help_level} von 4")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💡 Kleiner Hinweis", use_container_width=True):
            state.help_level = min(4, state.help_level + 1)
            hint_text = "Ich bin unsicher. Gib mir einen kleinen Hinweis, aber noch keine vollständige Lösung."
            st.session_state.messages_v21.append({"role": "user", "content": hint_text})
            try:
                st.session_state.messages_v21.append({
                    "role": "assistant",
                    "content": ask_sokrates(hint_text),
                })
                st.rerun()
            except Exception as exc:
                st.error(f"Fehler: {exc}")

    with c2:
        if st.button("↩️ Hilfestufe zurücksetzen", use_container_width=True):
            state.help_level = 1
            st.rerun()

    st.divider()
    st.markdown("### Dein nächster Schritt")
    reply_result = math_editor(
        value=st.session_state.reply_draft_v21,
        placeholder="Erkläre deinen Gedanken oder schreibe einen Rechenschritt.",
        reset_token=st.session_state.reply_reset_v21,
        key="reply_editor_v21",
    )
    st.session_state.reply_draft_v21 = reply_result.get("value", "")

    if st.button(
        "An Sokrates senden",
        type="primary",
        use_container_width=True,
        disabled=not st.session_state.reply_draft_v21.strip(),
    ):
        reply = st.session_state.reply_draft_v21.strip()
        st.session_state.messages_v21.append({"role": "user", "content": reply})
        try:
            answer = ask_sokrates(reply)
            st.session_state.messages_v21.append({"role": "assistant", "content": answer})
            st.session_state.reply_draft_v21 = ""
            st.session_state.reply_reset_v21 += 1
            st.rerun()
        except Exception as exc:
            st.error(f"Die Anfrage konnte nicht verarbeitet werden: {exc}")
