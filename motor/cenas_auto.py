# DIRETOR AUTOMÁTICO: monta as cenas a partir de work/episodio.json (sem escrever cena à mão).
# Rodado pelo motor.py (exec). Tolerante: nome desconhecido vira padrão em vez de quebrar.
exec(open('work/cenas_lib.py', encoding='utf-8').read())
import json
EP = json.load(open('work/episodio.json', encoding='utf-8'))
if EP.get("formato") == "short":
    SHORT = {"t1": EP.get("short", {}).get("t1", ""), "t2": EP.get("short", {}).get("t2", ""), "bg": EP.get("short", {}).get("bg", "escritorio"),
             "fs2": EP.get("short", {}).get("fs2", 104)}

PRESETS = {"ROMANO": ROMANO, "LAVANDAIO": LAVANDAIO, "IMPERATORE": IMPERATORE, "VITTORIANA": VITTORIANA, "SIGNORE": SIGNORE,
           "TOSHER": TOSHER, "SVUOTATORE": SVUOTATORE, "CONCIATORE": CONCIATORE, "RE": RE, "NORRIS": NORRIS, "REGINA": REGINA}
SVG_NOMES = ["XICARA", "RELOGIO", "POTE", "VIDRO_SANG", "TERMOMETRO", "CAIXA", "MOEDA", "LANTERNA", "BALDE", "PA", "TOALHA", "CADERNO",
             "LUPA", "FACA", "TACA", "PERGAMENA", "BORSA", "CANDELA"]                       # objetos de mão
EXTRA_NOMES = ["CARTOLA", "BONE", "FONE", "LENCO", "SUJEIRA", "COROA", "BARBA", "LOUROS"]  # coisas na cabeça
DESENHOS = {"CACCA": (CACCA, "0 0 200 200"), "CACCA_BRANCA": (CACCA_BRANCA, "0 0 200 200"), "TOPO": (TOPO, "0 0 220 200"), "MAIALE": (MAIALE, "0 0 220 200"),
            "SGABELLO": (SGABELLO, "0 0 200 200"), "LAPIDE": (LAPIDE_RIP, "0 0 200 200"), "MACHADO": (MACHADO, "0 0 200 200"), "CANE": (CANE, "0 0 200 200"),
            "GAS": (GAS, "0 0 200 200"), "PODIO": (PODIO, "0 0 200 200"), "GOTA": (GOTA, "0 0 110 150"), "PIPI": (PIPI, "0 0 110 150"), "UVA": (UVA, "0 0 170 200"),
            "CORACAO": (CORACAO, "0 0 120 120"), "COROA": (COROA, "70 -40 100 70"), "BORSA": (BORSA, "-34 -26 68 60"), "CANDELA": (CANDELA, "-40 -80 80 84"),
            "TACA": (TACA, "-24 -46 48 56"), "PERGAMENA": (PERGAMENA, "-28 -40 56 60"), "LUPA": (LUPA, "-22 -44 46 54"), "RELOGIO": (RELOGIO, "-34 -66 68 76")}
SOBS, BOCAS, POSES = set(SOB), set(BOCA), set(POSE)
LUZES = set(LUZ)
def ok(v, validos, padrao): return v if v in validos else padrao
def bg_ok(nome):
    import os
    return nome if nome and os.path.exists(f"assets/hd/{nome}.jpg") else "escritorio"

def personagem(c):
    sob = ok(c.get("sob"), SOBS, "normal"); boca = ok(c.get("boca"), BOCAS, "fechada"); pose = ok(c.get("pose"), POSES, "baixo")
    prop = globals()[c["prop"]] if c.get("prop") in SVG_NOMES else ""
    p = c.get("p", "custom")
    if p == "mr": return mr(pose, sob, prop, boca)
    if p in PRESETS: return PRESETS[p](sob=sob, boca=boca, pose=pose, prop=prop)
    extra = "".join(globals()[e] for e in c.get("extra", []) if e in EXTRA_NOMES)
    return bon(roupa=ok(c.get("roupa"), {"camisa", "terno", "vestido", "jaleco", "nobre"}, "camisa"), cor=c.get("cor", "#d97b37"),
               cabelo=ok(c.get("cabelo"), set(CABELO), "curto"), cc=c.get("cc", "#6b3a1e"), extra=extra, pose=pose, sob=sob, boca=boca, prop=prop)

def plano(v):
    if isinstance(v, (list, tuple)) and len(v) == 2: return tuple(v)
    return v if v in PLANO else "plano"

def acha(i0, i1, palavra):
    """linha (dentro da cena) onde a palavra aparece; None se não achar"""
    if not palavra: return i0
    for i in range(i0, i1 + 1):
        for x in LIN[i]["words"]:
            if x[0].lower().strip(".,!?:;…'\"«»").startswith(palavra.lower()): return i
    return None

