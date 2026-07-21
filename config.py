from __future__ import annotations

import os

APP_NAME = "Sokrates 2.0"
APP_ICON = "🧭"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
MAX_OUTPUT_TOKENS = 650
MAX_FILE_SIZE_MB = 20
SUPPORTED_UPLOAD_TYPES = ["pdf", "png", "jpg", "jpeg", "webp", "txt", "docx"]
