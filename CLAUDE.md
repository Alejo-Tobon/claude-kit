# CLAUDE.md — claude-kit

## Qué es este proyecto

Kit de configuración base de Claude Code para estandarizar el trabajo con agentes en cualquier proyecto. Incluye agents, skills, commands y hooks listos para usar. Se distribuye como git submodule que el proyecto consumidor monta en su `.claude/`.

**Este CLAUDE.md es para el desarrollo del kit, no para los proyectos que lo consumen.**

## Stack

- **Markdown** — agents, commands, skills
- **Python 3.10+** — hooks (security_guard, post_write, context_guardian) y utilidades (model_info, cost_report)
- **JSON** — settings.json.template (permisos y configuración de hooks)
- **Git** — distribución via submodule, rama `dist` para contenido limpio

## Estructura del repo

```
├── agents/              ← plantillas de agentes (5)
├── commands/            ← slash commands (9)
├── hooks/               ← hooks (3) + utilidades (model_info, cost_report)
├── skills/              ← skills con SKILL.md (5)
│   ├── skill-structure/
│   ├── project-setup/
│   ├── explore-module/
│   ├── explore-large/
│   └── requirements-to-spec/
├── .claude/scripts/
│   └── release-dist.sh  ← genera la rama dist desde main
├── settings.json.template
├── README.md
└── CLAUDE.md            ← este archivo (desarrollo del kit)
```

El kit tiene su propio `.claude/` para desarrollo (separado del contenido distribuible):

```
├── .claude/             ← configuración del desarrollo del kit
│   ├── agents/
│   │   ├── artifact-reviewer.md
│   │   ├── kit-security-auditor.md
│   │   ├── consistency-checker.md
│   │   └── kit-researcher.md
│   ├── commands/
│   │   └── verify-kit.md
│   ├── skills/
│   │   ├── git/SKILL.md
│   │   ├── prompt-quality/SKILL.md
│   │   ├── consistency-check/SKILL.md
│   │   └── release/SKILL.md
│   ├── scripts/
│   │   └── release-dist.sh
│   └── settings.json
├── agents/              ← contenido distribuible
├── commands/
├── hooks/
├── skills/
└── ...
```

## Modelo de distribución

El contenido distribuible (agents/, commands/, hooks/, skills/, settings.json.template) vive en la **raíz del repo** — NO dentro de `.claude/`. Esto es intencional.

**Rama `main`:** desarrollo completo del kit (incluye CLAUDE.md, README, `.claude/` propio del kit, scripts de release).

**Rama `dist`:** solo el contenido que va a `.claude/` del proyecto consumidor, aplanado en la raíz. El consumidor hace:
```bash
git submodule add -b dist <url-del-repo> .claude
```

La rama `dist` se genera desde `main` excluyendo archivos de desarrollo del kit.

### settings.json

`settings.json` vive en la rama `dist` y llega al proyecto via submodule/clone. Es editable directamente — si el proyecto necesita permisos extra, se modifican ahí. Si el cambio aplica a todos los proyectos, se sube al repo del kit y se actualiza en los demás.

### Instalación en proyectos

Dos opciones equivalentes:

**Submodule** (queda registrado en el repo):
```bash
git submodule add -b dist <url> .claude
```
Para que `git status` no reporte cambios locales en el submodule, agregar `ignore = dirty` en `.gitmodules`.

**Clone + gitignore** (más simple, sin tracking de versión):
```bash
git clone -b dist <url> .claude
echo ".claude/" >> .gitignore
```
Actualizar con `cd .claude && git pull`.

## Convenciones

### Naming
| Elemento | Convención | Ejemplo |
|----------|-----------|---------|
| Agentes | kebab-case con `.md` | `backend-impl.md` |
| Commands | kebab-case con `.md` | `setup-project.md` |
| Hooks | snake_case con `.py` | `security_guard.py` |
| Skills (carpetas) | kebab-case | `skill-structure/` |
| Skills (archivo) | siempre `SKILL.md` | `skills/explore-module/SKILL.md` |

### Agentes
- Frontmatter YAML obligatorio: name, description, tools, model, max_turns
- Restricciones explícitas de qué NO puede hacer el agente
- Formato de retorno definido con límite de tokens (200-300)
- Instrucción de leer CLAUDE.md del proyecto consumidor antes de actuar

