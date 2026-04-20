---
name: consistency-check
description: |
  Checklist de consistencia entre artefactos del kit.
  Verifica que todo lo que existe esté referenciado
  donde debe, y que no haya referencias rotas a cosas
  que no existen.
triggers:
  - "consistency"
  - "consistencia"
  - "verify-kit"
  - "verificar kit"
  - "referencias rotas"
  - "desincronizado"
---

## Cuándo aplicar esta skill

Antes de hacer release, o después de agregar, renombrar
o eliminar un artefacto del kit.

---

## Puntos de verificación

### 1. Agentes distribuibles (agents/)

Para cada archivo en `agents/`:
- [ ] Está listado en el README.md (tabla de agentes)
- [ ] Está listado en `skills/project-setup/SKILL.md`
  (tabla de agentes por tipo de proyecto)
- [ ] El nombre del archivo coincide con el `name` del
  frontmatter (kebab-case)
- [ ] Si referencia una skill, esa skill existe en skills/

### 2. Commands distribuibles (commands/)

Para cada archivo en `commands/`:
- [ ] Está listado en el README.md (tabla de commands)
- [ ] Si referencia una skill, esa skill existe en skills/
- [ ] Si referencia un agente, ese agente existe en agents/

### 3. Skills distribuibles (skills/)

Para cada carpeta en `skills/`:
- [ ] Tiene un SKILL.md dentro
- [ ] Está listada en el README.md (tabla de skills)
- [ ] Los triggers no se solapan con triggers de otra skill
- [ ] Tiene versionado al final

### 4. Hooks (hooks/)

Para cada archivo en `hooks/`:
- [ ] Está listado en el README.md (tabla de hooks)
- [ ] Está referenciado en settings.json.template
  (sección hooks con el path correcto)
- [ ] El path en settings.json.template coincide con
  la ubicación real del archivo

### 5. settings.json.template

- [ ] Los paths de hooks apuntan a archivos que existen
- [ ] Los matchers de hooks cubren las tools correctas
- [ ] Los permisos en allow no contradicen los de deny

### 6. README.md

- [ ] Toda tabla del README tiene una fila por cada
  artefacto real del directorio correspondiente
- [ ] No hay filas que referencien artefactos inexistentes
- [ ] La estructura del kit al final del README coincide
  con los archivos reales en disco

### 7. CLAUDE.md

- [ ] La estructura listada coincide con la real
- [ ] Las convenciones documentadas son consistentes
  con los artefactos existentes
- [ ] El registro de decisiones no contradice el estado
  actual del kit

---

## Proceso de verificación

1. Listar todos los archivos en agents/, commands/,
   hooks/, skills/
2. Para cada uno, verificar los puntos de su categoría
3. Leer README.md y verificar que las tablas coinciden
4. Leer CLAUDE.md y verificar la estructura
5. Leer settings.json.template y verificar los paths
6. Reportar inconsistencias encontradas

---

## Formato de reporte

```
VERIFICACIÓN DE CONSISTENCIA — claude-kit

INCONSISTENCIAS:
- [tipo] descripción — qué falta o qué sobra

REFERENCIAS ROTAS:
- [archivo] referencia a [X] pero X no existe

TODO CONSISTENTE:
- [lista de categorías sin problemas]
```

---

## Versionado
v1.0 — 2026-04-16 — versión inicial
