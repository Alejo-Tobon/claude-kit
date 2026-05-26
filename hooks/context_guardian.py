#!/usr/bin/env python3
"""
Hook: context_guardian.py
Evento: Stop
Propósito: Advertir sobre uso de contexto leyendo el último mensaje
           del transcript. Solo informa — la compactación automática
           (CLAUDE_AUTOCOMPACT_PCT_OVERRIDE) es el control efectivo.

El payload del evento Stop NO trae uso de tokens; solo trae
transcript_path. Por eso el uso de contexto se lee del transcript.

Umbrales (sobre la ventana del modelo):
  55% → aviso temprano
  65% → aviso urgente
"""

import json
import os
import sys

# Salida UTF-8 defensiva: en Windows el stdout puede ser cp1252 y los
# emoji crashearían el hook con UnicodeEncodeError.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model_info import match_model, DEFAULT_CONTEXT_WINDOW

WARN_THRESHOLD   = 0.55
URGENT_THRESHOLD = 0.65


def last_assistant_usage(transcript_path):
    """Devuelve (model, context_tokens) del último mensaje assistant
    con usage, o (None, 0) si no se puede determinar."""
    if not transcript_path or not os.path.exists(transcript_path):
        return None, 0
    model, ctx = None, 0
    with open(transcript_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("type") != "assistant":
                continue
            msg = rec.get("message", {})
            u = msg.get("usage")
            if not u:
                continue
            # Contexto ocupado por el INPUT de este turno. Las tres
            # categorías son particiones disjuntas del input procesado:
            #   input_tokens                = input fresco, no cacheado
            #   cache_read_input_tokens     = leído de caché (historia previa)
            #   cache_creation_input_tokens = escrito a caché este turno (nuevo)
            # Su suma = total de tokens de input en ventana en ese momento.
            # No es una aproximación: es la medida completa de ocupación de
            # input. Se EXCLUYE output_tokens a propósito — no ocupa ventana
            # de input en este turno (pasa a la historia recién el turno
            # siguiente, donde ya queda contado vía caché/input).
            ctx = (u.get("input_tokens", 0)
                   + u.get("cache_read_input_tokens", 0)
                   + u.get("cache_creation_input_tokens", 0))
            model = msg.get("model")
    return model, ctx


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    model, ctx = last_assistant_usage(data.get("transcript_path", ""))
    if ctx == 0:
        sys.exit(0)

    info = match_model(model)
    window = info["context_window"] if info else DEFAULT_CONTEXT_WINDOW
    usage = ctx / window

    if usage >= URGENT_THRESHOLD:
        print(f"⚠️  Contexto ~{usage*100:.0f}% ({ctx:,}/{window:,} tok). "
              "Compactación próxima. Si hay estado crítico, guardalo en "
              "`.claude/session-state.md`.")
    elif usage >= WARN_THRESHOLD:
        print(f"ℹ️  Contexto ~{usage*100:.0f}% ({ctx:,}/{window:,} tok). "
              "Considerá cerrar la tarea actual antes de iniciar otra.")

    sys.exit(0)


if __name__ == "__main__":
    main()
