# /review-claude-md

Revisá el CLAUDE.md actual y evaluá su calidad.

Verificar:
1. Que tiene las secciones obligatorias del estándar
   (qué es, stack, comandos, convenciones, agentes,
   skills, dispatch rules, gestión del contexto,
   estado de fases, registro de decisiones,
   cláusula de mantenimiento)
2. Que el stack y los comandos están actualizados
3. Que los agentes listados existen en `.claude/agents/`
4. Que las skills referenciadas existen en `.claude/skills/`
5. Que no supera las 300 líneas
6. Que la cláusula de mantenimiento está presente

Devolver un reporte:
- Secciones presentes ✓ / ausentes ✗
- Secciones desactualizadas o incompletas
- Sugerencias concretas de mejora
- Si supera las 300 líneas: qué mover a docs/

Preguntar si se quiere aplicar las correcciones
sugeridas antes de modificar el archivo.