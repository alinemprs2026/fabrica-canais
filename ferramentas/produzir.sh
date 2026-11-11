#!/usr/bin/env bash
# Produz um vídeo a partir de um roteiro + arquivo de cenas.
# Uso: ferramentas/produzir.sh <roteiro.txt> <cenas.py> <saida.mp4>
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
ROTEIRO="$(realpath "$1")"; CENAS="$(realpath "$2")"; SAIDA="$(realpath -m "$3")"
P="$(mktemp -d)/proj"
mkdir -p "$P/work/voz" "$P/compositions" "$P/assets"
cp -r "$RAIZ"/base/assets/* "$P/assets/"
cp "$RAIZ"/base/package.json "$RAIZ"/base/hyperframes.json "$P/"
echo '{"id":"video","name":"video"}' > "$P/meta.json"
cp "$RAIZ"/motor/*.py "$P/work/"
cp "$CENAS" "$P/work/cenas.py"
cd "$P"
echo "== voz";    python work/voz.py "$ROTEIRO"
echo "== boca";   python work/boca.py
echo "== trilha"; python work/trilha.py
echo "== cenas";  python work/motor.py work/cenas.py
echo "== render"; npx --yes hyperframes@0.9.28 render -o "$SAIDA"
echo "== pronto: $SAIDA"
