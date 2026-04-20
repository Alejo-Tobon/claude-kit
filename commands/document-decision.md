# /document-decision $ARGUMENTS

Agregá una entrada en el Registro de decisiones
del CLAUDE.md.

El argumento es la decisión en forma corta.
Ejemplo: `/document-decision JWT en token_store, no en .env`

1. Leer el CLAUDE.md para encontrar la sección
   "Registro de decisiones"
2. Preguntar la razón de la decisión si no fue
   especificada en $ARGUMENTS
3. Agregar la fila con la fecha actual, la decisión
   y la razón
4. Guardar el CLAUDE.md

Si la sección no existe, crearla antes de agregar
la entrada.