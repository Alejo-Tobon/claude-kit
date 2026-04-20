---
name: release
description: |
  Proceso completo de release del kit. Cubre: pre-release
  checks, generación de dist, tagging, changelog, y
  comunicación de cambios breaking a consumidores.
triggers:
  - "release"
  - "dist"
  - "versión"
  - "tag"
  - "changelog"
---

## Cuándo aplicar esta skill

Al preparar una nueva versión del kit para distribución.
No aplicar para commits normales de desarrollo.

---

## Pre-release checklist

Antes de correr el script de release, verificar:

### 1. Consistencia
Correr el agente consistency-checker o verificar
manualmente:
- [ ] Cada artefacto en disco está en el README
- [ ] Cada referencia en README/CLAUDE.md apunta a
  algo que existe
- [ ] settings.json.template referencia hooks reales

### 2. Calidad
Para artefactos nuevos o modificados desde el último
release:
- [ ] Pasar por artifact-reviewer
- [ ] Pasar por kit-security-auditor

### 3. Hooks
- [ ] Los tres hooks corren sin error con input vacío
  ```bash
  echo '{"tool_name":"Write","tool_input":{}}' | python hooks/security_guard.py
  echo '{"tool_name":"Write","tool_input":{}}' | python hooks/post_write.py
  echo '{"context_window":{"input_tokens":0,"context_window_size":100000}}' | python hooks/context_guardian.py
  ```

### 4. Git
- [ ] Estar en main
- [ ] Working tree limpio
- [ ] Main pusheado al remote

---

## Proceso de release

### Paso 1 — Definir la versión

Usar semantic versioning simplificado:
- **Major (v2.0):** cambios breaking — un consumidor
  que actualice podría tener problemas
- **Minor (v1.1):** features nuevas — compatibles con
  lo existente
- **Patch (v1.0.1):** fixes — correcciones sin features

Ejemplos de breaking changes:
- Renombrar un agente o command que los consumidores
  ya usan
- Cambiar el formato de frontmatter
- Eliminar un artefacto
- Cambiar el protocolo de un hook (stdin/exit codes)

### Paso 2 — Actualizar versionado en artefactos

Solo los artefactos que cambiaron necesitan actualizar
su sección de versionado al final del archivo.

### Paso 3 — Generar dist

```bash
bash .claude/scripts/release-dist.sh
```

### Paso 4 — Tag en main

```bash
git tag -a v1.X -m "descripción del release"
git push origin main --tags
```

### Paso 5 — Push dist

```bash
git push origin dist
```

### Paso 6 — Changelog

Actualizar un archivo CHANGELOG.md en main (no en dist)
con el formato:

```markdown
## vX.Y — YYYY-MM-DD

### Agregado
- Nuevo agente X para Y
- Nueva skill Z

### Cambiado
- Agente A ahora usa modelo B
- Hook C detecta patrón D adicional

### Eliminado
- Command E (reemplazado por F)

### Breaking
- Agente G renombrado de H a G
```

---

## Cambios breaking

Si el release incluye cambios breaking:

1. Documentar en CHANGELOG.md qué cambió y qué hacer
2. Si es un rename: dejar un comentario en el commit
   de dist indicando el nombre anterior
3. Considerar si vale la pena: ¿el cambio justifica
   que todos los consumidores tengan que ajustar algo?

---

## Versionado
v1.0 — 2026-04-16 — versión inicial
