#!/usr/bin/env bash
# Genera/actualiza la rama dist desde main.
# Solo incluye el contenido distribuible para proyectos consumidores.

set -euo pipefail

# ── Verificaciones ─────────────────────────────────────────────────────────

current_branch=$(git branch --show-current)
if [[ "$current_branch" != "main" ]]; then
    echo "Error: debes estar en main (estás en $current_branch)"
    exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "Error: hay cambios sin commitear. Commitea o stashea primero."
    exit 1
fi

# ── Contenido distribuible ─────────────────────────────────────────────────

DIST_DIRS=(agents commands hooks skills)
TEMPLATE="settings.json.template"

for dir in "${DIST_DIRS[@]}"; do
    if [[ ! -d "$dir" ]]; then
        echo "Error: $dir/ no encontrado"
        exit 1
    fi
done

if [[ ! -f "$TEMPLATE" ]]; then
    echo "Error: $TEMPLATE no encontrado"
    exit 1
fi

# ── Preparar contenido en directorio temporal ──────────────────────────────

main_sha=$(git rev-parse --short HEAD)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

for dir in "${DIST_DIRS[@]}"; do
    cp -r "$dir" "$tmp/"
done
cp "$TEMPLATE" "$tmp/settings.json"

# Quitar artefactos de Python que no deben distribuirse (los .pyc/__pycache__
# se generan al ejecutar/validar hooks y no son parte del kit).
rm -rf "$tmp"/hooks/__pycache__ "$tmp"/*/__pycache__ 2>/dev/null || true

# ── Cambiar a rama dist ────────────────────────────────────────────────────

if git show-ref --quiet refs/heads/dist; then
    git checkout dist
else
    git checkout --orphan dist
fi

# ── Reconstruir el contenido de dist ───────────────────────────────────────

# Vaciar el índice y borrar SOLO las carpetas distribuibles del working
# tree. No tocar archivos ocultos/personales como .claude/ — borrarlos del
# disco perdería skills personales (gitignored) que viven ahí.
# Al stagear explícitamente solo el contenido distribuible, cualquier
# untracked que persista del checkout (ej: .claude/) nunca entra al commit.
git rm -r --cached . >/dev/null 2>&1 || true
rm -rf agents commands hooks skills settings.json

cp -r "$tmp"/* .

# ── Commitear ──────────────────────────────────────────────────────────────

git add agents commands hooks skills settings.json

if git diff --cached --quiet 2>/dev/null; then
    echo "Sin cambios. dist ya está actualizada."
    git checkout main
    exit 0
fi

git commit -m "dist: update from main ($main_sha)"

echo ""
echo "Rama dist actualizada desde main ($main_sha)"
echo "Para pushear: git push origin dist"
echo ""

git checkout main
