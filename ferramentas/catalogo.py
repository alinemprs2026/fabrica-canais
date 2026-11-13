# Gera roteirista/catalogo.json: tudo o que o diretor automático sabe desenhar (nomes válidos).
# Rodar sempre que o motor ganhar personagem/objeto/cenário novo.
import json, os, re, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "motor"))
from bonecos import SOB, BOCA, POSE, CABELO
auto = open(os.path.join(RAIZ, "motor", "cenas_auto.py"), encoding="utf-8").read()
lista = lambda nome: re.findall(r'"([A-Z_]+)"', re.search(rf"{nome} = \[([^\]]*)\]", auto).group(1))
presets = re.findall(r'"([A-Z_]+)":', re.search(r"PRESETS = \{([^}]*)\}", auto, re.S).group(1))
desenhos = re.findall(r'"([A-Z_]+)": \(', re.search(r"DESENHOS = \{(.*?)\}\n", auto, re.S).group(1))
ns = {}; exec(open(os.path.join(RAIZ, "motor", "desenhos_saude.py"), encoding="utf-8").read(), ns)
desenhos += list(ns["SAUDE"])
cenarios = sorted(f[:-4] for f in os.listdir(os.path.join(RAIZ, "base", "assets", "hd")) if f.endswith(".jpg"))
cat = {
    "sobrancelhas_sob": sorted(SOB), "bocas": sorted(k for k in BOCA if not k.startswith("fala")), "poses": sorted(POSE), "cabelos": sorted(CABELO),
    "roupas": ["camisa", "terno", "vestido", "jaleco", "nobre"], "presets_personagem": presets + ["host"],
    "objetos_na_mao_prop": lista("SVG_NOMES") + list(ns["PROPS_SAUDE"]) + [""], "na_cabeca_extra": lista("EXTRA_NOMES"), "desenhos_icones": desenhos,
    "luzes": ["neutra", "quente", "fria", "noite", "madrugada", "dourada", "esgoto", "marrom"],
    "estilos_etiqueta": {"am": "amarelo", "br": "branco", "vm": "vermelho", "pt": "preto c/ letra amarela"},
    "planos": {"plano": "corpo inteiro", "grupo": "corpo inteiro menor (2-4 pessoas)", "medio": "cintura pra cima", "close": "rosto", "longe": "pequeno, distante"},
    "acoes": ["anda", "entra", "cai", "afunda", "pisa"], "efeitos_fx": ["treme", "soco", "confete"], "cortes": ["chicote", "seco"],
    "cenarios_prontos": cenarios,
}
os.makedirs(os.path.join(RAIZ, "roteirista"), exist_ok=True)
json.dump(cat, open(os.path.join(RAIZ, "roteirista", "catalogo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(cat, ensure_ascii=False)[:1500])
