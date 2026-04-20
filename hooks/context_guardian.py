#!/usr/bin/env python3
"""
Hook: context_guardian.py
Evento: Stop (al final de cada turno del agente)
Propósito: Monitorear el uso del contexto y disparar
           el protocolo Document & Clear antes de que
           el agente empiece a degradarse.

Umbrales:
  55% → advertencia — el agente ve el aviso en el próximo turno
  70% → bloqueo — fuerza Document & Clear antes de continuar
"""

import json
import sys


WARN_THRESHOLD  = 0.55  # aviso, no bloqueante
BLOCK_THRESHOLD = 0.70  # bloquea hasta que el usuario haga /clear


def main():
    data = json.loads(sys.stdin.read())

    context = data.get("context_window", {})
    tokens_used = context.get("input_tokens", 0)
    tokens_max  = context.get("context_window_size", 0)

    if tokens_max == 0:
        sys.exit(0)

    usage = tokens_used / tokens_max

    # ── Zona de bloqueo ─────────────────────────────────────────────────────
    if usage >= BLOCK_THRESHOLD:
        print(
            f"🚨 CONTEXTO AL {usage*100:.0f}% — LÍMITE ALCANZADO\n\n"
            "No continúes con la siguiente tarea. Ejecutá el protocolo "
            "Document & Clear ahora:\n\n"
            "1. Escribí `.claude/session-state.md` con:\n"
            "   - Fase actual y estado\n"
            "   - Archivos creados/modificados\n"
            "   - Decisiones tomadas y sus razones\n"
            "   - Próximos pasos en orden\n"
            "   - Contexto de dominio descubierto\n\n"
            "2. Avisá al usuario:\n"
            "   'Estado guardado en session-state.md. "
            "Corré /clear y luego escribí continúa.'\n\n"
            "3. Esperá — no ejecutes más herramientas.",
            file=sys.stderr
        )
        sys.exit(2)

    # ── Zona de advertencia ─────────────────────────────────────────────────
    if usage >= WARN_THRESHOLD:
        print(
            f"⚠️  Contexto al {usage*100:.0f}%.\n"
            "Antes de iniciar la siguiente tarea pesada, "
            "considerá ejecutar Document & Clear: guardá el estado "
            "en `.claude/session-state.md` y avisá al usuario para "
            "correr /clear."
        )
        # stdout va al contexto del agente — lo verá en el próximo turno
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()