---
name: explore-module
description: |
  Cómo analizar un módulo o proyecto pequeño y
  generar su CLAUDE.md desde cero. Cubre la
  exploración de estructura, dependencias, patrones
  existentes y convenciones del código.
triggers:
  - "explore-and-document"
  - "explorar módulo"
  - "documentar módulo"
  - "analizar proyecto"
  - "generar CLAUDE.md"
  - "proyecto existente"
---

## Cuándo aplicar esta skill

Al ejecutar `/explore-and-document` en un módulo
individual o proyecto de tamaño acotado (menos de
~100 archivos de código). Para proyectos más grandes
o monorepos, usar la skill `explore-large`.

---

## Proceso de exploración

### Paso 1 — Leer la estructura antes de tocar código

```bash
# Lo primero: entender qué hay
ls -la
cat package.json       # o pyproject.toml / pom.xml / go.mod
cat README.md          # si existe
```

Identificar:
- Tipo de proyecto (API, frontend, librería, CLI, etc.)
- Stack principal y versiones
- Punto de entrada de la aplicación
- Carpetas principales y su propósito

### Paso 2 — Mapear la estructura de carpetas

Explorar hasta 2 niveles de profundidad. No leer
archivos individuales todavía — solo entender la
organización.

Prestar atención a:
- Separación de capas (routes, controllers, services,
  repositories, models, etc.)
- Carpetas de tests y su relación con el código
- Configuración (config/, env, settings)
- Carpetas no estándar que sugieran patrones propios

### Paso 3 — Analizar dependencias

Leer el archivo de dependencias principal y extraer:
- Framework principal y versión
- ORM o cliente de base de datos
- Librerías de validación
- Librerías de testing
- Herramientas de build/lint

No listar todas — solo las que definen la arquitectura.

### Paso 4 — Identificar patrones del código existente

Leer 3-5 archivos representativos del código:
- Un controller o handler
- Un service o caso de uso
- Un modelo o schema
- Un test si existe

Identificar:
- Convenciones de naming (camelCase, snake_case, etc.)
- Estructura típica de una función o clase
- Manejo de errores
- Patrones de async/await o promesas
- Anti-patrones evidentes que ya existen

### Paso 5 — Revisar configuración de herramientas

Leer si existen:
- `.eslintrc` / `ruff.toml` / equivalente
- `jest.config.js` / `pytest.ini` / equivalente
- `.env.example` para entender variables de entorno

---

## Qué incluir en el CLAUDE.md generado

Usar la estructura de `project-setup/SKILL.md` como
base. Completar con lo encontrado:

**Sí incluir:**
- Stack real con versiones reales del proyecto
- Comandos exactos del package.json / Makefile
- Convenciones de naming que ya usa el código
- Anti-patrones que ya existen (para que el agente
  no los replique)
- Estructura de capas real del proyecto
- Variables de entorno requeridas (nombres, no valores)

**No incluir:**
- Contenido de archivos individuales
- Listado exhaustivo de archivos
- Información que cambia frecuentemente
- Más de 250 líneas en total

---

## Qué hacer si hay inconsistencias en el código

Si el código existente mezcla patrones (algunos archivos
usan una convención, otros otra), documentar la más
predominante y agregar una nota:

```markdown
## Convenciones
[patrón predominante]

> Nota: hay inconsistencias en el código existente.
> El agente debe seguir las convenciones documentadas
> aquí, no las del código legacy que las viola.
```

---

## Al terminar

Mostrar al usuario:
- El CLAUDE.md generado
- Las secciones que quedaron incompletas y por qué
- Las inconsistencias encontradas en el código

Preguntar si hay correcciones antes de guardarlo.

---

## Versionado
v1.0 — 2026-04-01 — versión inicial del kit