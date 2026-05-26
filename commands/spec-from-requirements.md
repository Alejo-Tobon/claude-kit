# /spec-from-requirements $ARGUMENTS

Lee `.claude/skills/requirements-to-spec/SKILL.md` y
generá el spec a partir del documento de requerimientos.

$ARGUMENTS es el path al documento de requerimientos.
Si no se indica, preguntá cuál es la fuente antes de
continuar.

Proceso:
1. Leer la skill para conocer el formato del spec
2. Leer el documento de requerimientos indicado
3. Extraer los elementos estructurales (entidades,
   operaciones, pantallas, reglas, actores, RNF)
4. Producir el spec normalizado y mostrarlo
5. Listar las ambigüedades detectadas

No despachar a los agentes de implementación hasta que
el usuario resuelva las ambigüedades bloqueantes y
confirme el spec.
