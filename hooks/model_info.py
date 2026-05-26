#!/usr/bin/env python3
"""
model_info.py — Tabla de modelos: ventana de contexto y precios.

NO es un hook. Es data compartida que importan context_guardian.py
(para la ventana de contexto) y cost_report.py (para precios).

⚠️  MANTENIMIENTO MANUAL. Precios y ventanas verificados al: 2026-05-26
Fuente: https://platform.claude.com/docs/en/about-claude/pricing
        https://claude.com/blog/1m-context-ga (ventana 1M GA para 4.6)
Revisar cada vez que Anthropic cambie precios o saque modelos nuevos.

Precios en USD por millón de tokens (MTok). Multiplicadores de caché
estándar de Anthropic: read = 0.1× input, write 5m = 1.25× input,
write 1h = 2× input.
"""

# Claves matcheadas por substring contra message.model del transcript.
# El orden importa: las más específicas primero (ver match_model).
MODEL_INFO = {
    "opus-4-7": {
        "context_window": 1_000_000,
        "price_input":       5.00,
        "price_output":     25.00,
        "price_cache_read":  0.50,
        "price_cache_write_5m": 6.25,
        "price_cache_write_1h": 10.00,
    },
    "opus-4-6": {
        "context_window": 1_000_000,
        "price_input":       5.00,
        "price_output":     25.00,
        "price_cache_read":  0.50,
        "price_cache_write_5m": 6.25,
        "price_cache_write_1h": 10.00,
    },
    "sonnet-4-6": {
        "context_window": 1_000_000,
        "price_input":       3.00,
        "price_output":     15.00,
        "price_cache_read":  0.30,
        "price_cache_write_5m": 3.75,
        "price_cache_write_1h": 6.00,
    },
    "haiku-4-5": {
        "context_window":  200_000,
        "price_input":       1.00,
        "price_output":      5.00,
        "price_cache_read":  0.10,
        "price_cache_write_5m": 1.25,
        "price_cache_write_1h": 2.00,
    },
}

# Fallback si el modelo no matchea ninguna entrada.
DEFAULT_CONTEXT_WINDOW = 200_000


def match_model(model_name: str):
    """Devuelve la entrada de MODEL_INFO cuyo key sea substring del modelo,
    o None si no hay match. Las claves más específicas (versionadas) se
    prueban primero por estar listadas antes en el dict."""
    if not model_name:
        return None
    for key, info in MODEL_INFO.items():
        if key in model_name:
            return info
    return None
