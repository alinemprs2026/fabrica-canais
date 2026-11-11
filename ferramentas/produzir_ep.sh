#!/usr/bin/env bash
# Produz um episódio inteiro a partir de UM arquivo: episodio.json (roteiro + cenas + metadados).
# Uso: ferramentas/produzir_ep.sh <episodio.json> <saida.mp4>
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
EP="$(realpath "$1")"; SAIDA="$(realpath -m "$2")"
P="$(mktemp -d)/proj"
mkdir -p "$P/work/voz" "$P/compositions" "$P/assets"
cp -r "$RAIZ"/base/assets/* "$P/assets/"
cp "$RAIZ"/base/package.json "$RAIZ"/base/hyperframes.json "$P/"
echo '{"id":"video","name":"video"}' > "$P/meta.json"
cp "$RAIZ"/motor/*.py "$P/work/"
cp "$EP" "$P/work/episodio.json"
cd "$P"
# roteiro falado = falas das cenas, em ordem ("|" no começo = pausa cômica)
python - <<'PY'
import json
ep = json.load(open("work/episodio.json", encoding="utf-8"))
open("work/roteiro.txt", "w", encoding="utf-8").write("\n".join(f for c in ep["cenas"] for f in c.get("falas", [])) + "\n")
v = {"it": ("it-IT-DiegoNeural", "+10%"), "en": ("en-GB-RyanNeural", "+8%"), "es": ("es-MX-JorgeNeural", "+8%"), "pt": ("pt-BR-AntonioNeural", "+8%")}
voz, rate = v.get(ep.get("idioma", "it"), v["it"])
open("work/voz.env", "w").write(f"VOZ={ep.get('voz', voz)}\nRATE={ep.get('rate', rate)}\n")
PY
set -a; . work/voz.env; set +a
echo "== cenários"; python work/cenarios.py
echo "== voz ($VOZ)"; python work/voz.py work/roteiro.txt
echo "== boca";   python work/boca.py
echo "== trilha"; python work/trilha.py
echo "== cenas";  python work/motor.py work/cenas_auto.py
echo "== render"; npx --yes hyperframes@0.9.28 render -o "$SAIDA"
cp work/episodio.json "${SAIDA%.mp4}.json"
echo "== pronto: $SAIDA"
