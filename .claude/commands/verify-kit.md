# /verify-kit

Ejecutá una verificación completa del kit antes de release.

Proceso:

1. Leer `.claude/skills/consistency-check/SKILL.md`
2. Ejecutar el checklist completo de consistencia:
   - Verificar que cada artefacto en agents/, commands/,
     hooks/, skills/ está referenciado en README.md
   - Verificar que cada entrada en las tablas del README
     apunta a un archivo que existe
   - Verificar que settings.json.template referencia
     hooks que existen
   - Verificar que la estructura en CLAUDE.md coincide
     con los archivos reales
   - Verificar que los nombres en frontmatter coinciden
     con los nombres de archivo
3. Mostrar el reporte de consistencia
4. Si hay inconsistencias, preguntar si se quiere
   corregir alguna antes de continuar
5. Si todo está consistente, indicar que el kit está
   listo para release con `bash .claude/scripts/release-dist.sh`
