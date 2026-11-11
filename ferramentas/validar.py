# Confere um episodio.json ANTES de produzir. Erros bloqueiam; avisos só informam.
# Uso: python ferramentas/validar.py <episodio.json> [canal_dir]
import json, os, re, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = json.load(open(os.path.join(RAIZ, "roteirista", "catalogo.json"), encoding="utf-8"))
PAL_POR_SEG = {"en": 2.75, "it": 2.75, "es": 2.9, "pt": 2.8}
def checa(caminho):
    ep = json.load(open(caminho, encoding="utf-8")); E, A = [], []
    for k in ("canal", "idioma", "formato", "titulo", "cenas"):
        if k not in ep: E.append(f"falta o campo '{k}'")
    if E: return E, A, ep
    falas = [f for c in ep["cenas"] for f in c.get("falas", [])]
    if any(not isinstance(f, str) or not f.strip("| ") for f in falas): E.append("fala vazia")
    palavras = sum(len(f.split()) for f in falas)
    seg = palavras / PAL_POR_SEG.get(ep["idioma"], 2.75)
    alvo = (28, 58) if ep["formato"] == "short" else (480, 840)
    if not alvo[0] <= seg <= alvo[1]: E.append(f"duração estimada {seg/60:.1f} min fora do alvo {alvo[0]/60:.1f}-{alvo[1]/60:.1f} ({palavras} palavras)")
    if ep["formato"] == "short" and not ep.get("short", {}).get("t2"): E.append("short sem 'short.t2' (título da faixa de cima)")
    if ep["formato"] == "longo":
        for k in ("descricao", "tags", "thumb"):
            if not ep.get(k): E.append(f"falta '{k}' (obrigatório no vídeo longo)")
    if len(ep["titulo"]) > 70: E.append(f"título com {len(ep['titulo'])} caracteres (máx 70)")
    texto = " ".join(falas).lower()
    cen_ok = set(CAT["cenarios_prontos"]) | set(ep.get("cenarios", {}))
    validos = {"sob": set(CAT["sobrancelhas_sob"]), "boca": set(CAT["bocas"]), "pose": set(CAT["poses"]), "prop": set(CAT["objetos_na_mao_prop"]),
               "p": set(CAT["presets_personagem"]) | {"mr", "custom"}, "cabelo": set(CAT["cabelos"]), "roupa": set(CAT["roupas"])}
    for n, c in enumerate(ep["cenas"]):
        if len(c.get("falas", [])) > 3: A.append(f"cena {n}: {len(c['falas'])} falas (ideal ≤ 3 — cenas curtas prendem mais)")
        if c.get("bg") not in cen_ok: E.append(f"cena {n}: cenário '{c.get('bg')}' não existe nem foi pedido em 'cenarios'")
        if c.get("titulo"): continue
        for ch in c.get("chars", []):
            for k, ok in validos.items():
                if k in ch and ch[k] not in ok: A.append(f"cena {n}: {k}='{ch[k]}' inválido (vira padrão)")
        for e in c.get("etiquetas", []):
            p = (e.get("palavra") or "").lower()
            if p and not re.search(r"\b" + re.escape(p), " ".join(c.get("falas", [])).lower()): E.append(f"cena {n}: etiqueta '{e.get('texto')}' ancorada em '{p}', que não está nas falas da cena")
        for ic in c.get("icones", []):
            if ic.get("svg") not in CAT["desenhos_icones"]: A.append(f"cena {n}: ícone '{ic.get('svg')}' não existe")
    sem_visual = sum(1 for c in ep["cenas"] if not c.get("titulo") and not c.get("chars") and not c.get("icones"))
    if sem_visual > len(ep["cenas"]) * 0.25: A.append(f"{sem_visual} cenas sem personagem nem desenho (fica vazio)")
    if ep["formato"] == "longo" and len(ep["cenas"]) < 45: A.append(f"só {len(ep['cenas'])} cenas para um vídeo longo (ideal 60+, troca a cada 5-10 s)")
    return E, A, ep
if __name__ == "__main__":
    E, A, ep = checa(sys.argv[1])
    for a in A: print("  aviso:", a)
    for e in E: print("  ERRO:", e)
    print("REPROVADO" if E else "APROVADO", f"({len(E)} erros, {len(A)} avisos)")
    sys.exit(1 if E else 0)