ICON_POS = [(330, 300), (1590, 300), (330, 560), (1590, 560)]
li = 0
for k, sc in enumerate(EP["cenas"]):
    n = max(1, len(sc.get("falas", [])))
    i0, i1 = li, min(li + n - 1, len(LIN) - 1); li += n
    if i0 >= len(LIN): break
    cid = f"s{k}"
    if sc.get("titulo"):
        t = sc["titulo"]; titulo(cid, i0, bg_ok(sc.get("bg")), ok(sc.get("luz"), LUZES, "quente"), t.get("num", ""), t.get("nome", ""), t.get("sub")); continue
    chars = [(personagem(c), int(c.get("x", 960)), plano(c.get("plano"))) for c in sc.get("chars", [])[:4]]
    etqs = []
    for e in sc.get("etiquetas", [])[:3]:
        i = acha(i0, i1, e.get("palavra"))
        if i is None: continue
        etqs.append((i, e.get("palavra"), str(e.get("texto", "")).upper()[:28], ok(e.get("estilo"), {"am", "br", "vm", "pt"}, "am"),
                    int(e.get("x", 960)), int(e.get("y", 140)), random.choice([-4, -3, 3, 4]), int(e.get("tam", 120))))
    efx = []
    for f in sc.get("fx", []):
        i = acha(i0, i1, f.get("palavra"))
        if i is not None and f.get("tipo") in ("treme", "soco", "confete"): efx.append((f["tipo"], i, f.get("palavra")))
    icones = []
    for j, ic in enumerate(sc.get("icones", [])[:2]):
        if ic.get("svg") not in DESENHOS: continue
        i = acha(i0, i1, ic.get("palavra"))
        if i is None: continue
        svg, vb = DESENHOS[ic["svg"]]; x, y = ICON_POS[(k + j) % 4]
        icones.append((f"{cid}i{j}", svg, vb, x, y, wt(i, ic["palavra"]) if ic.get("palavra") else None, int(ic.get("tam", 260))))
    acao = sc.get("acao")
    def ex(c, icones=icones):
        for iid, svg, vb, x, y, t, tam in icones: c.svg(desenho(iid, svg, x - tam // 2, y - tam // 2, tam, tam, vb), "pers")
    def post(c, p, a, b, icones=icones, acao=acao, ultima=(k == len(EP["cenas"]) - 1)):
        for iid, svg, vb, x, y, t, tam in icones:
            tt = a + 0.15 if t is None else t
            esconde(iid); de(iid, tt, 0.28, "scale: 0, opacity: 1", "scale: 1, opacity: 1", "back.out(3)"); som("pop.mp3", tt, 0.35)
        if p:
            if acao == "anda": anda(p[0], a, b)
            elif acao == "entra": de(p[0], a, 0.35, "x: -1300", "x: 0", "power3.out")
            elif acao == "cai": de(p[0], a, 0.55, "y: -900", "y: 300", "power2.in"); som("splash.mp3", a + 0.55, 0.4, 1.2)
            elif acao == "afunda": J(f'tl.to("#{p[0]}", {{ y: 260, duration: 0.8, ease: "power1.in" }}, {max(a, b - 1.2):.2f});')
            elif acao == "pisa": J(f'tl.fromTo("#{p[0]}", {{ y: 0 }}, {{ y: -40, duration: 0.22, yoyo: true, repeat: {int((b-a)/0.22)}, ease: "power1.out", immediateRender: false }}, {a});')
            if ultima and EP.get("formato") != "short" and chars and chars[0][0].mr:
                tchau(p[0], LIN[-1]["fim"] + 0.1, b)
    S(cid, i0, i1, bg_ok(sc.get("bg")), ok(sc.get("luz"), LUZES, "quente"), chars, etqs, efx,
      corte=ok(sc.get("corte"), {"chicote", "seco", "nenhum"}, "chicote") if k else "nenhum",
      agua_y=sc.get("agua_y"), agua_cor=sc.get("agua_cor", "50,80,50"), blur=int(sc.get("desfoque", 0)), ex=ex, post=post,
      fala=sc.get("fala", True))

# objetos automáticos por palavra também em inglês
if EP.get("idioma", "it") == "en":
    ICONES = [
        (("blood", "bleeding", "bled"), GOTA, "0 0 110 150"), (("pee", "urine", "piss"), PIPI, "0 0 110 150"),
        (("poop", "dung", "feces", "excrement", "shit"), CACCA, "0 0 200 200"), (("rats", "rat"), TOPO, "0 0 220 200"),
        (("coin", "coins", "gold"), MOEDA, "-12 -20 24 24"), (("money", "paid", "salary", "wage", "rich", "tax", "pay"), BORSA, "-34 -26 68 60"),
        (("king", "queen", "royal", "crown", "emperor", "court"), COROA, "70 -40 100 70"), (("heart", "love"), CORACAO, "0 0 120 120"),
        (("candle", "night", "midnight"), CANDELA, "-40 -80 80 84"), (("executed", "beheaded", "axe"), MACHADO, "0 0 200 200"),
        (("smell", "stink", "stench", "smelled"), GAS, "0 0 200 200"), (("bucket",), BALDE, "-30 -50 60 80"), (("knife",), FACA, "-20 -40 60 60"),
        (("wine", "poison", "drink"), TACA, "-24 -46 48 56"), (("dog", "dogs"), CANE, "0 0 200 200"), (("doctor", "doctors"), LUPA, "-22 -44 46 54"),
        (("died", "dead", "death", "grave"), LAPIDE_RIP, "0 0 200 200"), (("hours", "years", "time"), RELOGIO, "-34 -60 68 72"),
    ]
