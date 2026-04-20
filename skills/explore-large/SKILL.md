---
name: explore-large
description: |
  Cómo analizar un repo grande o monorepo y generar
  su CLAUDE.md sin saturar el contexto. Usa un enfoque
  por capas: primero exploración superficial del todo,
  luego profundidad selectiva, nunca todo a la vez.
triggers:
  - "explore-large"
  - "explorar monorepo"
  - "documentar monorepo"
  - "repo grande"
  - "consolidar CLAUDE.md"
  - "monorepo"
  - "múltiples módulos"
---

## Cuándo aplicar esta skill

Al ejecutar `/explore-large` en un monorepo o proyecto
con más de ~100 archivos de código. También al ejecutar
`/consolidate-monorepo` para generar el CLAUDE.md raíz
a partir de los CLAUDE.md de los módulos hijos.

---

## Dos modos de operación

Esta skill cubre dos situaciones distintas. Leer cuál
aplica antes de continuar.

---

## Modo A — Repo grande sin CLAUDE.md existentes

Para repos grandes donde ningún módulo tiene CLAUDE.md
todavía. El objetivo es generar el CLAUDE.md raíz con
suficiente contexto para trabajar, sin leer todo.

### Fase 1 — Mapa superficial (no leer código aún)

```bash
ls -la                    # raíz del repo
ls packages/ apps/ src/   # según estructura del monorepo
cat package.json           # o equivalente raíz
```

Identificar:
- Tipo de monorepo (nx, turborepo, lerna, custom)
- Cuántos módulos/packages hay
- Nombres y propósito aparente de cada módulo
- Stack compartido en la raíz

### Fase 2 — Explorar selectivamente 2-3 módulos

No explorar todos. Elegir:
- El módulo más central o más grande
- Un módulo representativo del stack típico
- El módulo con más dependencias internas

Para cada uno: leer solo `package.json` + estructura
de carpetas de primer nivel. No leer archivos de código.

### Fase 3 — Generar el CLAUDE.md raíz

El CLAUDE.md raíz solo documenta:
- Stack compartido y herramientas de build del monorepo
- Convenciones globales (git, naming, estructura)
- Cómo se comunican los módulos entre sí
- Comandos globales (build all, test all, lint all)
- Lista de módulos con una línea de descripción cada uno
- Agentes transversales disponibles
- Reglas de dispatch globales

**No incluir** en el raíz lo que es específico de
cada módulo — eso va en el CLAUDE.md de cada módulo.

---

## Modo B — Consolidar desde CLAUDE.md existentes

Para cuando los módulos ya tienen su propio CLAUDE.md
(generado con `/explore-and-document` o escrito
manualmente). Este es el modo más eficiente.

### Proceso

1. Leer todos los CLAUDE.md de los módulos hijos:
   ```bash
   cat packages/*/CLAUDE.md
   cat apps/*/CLAUDE.md
   ```

2. Extraer de cada uno:
   - Stack específico del módulo
   - Propósito en 1 línea
   - Agentes disponibles en ese módulo
   - Dependencias hacia otros módulos

3. Generar el CLAUDE.md raíz con:
   - Stack compartido (lo que aparece en todos)
   - Tabla de módulos: nombre · propósito · stack particular
   - Convenciones globales (las que son consistentes en todos)
   - Inconsistencias detectadas entre módulos (para avisarle
     al agente que existen y cuál es el estándar)
   - Agentes transversales (los que aplican a todos los módulos)
   - Regla de dónde abrir VSCode según la tarea

4. No releer código — confiar en los CLAUDE.md hijos.
   Si hay dudas sobre un módulo, indicarlo en el CLAUDE.md
   raíz como "pendiente de verificación".

---

## Gestión del contexto en repos grandes

Al analizar repos grandes el contexto se llena rápido.
Aplicar estas reglas:

**Regla 1 — No leer archivos completos**
Solo leer los primeros 50-100 líneas de archivos de
código para identificar patrones. Usar Grep para buscar
patrones específicos en lugar de leer todo.

**Regla 2 — Un módulo por vez**
Si hay que profundizar en varios módulos, hacerlo en
sesiones separadas. Al terminar cada módulo, documentar
lo encontrado antes de pasar al siguiente.

**Regla 3 — Devolver resúmenes, no contenido**
Al final de la exploración, el agente devuelve el
CLAUDE.md generado — no el contenido de los archivos
leídos. El orquestador no necesita ver el código.

**Regla 4 — Avisar si el contexto se acerca al 55%**
Antes de continuar explorando, verificar el contexto.
Si supera el 55%, guardar lo explorado hasta ese punto
en session-state.md y continuar en la próxima sesión.

---

## Estructura recomendada del CLAUDE.md raíz

```markdown
# CLAUDE.md — [nombre del monorepo]

## Qué es este monorepo
[2-3 líneas de propósito global]

## Herramientas de build
[nx / turborepo / lerna + comandos globales]

## Stack compartido
[dependencias y herramientas presentes en todos los módulos]

## Módulos
| Módulo | Propósito | Stack particular | CLAUDE.md |
|--------|-----------|-----------------|-----------|
| packages/auth | Autenticación | Node + JWT | ✓ |
| packages/orders | Gestión de órdenes | Node + Prisma | ✓ |

## Convenciones globales
[solo las que aplican en TODOS los módulos]

## Dónde abrir VSCode
- Feature en un módulo → abrir desde el módulo
- Tarea cross-módulo → abrir desde la raíz
- Agente transversal → abrir desde la raíz

## Agentes transversales
[agentes del .claude/agents/ raíz disponibles en todos]

## Reglas de dispatch
[dispatch rules globales]
```

---

## Versionado
v1.0 — 2026-04-01 — versión inicial del kit