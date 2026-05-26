---
name: requirements-to-spec
description: |
  Convierte un documento de requerimientos (en cualquier
  formato) en un spec estructurado que alimenta a los
  agentes de implementación. NO genera código ni scaffolding
  — extrae y normaliza para dar contexto a backend-impl,
  frontend-impl, test-writer y security-reviewer.
triggers:
  - "requerimiento"
  - "spec"
  - "documento funcional"
  - "extraer requisitos"
  - "contextualizar agentes"
  - "implementar desde requerimiento"
---

## Cuándo aplicar esta skill

Cuando existe un documento de requerimientos y el objetivo
es empezar a implementar. Traduce el documento al lenguaje
que los agentes del kit consumen.

---

## Qué hace y qué NO hace

**Hace:** lee el documento, extrae los elementos estructurales
(entidades, endpoints, pantallas, reglas, actores) y produce
un spec normalizado que se reparte a los agentes correctos.

**No hace:** no genera carpetas, schemas, ni código. Eso es
trabajo de backend-impl y frontend-impl. No impone stack —
el stack lo define el CLAUDE.md del proyecto.

---

## Proceso

### Paso 1 — Leer el documento

Aceptar cualquier formato de entrada (.md, .docx, .pdf,
notas sueltas). Leer para extraer información, no para
reformatear.

Si hay varios documentos o ninguno claro, preguntar cuál
es la fuente antes de continuar.

### Paso 2 — Extraer los elementos estructurales

Identificar y listar, sin inventar lo que no esté:

- **Entidades / modelos de datos** — sustantivos del dominio
  con sus atributos si están descritos
- **Endpoints / operaciones** — acciones que el sistema
  expone (crear X, listar Y, actualizar Z)
- **Pantallas / vistas** — interfaces que el usuario ve
- **Actores / roles** — quién usa cada parte
- **Reglas de negocio** — condiciones, validaciones,
  restricciones
- **Requisitos no funcionales** — seguridad, rendimiento,
  volumetría

Marcar como `[AMBIGUO]` lo que esté incompleto o contradictorio.
No rellenar vacíos con suposiciones.

### Paso 3 — Normalizar al spec

Producir un único bloque markdown con esta estructura:

```markdown
# Spec — [nombre del proyecto/feature]

## Entidades
- [Entidad]: [atributos conocidos] | [AMBIGUO: qué falta]

## Operaciones (backend)
- [verbo + recurso]: [descripción] → actor: [rol]

## Pantallas (frontend)
- [nombre]: [qué muestra/permite] → operaciones: [refs]

## Reglas de negocio
- RN: [condición → acción]

## No funcionales
- [atributo]: [valor esperado | AMBIGUO]

## Ambigüedades a resolver antes de implementar
- [lista de lo marcado AMBIGUO]
```

### Paso 4 — Repartir a los agentes

Según lo que tenga el proyecto en `.claude/agents/`:

| Sección del spec | Agente que la consume |
|---|---|
| Entidades + Operaciones | backend-impl |
| Pantallas | frontend-impl |
| Reglas + No funcionales | security-reviewer (revisión) |
| Operaciones + Reglas | test-writer (casos) |

No despachar a un agente que no exista en el proyecto.

### Paso 5 — Confirmar antes de implementar

Mostrar el spec y la lista de ambigüedades. **No iniciar
implementación** si hay ambigüedades bloqueantes — primero
resolverlas con el usuario.

---

## Anti-patrones

- **Inventar requisitos** que no están en el documento
- **Generar código o carpetas** — esta skill solo extrae
- **Imponer un stack** — el spec es agnóstico, el stack
  sale del CLAUDE.md
- **Despachar sin confirmar** cuando hay ambigüedades

---

## Versionado
v1.0 — 2026-05-26 — versión inicial
