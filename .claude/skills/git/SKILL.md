---
name: git
description: |
  Flujo de git para el desarrollo del kit.
  Cubre el modelo de branches (main/dist), el proceso
  de release, y cómo manejar cambios que llegan desde
  proyectos consumidores.
triggers:
  - "git"
  - "branch"
  - "dist"
  - "release"
  - "commit"
  - "push"
  - "merge"
---

## Cuándo aplicar esta skill

Al trabajar con git en este repo: commits, branches,
releases, o al integrar cambios que llegaron desde
un proyecto consumidor.

---

## Modelo de branches

```
main   ← desarrollo del kit (todo)
dist   ← solo contenido distribuible (generada por script)
```

**main:** tiene todo — agents, commands, hooks, skills,
scripts, CLAUDE.md, README, .claude/ del kit.

**dist:** solo lo que va a `.claude/` del consumidor.
Es una rama orphan (sin historia compartida con main).
Nunca se trabaja directo en dist — siempre se genera
desde main con el script de release.

---

## Commits en main

### Convención de mensajes

```
tipo: descripción corta

tipo puede ser:
  feat     → agente, command, skill o hook nuevo
  fix      → corrección de un artefacto existente
  docs     → cambios en CLAUDE.md, README, o skills
  chore    → scripts, CI, configuración del repo
  refactor → reestructuración sin cambio funcional
```

Ejemplos:
```
feat: agregar agente frontend-impl
fix: corregir regex de secrets en security_guard
docs: actualizar README con flujo de clone+gitignore
chore: agregar script de release para rama dist
```

### Qué commitear junto

- Un agente nuevo → un commit
- Un command + la skill que usa → pueden ir juntos
- Cambios en hook + actualización de settings.json.template → juntos
- Actualización de CLAUDE.md → separado si no es parte de otro cambio

---

## Proceso de release (main → dist)

### Prerequisitos
- Estar en main
- Working tree limpio (todo commiteado)

### Pasos
```bash
# 1. Generar/actualizar dist
bash .claude/scripts/release-dist.sh

# 2. Pushear dist al remote
git push origin dist

# 3. Ya estás de vuelta en main
```

### Qué hace el script
1. Verifica que estés en main y limpio
2. Copia agents/, commands/, hooks/, skills/ a un temp
3. Copia settings.json.template → settings.json (renombrado)
4. Cambia a dist (crea orphan si no existe)
5. Limpia todo, pega el contenido, commitea
6. Vuelve a main

### Cuándo hacer release
- Después de agregar o modificar un agente/command/skill/hook
- No hace falta release por cambios en README, CLAUDE.md,
  scripts, o .claude/ del kit — eso no va a dist

---

## Cambios desde proyectos consumidores

Cuando se edita `.claude/settings.json` u otro archivo
del kit directamente en un proyecto consumidor y se
pushea:

```bash
# En el repo del kit (main), traer los cambios
git checkout main

# Los cambios del consumidor están en dist.
# No hacer merge de dist a main — son árboles distintos.
# En su lugar, aplicar el cambio manualmente en main:
# 1. Ver qué cambió en dist
git log dist --oneline -5
git diff dist~1 dist

# 2. Replicar el cambio en los archivos de main
#    (ej: editar settings.json.template con el mismo cambio)

# 3. Commitear en main
git add -A && git commit -m "fix: incorporar cambio desde proyecto X"

# 4. Regenerar dist (ahora incluye el cambio + lo que
#    ya había en main)
bash .claude/scripts/release-dist.sh
git push origin dist
```

### Por qué no mergear dist a main

dist es orphan — no comparte historia con main.
Además los archivos difieren (settings.json vs
settings.json.template, no hay README ni CLAUDE.md).
Mergear crearía conflictos sin sentido.

---

## Anti-patrones

- **No trabajar directo en dist.** Siempre main → script → dist.
- **No hacer merge de dist a main** ni viceversa.
- **No pushear dist sin antes pushear main.** El commit
  de dist referencia el SHA de main — si main no está
  en el remote, la referencia no sirve.
- **No commitear archivos de desarrollo en dist** (CLAUDE.md,
  README, .claude/scripts/, .claude/). El script ya los excluye,
  pero si se manipula dist manualmente se puede romper.

---

## Versionado
v1.0 — 2026-04-16 — versión inicial
