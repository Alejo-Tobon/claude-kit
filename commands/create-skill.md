# /create-skill $ARGUMENTS

Lee `.claude/skills/skill-structure/SKILL.md` y
creá una nueva skill llamada $ARGUMENTS siguiendo
ese estándar.

Proceso:
1. Leer la skill-structure para conocer el formato
2. Preguntar qué conocimiento cubre la skill si no
   es obvio por el nombre
3. Proponer 3-7 triggers y confirmar antes de usarlos
4. Escribir el SKILL.md completo
5. Crear el archivo en `.claude/skills/$ARGUMENTS/SKILL.md`
6. Agregar una línea de referencia en
   `.claude/skills/README.md` — crearlo si no existe

No crear el archivo hasta tener el contenido completo
aprobado por el usuario.