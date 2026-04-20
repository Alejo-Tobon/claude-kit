---
name: project-setup
description: |
  Estándar del kit para estructurar un proyecto nuevo.
  Define qué secciones debe tener el CLAUDE.md, qué
  agentes crear según el tipo de proyecto, y cómo
  verificar que el entorno quedó bien configurado.
triggers:
  - "setup-project"
  - "setup proyecto"
  - "inicializar proyecto"
  - "estructurar CLAUDE.md"
  - "nuevo proyecto"
  - "configurar entorno"
---

## Cuándo aplicar esta skill

Al ejecutar `/setup-project` en un proyecto nuevo
o al reestructurar el CLAUDE.md generado por `/init`
al estándar del equipo.

---

## Paso 1 — Preguntar el tipo de proyecto

Antes de crear cualquier archivo, hacer esta pregunta:

> "¿Qué tipo de proyecto es?
> 1. Backend API (Node/Express, Python/FastAPI, etc.)
> 2. Frontend (React, Vue, etc.)
> 3. Fullstack
> 4. MCP Server
> 5. Otro — describilo brevemente"

Esperar respuesta antes de continuar.

---

## Paso 2 — Reestructurar el CLAUDE.md

Si ya existe un CLAUDE.md (generado por `/init` u otro
medio), reestructurarlo. Si no existe, crearlo.

### Secciones obligatorias en orden:

```markdown
# CLAUDE.md — [nombre del proyecto]

## Qué es este proyecto
[2-3 líneas: propósito, dominio, qué problema resuelve]

## Stack
[Lenguajes, frameworks, versiones, herramientas principales]

## Comandos esenciales
- Dev:   [comando para levantar el proyecto]
- Test:  [comando para correr tests]
- Lint:  [comando para correr el linter]
- Build: [comando para compilar/build]

## Convenciones del equipo
[Naming, estructura de archivos, patrones obligatorios]
[Anti-patrones prohibidos]

## Agentes disponibles
| Tarea | Agente | Herramientas |
|-------|--------|--------------|
[completar según los agentes creados en Paso 3]

## Skills de referencia
| Tarea | Skill |
|-------|-------|
[completar según las skills disponibles en .claude/skills/]

## Reglas de dispatch
### Paralelo — solo si TODAS se cumplen:
- Las tareas son de dominios completamente separados
- No hay archivos compartidos que se modifiquen
- Cada tarea tiene scope claro

### Secuencial — si CUALQUIERA aplica:
- La tarea B depende del resultado de la tarea A
- Hay archivos compartidos que se modificarán

### Retorno de subagentes
Todo subagente devuelve máximo 200 tokens al
orquestador. Nunca devolver contenido completo
de archivos.

## Gestión del contexto
Al superar el 55% de uso del contexto:
1. Escribir .claude/session-state.md con:
   - Fase actual y estado
   - Archivos creados/modificados
   - Decisiones tomadas y sus razones
   - Próximos pasos pendientes
2. Avisar: "Estado guardado. Corré /clear y luego
   escribí 'continúa'."
3. Esperar confirmación antes de seguir.

Al iniciar sesión: si existe session-state.md,
leerlo ANTES de cualquier otra acción.

## Estado de fases
- [ ] Fase 1: [descripción]
[agregar fases según el proyecto]

## Registro de decisiones
| Fecha | Decisión | Razón |
|-------|----------|-------|

## Mantenimiento (obligatorio)
Ante cualquier cambio significativo, actualizar
este archivo ANTES de marcar la tarea como terminada.

Cuenta como cambio significativo:
- Agregar, renombrar o eliminar un módulo o endpoint
- Cambiar la estructura de carpetas
- Agregar una dependencia nueva
- Descubrir un patrón o anti-patrón relevante
- Tomar una decisión de arquitectura
```

---

## Paso 3 — Crear los agentes según el tipo de proyecto

Crear solo los agentes relevantes en `.claude/agents/`.
Preguntar al usuario cuáles incluir si no es obvio.

### Agentes disponibles en el kit:

| Agente | Archivo | Usar cuando |
|--------|---------|-------------|
| Backend implementer | `backend-impl.md` | Cualquier proyecto con lógica de servidor |
| Security reviewer | `security-reviewer.md` | Siempre — todo proyecto |
| Test writer | `test-writer.md` | Siempre — todo proyecto |
| API explorer | `api-explorer.md` | Al analizar APIs externas o repos |
| Frontend implementer | `frontend-impl.md` | Proyectos con UI |

### Por tipo de proyecto:

**Backend API:**
backend-impl + security-reviewer + test-writer + api-explorer

**Frontend:**
frontend-impl + security-reviewer + test-writer

**Fullstack:**
backend-impl + frontend-impl + security-reviewer + test-writer

**MCP Server:**
backend-impl + security-reviewer + test-writer + api-explorer

---

## Paso 4 — Verificar el entorno

Antes de terminar, verificar que el kit está montado correctamente:

```
.claude/
├── settings.json          ← viene con el kit
├── agents/                ← al menos los agentes del paso 3
├── commands/              ← commands del kit presentes
├── hooks/                 ← los tres hooks base
│   ├── security_guard.py
│   ├── post_write.py
│   └── context_guardian.py
└── skills/                ← al menos skill-structure y project-setup
```

Si el kit se instaló correctamente (clone de rama dist),
todo lo anterior ya debería existir. Solo verificar que
los agentes del paso 3 están presentes.

Verificar que `.claude/` está en el `.gitignore` del
proyecto. Si no está, agregarlo:
```bash
echo ".claude/" >> .gitignore
```

Si el proyecto necesita permisos adicionales en
`settings.json` (ej: herramientas específicas del stack),
editarlo directamente — es el enfoque esperado.

Si falta alguno, avisar al usuario antes de terminar.

---

## Paso 5 — Confirmar y resumir

Al terminar, mostrar un resumen de lo que se creó:
- Secciones del CLAUDE.md completadas
- Agentes creados
- Qué falta completar manualmente (comandos del proyecto,
  convenciones específicas, fases del proyecto)

---

## Versionado
v1.0 — 2026-04-15 — versión inicial del kit
v1.1 — 2026-04-16 — simplificado Paso 4: settings.json editable directo, agregar .claude/ a .gitignore