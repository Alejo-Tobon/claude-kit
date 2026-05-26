#!/usr/bin/env python3
"""
cost_report.py — Parsea transcripts de Claude Code y estima costo.

NO es un hook. Es un script invocado por el command /cost-report.

Uso:
  python hooks/cost_report.py [ruta-a-transcript.jsonl]

Sin argumento: escanea todos los transcripts bajo
~/.claude/projects/*/*.jsonl y se queda con los registros cuyo campo
`cwd` coincida con el directorio de trabajo actual (os.getcwd()).
NO reconstruye el nombre codificado del proyecto (en Windows la letra
de unidad se pasa a minúscula y la regla naive falla).

Salida: JSON a stdout. No escribe ni modifica archivos.

El costo se estima con la tabla de precios de model_info.py. Las 4
categorías de tokens se cobran a precios distintos; cache_creation se
desglosa en 5m/1h cuando el transcript lo informa.
"""

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model_info import match_model

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def transcript_files(arg_path):
    """Lista de archivos a procesar. Si se pasó un path, ese; si no,
    todos los transcripts del usuario (luego se filtran por cwd)."""
    if arg_path:
        return [arg_path]
    home = os.path.expanduser("~")
    pattern = os.path.join(home, ".claude", "projects", "*", "*.jsonl")
    return glob.glob(pattern)


def turn_cost(usage, info):
    """Costo USD de un turno dado su usage y la entrada de precios.
    Devuelve None si no hay precios (modelo no reconocido)."""
    if not info:
        return None
    inp   = usage.get("input_tokens", 0)
    out   = usage.get("output_tokens", 0)
    read  = usage.get("cache_read_input_tokens", 0)
    # Desglose de cache_creation en 5m / 1h si está disponible.
    cc = usage.get("cache_creation") or {}
    w5m = cc.get("ephemeral_5m_input_tokens")
    w1h = cc.get("ephemeral_1h_input_tokens")
    if w5m is None and w1h is None:
        # Sin desglose: tratar todo cache_creation como 5m (conservador).
        w5m = usage.get("cache_creation_input_tokens", 0)
        w1h = 0
    cost = (
        inp  * info["price_input"]
        + out  * info["price_output"]
        + read * info["price_cache_read"]
        + (w5m or 0) * info["price_cache_write_5m"]
        + (w1h or 0) * info["price_cache_write_1h"]
    ) / 1_000_000
    return cost


def main():
    arg_path = sys.argv[1] if len(sys.argv) > 1 else None
    scan_all = arg_path is None
    # Normalizar para comparar cwd: en Windows la letra de unidad aparece
    # con mayúscula y minúscula de forma inconsistente entre registros
    # (C:\ vs c:\). normcase lo unifica; en POSIX es no-op (case-sensitive).
    target_cwd = os.path.normcase(os.path.normpath(os.getcwd()))

    totals = {
        "turns": 0,
        "input_tokens": 0, "output_tokens": 0,
        "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0,
        "cost_usd": 0.0,
    }
    by_model = {}     # model -> {turns, total_tokens, cost_usd}
    by_agent = {}     # "main"/"subagent" -> {turns, total_tokens, cost_usd}
    unknown_models = set()
    dispatch_alerts = []   # subagentes con modelo inesperado (no-haiku)

    for path in transcript_files(arg_path):
        try:
            f = open(path, encoding="utf-8")
        except OSError:
            continue
        with f:
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
                # Filtro por proyecto cuando se escanea todo (cwd normalizado).
                if scan_all:
                    rec_cwd = rec.get("cwd")
                    if not rec_cwd or os.path.normcase(os.path.normpath(rec_cwd)) != target_cwd:
                        continue
                msg = rec.get("message", {})
                usage = msg.get("usage")
                if not usage:
                    continue
                model = msg.get("model", "unknown")
                info = match_model(model)

                inp  = usage.get("input_tokens", 0)
                out  = usage.get("output_tokens", 0)
                read = usage.get("cache_read_input_tokens", 0)
                cwr  = usage.get("cache_creation_input_tokens", 0)
                tot_tokens = inp + out + read + cwr

                cost = turn_cost(usage, info)
                if cost is None:
                    unknown_models.add(model)
                    cost_val = 0.0
                else:
                    cost_val = cost

                totals["turns"] += 1
                totals["input_tokens"] += inp
                totals["output_tokens"] += out
                totals["cache_read_input_tokens"] += read
                totals["cache_creation_input_tokens"] += cwr
                totals["cost_usd"] += cost_val

                m = by_model.setdefault(model, {"turns": 0, "total_tokens": 0, "cost_usd": 0.0})
                m["turns"] += 1
                m["total_tokens"] += tot_tokens
                m["cost_usd"] += cost_val

                is_sidechain = bool(rec.get("isSidechain"))
                akey = "subagent" if is_sidechain else "main"
                a = by_agent.setdefault(akey, {"turns": 0, "total_tokens": 0, "cost_usd": 0.0})
                a["turns"] += 1
                a["total_tokens"] += tot_tokens
                a["cost_usd"] += cost_val

                # Alerta de dispatch (best-effort): subagente cuyo slug/
                # atribución sugiere api-explorer pero el modelo no es haiku.
                slug = (rec.get("slug") or "") + " " + (rec.get("attributionSkill") or "")
                if is_sidechain and "api-explorer" in slug.lower() and "haiku" not in model.lower():
                    dispatch_alerts.append({"model": model, "slug": rec.get("slug")})

    totals["cost_usd"] = round(totals["cost_usd"], 6)
    for d in (by_model, by_agent):
        for v in d.values():
            v["cost_usd"] = round(v["cost_usd"], 6)

    report = {
        "scope": "transcript único" if arg_path else f"proyecto cwd={target_cwd}",
        "totals": totals,
        "by_model": by_model,
        "by_agent": by_agent,
        "dispatch_alerts": dispatch_alerts,
        "unknown_models": sorted(unknown_models),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
