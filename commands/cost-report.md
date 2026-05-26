---
name: cost-report
description: Reporte de tokens y costos estimados, parseando los transcripts del proyecto
---

Ejecutá `python .claude/hooks/cost_report.py` (sin argumentos para escanear
todas las sesiones del proyecto actual, o pasando la ruta de un transcript
específico).

El script emite JSON con totales, desglose por modelo, por agente y alertas
de dispatch. Tomá esa salida y presentála formateada al usuario. No hagas
los cálculos vos — usá los números que devuelve el script.

### Resumen general
Turnos registrados, tokens por categoría (input / output / cache-read /
cache-creation), costo total USD estimado.

### Por modelo
Tabla: Modelo | Turnos | Tokens totales | Costo USD | % del costo total.

### Por agente
Tabla: Agente (main / subagent) | Turnos | Tokens totales | Costo USD.

### Alertas de dispatch
Si `dispatch_alerts` trae registros, listalos (subagente que se esperaba en
haiku pero usó otro modelo). Si está vacío: "Sin alertas de dispatch."

### Modelos no reconocidos
Si `unknown_models` no está vacío, listalos y recordá que hay que agregar sus
precios en `.claude/hooks/model_info.py` para que el costo los incluya.

---

Si el script falla o no hay transcripts, informá el error tal cual.
No modifiques ningún archivo. El costo es una **estimación** basada en la
tabla de precios de `model_info.py` (ver su fecha de verificación).
