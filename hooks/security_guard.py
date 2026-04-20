#!/usr/bin/env python3
"""
Hook: security_guard.py
Evento: PreToolUse (Write, Edit)
Propósito: Detectar patrones peligrosos en el contenido
           que el agente intenta escribir, antes de que
           el archivo llegue al disco.
"""

import json
import re
import sys


# ─── Patrones que bloquean el write (exit 2) ───────────────────────────────

BLOCKED_PATTERNS = [
    # JWT / tokens como parámetros de función
    (
        r"def\s+\w+\s*\(.*\btoken\b.*\)",
        "JWT/token como parámetro de función — usar token_store"
    ),
    (
        r"function\s+\w+\s*\(.*\btoken\b.*\)",
        "JWT/token como parámetro de función — usar token_store"
    ),
    # Secrets hardcodeados
    (
        r"(password|secret|api_key|apikey)\s*=\s*['\"][^'\"]{6,}['\"]",
        "Posible secret hardcodeado detectado"
    ),
    # rm -rf peligroso
    (
        r"rm\s+-rf\s+/(?!tmp|var/tmp)",
        "rm -rf en ruta del sistema — operación bloqueada"
    ),
    # Curl piped a bash
    (
        r"curl\s+.*\|\s*(ba)?sh",
        "curl piped a shell — patrón inseguro"
    ),
    # DROP DATABASE / DROP TABLE
    (
        r"DROP\s+(DATABASE|TABLE)\s+\w+",
        "Operación DDL destructiva sin confirmed=True"
    ),
]

# ─── Patrones que emiten advertencia (no bloquean) ─────────────────────────

WARNING_PATTERNS = [
    (
        r"console\.log\(",
        "console.log detectado — usar el logger del proyecto"
    ),
    (
        r"TODO|FIXME|HACK",
        "Marcador de deuda técnica en el código"
    ),
    (
        r"\.env\b",
        "Referencia a .env — verificar que no se hardcodeen valores"
    ),
]


def main():
    data = json.loads(sys.stdin.read())

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Solo actuar en Write y Edit
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    # Obtener el contenido según la tool
    if tool_name == "Write":
        content = tool_input.get("content", "")
        filepath = tool_input.get("file_path", "")
    else:  # Edit
        content = tool_input.get("new_content", "") or tool_input.get("new_string", "")
        filepath = tool_input.get("file_path", tool_input.get("path", ""))

    if not content:
        sys.exit(0)

    # ── Verificar patrones bloqueantes ──────────────────────────────────────
    for pattern, message in BLOCKED_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            print(
                f"🚫 BLOQUEADO — {message}\n"
                f"   Archivo: {filepath}\n"
                f"   Patrón: {pattern}\n"
                f"   Corregí el código antes de continuar.",
                file=sys.stderr
            )
            sys.exit(2)

    # ── Verificar patrones de advertencia ───────────────────────────────────
    warnings = []
    for pattern, message in WARNING_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            warnings.append(message)

    if warnings:
        for w in warnings:
            print(f"⚠️  {w} — {filepath}")

    sys.exit(0)


if __name__ == "__main__":
    main()