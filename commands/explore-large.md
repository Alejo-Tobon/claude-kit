# /explore-large

Lee `.claude/skills/explore-large/SKILL.md`.

Antes de empezar, preguntá al usuario cuál de los
dos modos aplica:

> "¿Los módulos ya tienen su propio CLAUDE.md?
> 1. Sí — consolidar desde los CLAUDE.md existentes (Modo B)
> 2. No — explorar el repo y generarlo desde cero (Modo A)"

Según la respuesta, ejecutá el modo correspondiente
de la skill.

Respetá las reglas de gestión del contexto de la skill
— si el contexto supera el 55% durante la exploración,
guardá el estado en session-state.md y avisá antes
de continuar.