### Skills
- Seguir el estándar definido en `skills/skill-structure/SKILL.md`
- Máximo 150 líneas por skill
- 3-7 triggers por skill
- Versionado al final de cada SKILL.md

### Commands
- Cada command delega a una skill o define un proceso corto
- Usa `$ARGUMENTS` para parámetros del usuario
- Debe esperar confirmación del usuario en puntos clave

### Hooks
- Leen JSON de stdin (formato Claude Code)
- Exit 0 = OK, Exit 2 = bloqueo
- Stdout va al contexto del agente, stderr al usuario
- Timeout máximo definido en settings.json.template
- El payload del evento `Stop` trae `transcript_path` pero NO uso de
  tokens/costo. `context_guardian.py` lee el uso real del transcript
  (suma input + cache_read + cache_creation del último mensaje) y avisa
  a 55%/65% de la ventana del modelo. Es advertencia pura, sin bloqueo.
- `model_info.py` y `cost_report.py` viven en `hooks/` pero NO son hooks
  de evento: son utilidades (data de modelos / parser de costos para
  `/cost-report`). Es el único lugar python distribuible del kit.
- La compactación automática se controla con la env var
  `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` en settings (no con `autoCompactThreshold`,
  que no es una setting real).

## Qué incluir en la rama dist

**Sí incluir:**
- `agents/` completo
- `commands/` completo
- `hooks/` completo
- `skills/` completo
- `settings.json` (renombrado desde settings.json.template)

**No incluir:**
- `CLAUDE.md` (es del kit, no del consumidor)
- `README.md` (es del kit)
- `.claude/` (si existe, es del desarrollo del kit)
- `.git/`, `.github/`, CI config
- Tests del kit
- `.claude/scripts/` (build/release del kit)

## Comandos de desarrollo

- Lint Python: `ruff check hooks/ && ruff format --check hooks/`
- Validar estructura: verificar que cada skill tiene SKILL.md, cada agent tiene frontmatter válido
- Generar rama dist: `bash .claude/scripts/release-dist.sh` (debe ejecutarse desde main, con working tree limpio)

## Registro de decisiones

| Fecha | Decisión | Razón |
|-------|----------|-------|
| 2026-04-15 | Estructura plana en raíz, no bajo .claude/ | El kit es material distribuible; .claude/ se reserva para el desarrollo del propio kit |
| 2026-04-15 | Distribución via rama `dist` | Permite que main tenga archivos de desarrollo sin contaminar el submodule del consumidor |
| 2026-04-15 | Hooks en Python, no en Bash | Portabilidad entre OS, manejo de JSON nativo, más legible |
| 2026-04-15 | settings.json.template como nombre | El consumidor lo renombra a settings.json; evita que se aplique accidentalmente en el repo del kit |
| 2026-04-16 | settings.json editable directamente, sin settings.local.json | Uso personal — si se necesita un cambio puntual se edita directo; si aplica a todos los proyectos se pushea al kit. Sin capa extra de indirección |
| 2026-04-16 | Dos modos de instalación: submodule (con ignore=dirty) o clone+gitignore | Submodule para tracking de versión, clone+gitignore para simplicidad. Ambos usan rama dist |
| 2026-05-26 | Observabilidad de costo on-demand (`/cost-report`), sin hook de tracking | El payload de Stop no trae tokens/costo; el transcript ya es la fuente de verdad. Parsearlo on-demand evita duplicar datos y la lógica de dedup |
| 2026-05-26 | `context_guardian` lee el transcript en vez del payload | El payload de Stop no expone uso de contexto; antes el hook era un no-op silencioso |
| 2026-05-26 | Compactación via `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, no `autoCompactThreshold` | `autoCompactThreshold` no es una setting real, se ignoraba |

## Mantenimiento

Ante cualquier cambio, actualizar este archivo ANTES de marcar la tarea como terminada.

Cuenta como cambio significativo:
- Agregar, renombrar o eliminar un agente, command, hook o skill
- Cambiar el formato del frontmatter o la estructura de skills
- Cambiar convenciones de naming
- Modificar el modelo de distribución
- Cambiar los exit codes o el protocolo de los hooks
