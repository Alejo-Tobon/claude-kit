# claude-kit

Estructura base de Claude Code para proyectos del equipo.
Incluye agentes, skills, commands y hooks listos para usar.

---

## Requisitos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) instalado
- Python 3.10+ (para los hooks)
- Git

---

## Instalación en un proyecto

```bash
git clone -b dist <url-del-repo> .claude
echo ".claude/" >> .gitignore
```

Eso es todo. El `.claude/` del proyecto queda con el kit
completo y git del proyecto lo ignora.

### Actualizar el kit

```bash
cd .claude && git pull
```

### Subir un cambio al kit desde un proyecto

Si editaste algo en `.claude/` y quieres que aplique
a todos tus proyectos:

```bash
cd .claude && git add -A && git commit -m "..." && git push
```

---

## Instalación alternativa (submodule)

Si preferís que el proyecto registre qué versión del kit
usa:

```bash
git submodule add -b dist <url-del-repo> .claude
```

Agregar `ignore = dirty` en `.gitmodules` para que
`git status` no reporte cambios locales del kit:

```
[submodule ".claude"]
    path = .claude
    url = <url>
    branch = dist
    ignore = dirty
```

Actualizar con:
```bash
git submodule update --remote
git commit -m "chore: actualizar claude-kit"
```

---

## Flujo para un proyecto nuevo

```
1. Instalar el kit (clone o submodule)
2. Abrir VSCode en la raíz del proyecto
3. /init          → genera un CLAUDE.md básico
4. /setup-project → reestructura al estándar del kit,
                    crea los agentes según el tipo de proyecto
5. Trabajar
```

## Flujo para un proyecto existente

```
1. Instalar el kit (clone o submodule)
2. Abrir VSCode en la raíz del proyecto
3. /explore-and-document  → analiza el repo y genera el CLAUDE.md
   (o /explore-large      → para repos grandes o monorepos)
4. /review-claude-md      → verifica y ajusta el CLAUDE.md generado
5. Trabajar
```

---

## Contenido del kit

### Agentes — `agents/`

| Agente | Modelo | Para qué |
|---|---|---|
| `backend-impl` | Sonnet | Implementar código de servidor |
| `frontend-impl` | Sonnet | Implementar componentes y páginas |
| `security-reviewer` | Opus | Auditar seguridad — solo lectura |
| `test-writer` | Sonnet | Escribir tests para código existente |
| `api-explorer` | Haiku | Explorar repos y APIs desconocidas |

El command `/setup-project` pregunta qué agentes incluir
y crea solo los relevantes para el tipo de proyecto.

### Skills — `skills/`

| Skill | Para qué |
|---|---|
| `skill-structure` | Cómo crear nuevas skills (meta-skill) |
| `project-setup` | Estándar del CLAUDE.md y proceso de setup |
| `explore-module` | Analizar un módulo o proyecto pequeño |
| `explore-large` | Analizar repos grandes o monorepos |
| `requirements-to-spec` | Convertir un doc de requerimientos en spec para los agentes |

Las skills de dominio (node-api, security, testing, etc.)
no están incluidas en el kit base — se crean por proyecto
con `/create-skill [nombre]`.

### Commands — `commands/`

| Command | Para qué |
|---|---|
| `/setup-project` | Setup inicial del proyecto |
| `/explore-and-document` | Analizar proyecto existente y generar CLAUDE.md |
| `/explore-large` | Analizar repo grande o monorepo |
| `/create-skill [nombre]` | Crear una nueva skill con el formato del kit |
| `/phase-start [número]` | Iniciar una fase del proyecto |
| `/document-decision [texto]` | Registrar una decisión en el CLAUDE.md |
| `/review-claude-md` | Auditar el CLAUDE.md actual |
| `/spec-from-requirements [archivo]` | Convertir un doc de requerimientos en spec para los agentes |

### Hooks — `hooks/`

| Hook | Evento | Para qué |
|---|---|---|
| `security_guard.py` | PreToolUse | Bloquea patrones peligrosos antes del write |
| `post_write.py` | PostToolUse | Formatea el archivo después del write |
| `context_guardian.py` | Stop | Avisa al 55% y bloquea al 70% de contexto |

### `settings.json`

Permisos de Bash y configuración de hooks.
Si el proyecto necesita permisos adicionales
(ej: `docker`, `cargo`, etc.), editarlos directamente
en `.claude/settings.json`.

---

## Agregar skills de dominio

Las skills de dominio son específicas de cada proyecto.
Crearlas con:

```
/create-skill node-api
/create-skill security
/create-skill testing
```

El agente lee `skill-structure/SKILL.md` y genera
el archivo con el formato correcto. Luego se completa
con el conocimiento específico del proyecto.

---

## Personalizar los hooks

Los hooks están diseñados para ser agnósticos al stack.
`post_write.py` detecta la extensión del archivo y corre
el formatter correspondiente. Si el proyecto usa un
formatter diferente, editar el diccionario `FORMATTERS`
en el archivo.

`security_guard.py` tiene dos tipos de reglas:
- `BLOCKED_PATTERNS` — bloquean el write con exit 2
- `WARNING_PATTERNS` — emiten advertencia sin bloquear

Agregar reglas específicas del proyecto en cualquiera
de las dos listas.

---

## Desarrollo del kit

El contenido distribuible vive en la raíz del repo
(agents/, commands/, hooks/, skills/). La rama `dist`
contiene solo ese contenido, sin archivos de desarrollo.

Para generar/actualizar la rama dist:

```bash
bash .claude/scripts/release-dist.sh
git push origin dist
```

El script verifica que estés en `main` con working tree
limpio, copia el contenido distribuible a la rama `dist`
y renombra `settings.json.template` → `settings.json`.

---

## Estructura del kit

```
agents/
├── backend-impl.md
├── frontend-impl.md
├── security-reviewer.md
├── test-writer.md
└── api-explorer.md
commands/
├── setup-project.md
├── explore-and-document.md
├── explore-large.md
├── create-skill.md
├── phase-start.md
├── document-decision.md
├── review-claude-md.md
└── spec-from-requirements.md
hooks/
├── security_guard.py
├── post_write.py
└── context_guardian.py
skills/
├── skill-structure/SKILL.md
├── project-setup/SKILL.md
├── explore-module/SKILL.md
├── explore-large/SKILL.md
└── requirements-to-spec/SKILL.md
settings.json.template
```
