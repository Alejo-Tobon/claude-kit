# /phase-start $ARGUMENTS

Iniciá la fase $ARGUMENTS del proyecto.

1. Leer el CLAUDE.md y verificar que la fase anterior
   está marcada como [x] completada. Si no lo está,
   preguntar si se quiere continuar de todas formas.
2. Leer `.claude/session-state.md` si existe.
3. Revisar los archivos creados o modificados en la
   fase anterior con un git status o git log corto.
4. Describir en 3-4 líneas qué se hará en esta fase
   y cuáles son los archivos principales que se van
   a tocar.
5. Pedir confirmación explícita antes de comenzar.

Al terminar la fase, marcar [x] en el CLAUDE.md y
agregar una entrada en el Registro de decisiones
si se tomó alguna decisión relevante.