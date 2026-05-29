---
name: skill-structure
description: |
  Estándar para crear nuevas skills en este kit.
  Define el formato, las secciones obligatorias y
  las convenciones de naming y triggers.
triggers:
  - "crear skill"
  - "nueva skill"
  - "create-skill"
  - "SKILL.md"
  - "skill structure"
  - "formato de skill"
---

## Cuándo aplicar esta skill

Leer esta skill antes de crear cualquier archivo
`SKILL.md` nuevo. También al revisar o actualizar
skills existentes para verificar consistencia.

---

## Estructura obligatoria de un SKILL.md

```
skills/{nombre}/
├── SKILL.md          ← obligatorio
└── examples/         ← opcional, archivos de referencia
    └── example.ts
```

### El archivo SKILL.md tiene tres partes:

**1. Frontmatter YAML** (obligatorio)
```yaml
---
name: nombre-en-kebab-case
description: |
  Una o dos líneas explicando qué cubre la skill.
  Debe responder: ¿qué sabe el agente al activar esto?
triggers:
  - "término 1"
  - "término 2"
  - "término 3"
---
```

**2. Cuándo aplicar** (obligatorio)
Una sección corta que le dice al agente en qué
contexto es relevante esta skill. Máximo 3 líneas.

**3. Contenido** (obligatorio)
El conocimiento real. Ver secciones recomendadas abajo.

---

## Secciones recomendadas para el contenido

Usar las que apliquen — no todas son necesarias en
todas las skills:

- **Stack / herramientas** — versiones y librerías estándar
- **Estructura / patrones** — cómo organizar el código
- **Anti-patrones prohibidos** — qué nunca hacer
- **Checklist** — pasos de verificación antes de terminar
- **Ejemplos** — referencias a `examples/` si existen
- **Referencias** — links o archivos externos útiles
- **Versionado** — `vX.Y — YYYY-MM-DD — descripción del cambio`

---

## Reglas de naming

| Elemento | Convención | Ejemplo |
|---|---|---|
| Carpeta de la skill | kebab-case | `node-api/` |
| Nombre en frontmatter | kebab-case | `node-api` |
| Triggers | minúsculas, términos naturales | `"endpoint"`, `"route"` |

---

## Reglas de triggers

Los triggers son las palabras clave que hacen que el
agente active la skill automáticamente.

**Buenos triggers:**
- Términos técnicos que el agente usaría en sus propios
  razonamientos internos
- Sustantivos y verbos específicos del dominio
- Nombres de herramientas o patrones

**Malos triggers:**
- Palabras demasiado genéricas (`"código"`, `"proyecto"`)
- Frases largas (usar términos individuales)
- Sinónimos excesivos (3-7 triggers es suficiente)

---

## Longitud y tono

- **Longitud máxima:** ~150 líneas. Si supera eso,
  la skill probablemente cubre demasiado — dividirla,
  o externalizar plantillas a `examples/` (ver abajo).
- **Tono:** instrucciones directas al agente, no
  documentación para humanos. Usar imperativo.
  MAL: "Los endpoints deberían seguir el patrón REST"
  BIEN: "Seguir el patrón REST en todos los endpoints"
- **Sin redundancia:** si una regla ya está en el
  CLAUDE.md del proyecto, no repetirla en la skill.

### Plantillas largas: usar `examples/`

Si hay plantillas de código extensas (típico en scaffolding), moverlas
a `examples/` en vez de violar el límite. El SKILL.md describe el
proceso y referencia las plantillas; el agente las lee al generar:

```
skills/{nombre}/
├── SKILL.md          ← instrucciones, ≤150 líneas
└── examples/
    ├── router.ts
    └── service.ts
```

---

## Patrón para skills de scaffolding

Para skills que generan código (servicios, páginas, clientes). No
aplica a skills de proceso. Estructura de 5 fases + reglas finales:

- **Fase 0 — Declarar rol:** "Actúo como generador… No invento
  lógica… Marco con `// TODO:`". Ancla al agente.
- **Fase 1 — Contexto en un bloque:** 3-8 ítems numerados, una sola
  pregunta, esperar respuesta completa.
- **Fase 2 — Plan y confirmación:** mostrar árbol de archivos antes
  de escribir; pedir OK.
- **Fase 3 — Generar:** crear archivos en orden; borrador en chat
  para los que tienen lógica.
- **Fase 4 — Verificar y cerrar:** listar generados + próximos pasos
  manuales (tipos, lógica, i18n).
- **Reglas finales:** sección enumerada con invariantes (patrones
  obligatorios, anti-patrones, límites por archivo).

---

## Cierre — versionado y registro

Toda skill incluye al final un bloque `## Versionado` con
`vX.Y — YYYY-MM-DD — descripción del cambio` (una línea por versión).
Al crear una skill nueva, agregar también una línea de referencia en
`skills/README.md` para que sea descubrible.

---

## Versionado
v1.0 — 2026-04-01 — versión inicial del kit
v1.1 — 2026-05-28 — patrón para skills de scaffolding + examples/ como escape de longitud