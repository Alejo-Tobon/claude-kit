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

# ── Cambiar a rama dist ────────────────────────────────────────────────────

if git show-ref --quiet refs/heads/dist; then
    git checkout dist
else
    git checkout --orphan dist
    git rm -rf . 2>/dev/null || true
    git clean -fd 2>/dev/null || true
fi

# ── Limpiar y copiar contenido nuevo ──────────────────────────────────────

# Limpiar todo excepto .git (compatible con Windows/Git Bash)
for item in *; do
    rm -rf "$item"
done
cp -r "$tmp"/* .

# ── Commitear ──────────────────────────────────────────────────────────────

git add -A

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
