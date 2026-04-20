---
name: prompt-quality
description: |
  Criterios para evaluar y escribir artefactos del kit
  (agents, skills, commands). Detecta ambigüedades,
  contradicciones, instrucciones vagas y anti-patrones
  de prompting que se propagarían a todos los consumidores.
triggers:
  - "revisar agente"
  - "revisar skill"
  - "revisar command"
  - "calidad del prompt"
  - "prompt-quality"
  - "artifact-reviewer"
---

## Cuándo aplicar esta skill

Al crear o modificar cualquier artefacto del kit
(agents/, skills/, commands/). También cuando el
agente artifact-reviewer ejecuta una revisión.

---

## Criterios de calidad para agentes

### Frontmatter
- [ ] name en kebab-case
- [ ] description dice qué hace Y qué NO hace
- [ ] tools lista solo las herramientas necesarias
- [ ] model especificado (sonnet/opus/haiku)
- [ ] max_turns definido con un límite razonable

### Instrucciones
- [ ] Primera instrucción: leer el CLAUDE.md del proyecto
- [ ] Proceso numerado paso a paso (no párrafos vagos)
- [ ] Cada paso es una acción concreta, no "analizar y considerar"
- [ ] Restricciones explícitas (qué NO hacer)
- [ ] Formato de retorno definido con límite de tokens

### Anti-patrones en agentes
- **Instrucciones contradictorias:** "nunca modificar archivos"
  pero tools incluye Write/Edit
- **Scope creep:** un agente que hace todo no es útil —
  debe tener un solo rol
- **Retorno indefinido:** si no define formato de retorno,
  el orquestador recibe texto impredecible
- **Sin restricción de archivos:** un agente sin límite de
  "si requiere más de N archivos, preguntar" puede
  generar sprawl descontrolado
- **Uso de palabras blandas:** "considerar", "tal vez",
  "si es posible" — usar imperativos

---

## Criterios de calidad para skills

### Frontmatter
- [ ] name en kebab-case
- [ ] description responde: ¿qué sabe el agente al activar esto?
- [ ] triggers: 3-7, términos técnicos específicos
- [ ] Sin triggers genéricos ("código", "proyecto", "archivo")

### Contenido
- [ ] Sección "Cuándo aplicar" presente (máximo 3 líneas)
- [ ] Instrucciones en imperativo, no en condicional
- [ ] Sin redundancia con el CLAUDE.md del kit
- [ ] Máximo 150 líneas
- [ ] Versionado al final

### Anti-patrones en skills
- **Skill enciclopédica:** si supera 150 líneas, cubre
  demasiado — dividirla
- **Triggers demasiado amplios:** "python" como trigger
  activaría la skill en cualquier contexto Python
- **Instrucciones para humanos:** "los developers deberían..."
  — las skills son para el agente, usar imperativo directo
- **Conocimiento que caduca rápido:** versiones específicas
  de librerías cambian — preferir patrones sobre versiones

---

## Criterios de calidad para commands

### Estructura
- [ ] Delega a una skill o define un proceso corto
- [ ] Usa $ARGUMENTS si recibe parámetros
- [ ] Pide confirmación en puntos irreversibles
- [ ] No repite contenido de la skill — solo orquesta

### Anti-patrones en commands
- **Command que es una skill disfrazada:** si el command
  tiene más de 20 líneas de instrucciones, debería ser
  una skill con un command que la invoque
- **Sin punto de confirmación:** commands que ejecutan
  todo sin preguntar son peligrosos en operaciones
  destructivas
- **Dependencia implícita:** un command que asume que
  otro command se corrió antes sin verificarlo

---

## Checklist rápido para cualquier artefacto

1. Leerlo como si fueras Claude sin contexto previo —
   ¿las instrucciones son claras sin ambigüedad?
2. Buscar "considerar", "tal vez", "si es posible" —
   reemplazar por instrucciones directas
3. Buscar contradicciones entre secciones
4. Verificar que los archivos/paths referenciados existen
5. Verificar que no repite lo que ya dice otro artefacto

---

## Versionado
v1.0 — 2026-04-16 — versión inicial
