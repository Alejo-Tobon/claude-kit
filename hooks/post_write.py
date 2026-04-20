#!/usr/bin/env python3
"""
Hook: post_write.py
Evento: PostToolUse (Write, Edit)
Propósito: Ejecutar linter y formatter automáticamente
           después de que el agente escribe un archivo.
           Detecta el stack por extensión de archivo.
"""

import json
import os
import subprocess
import sys


# ─── Configuración por extensión ───────────────────────────────────────────

# Cada entrada: extensión → lista de comandos a ejecutar en orden
# Los comandos usan {file} como placeholder para el path del archivo

FORMATTERS = {
    ".ts":  ["npx prettier --write {file}", "npx eslint --fix {file}"],
    ".tsx": ["npx prettier --write {file}", "npx eslint --fix {file}"],
    ".js":  ["npx prettier --write {file}", "npx eslint --fix {file}"],
    ".jsx": ["npx prettier --write {file}", "npx eslint --fix {file}"],
    ".py":  ["ruff format {file}", "ruff check --fix {file}"],
    ".go":  ["gofmt -w {file}"],
    ".java":["google-java-format --replace {file}"],
}

# Extensiones que se skipean silenciosamente
SKIP_EXTENSIONS = {".md", ".json", ".yml", ".yaml", ".env", ".gitignore", ".txt"}


def run_command(cmd: str, filepath: str) -> tuple[int, str]:
    """Ejecuta un comando reemplazando {file} por el path real."""
    cmd_with_file = cmd.replace("{file}", filepath)
    try:
        result = subprocess.run(
            cmd_with_file,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        output = (result.stdout + result.stderr).strip()
        return result.returncode, output
    except subprocess.TimeoutExpired:
        return 1, "Timeout al ejecutar el comando"
    except Exception as e:
        return 1, str(e)


def main():
    data = json.loads(sys.stdin.read())

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    filepath = tool_input.get("file_path", tool_input.get("path", ""))
    if not filepath or not os.path.exists(filepath):
        sys.exit(0)

    _, ext = os.path.splitext(filepath)

    if ext in SKIP_EXTENSIONS:
        sys.exit(0)

    commands = FORMATTERS.get(ext)
    if not commands:
        sys.exit(0)

    # ── Ejecutar cada comando en orden ──────────────────────────────────────
    errors = []
    for cmd in commands:
        returncode, output = run_command(cmd, filepath)
        if returncode != 0 and output:
            errors.append(f"{cmd.split()[0]}: {output[:200]}")

    if errors:
        print(
            f"⚠️  Post-write issues en {filepath}:\n" +
            "\n".join(f"   {e}" for e in errors),
            file=sys.stderr
        )
    else:
        print(f"✅ {os.path.basename(filepath)} formateado correctamente")

    # No bloqueamos por errores de formato — son advertencias
    sys.exit(0)


if __name__ == "__main__":
    main()