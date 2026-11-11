import re
# Episódio 1 (italiano) — "Com'era Fare il Lavoro Più Schifoso della Storia"
# Rodado pelo motor.py (exec): todas as funções do motor estão disponíveis aqui.

# ---------------------------------------------------------------- utilidades do episódio
def wt(i, pref, n=1):
    """início da n-ésima palavra da frase i que começa com 'pref'"""
    c = 0
    for x in LIN[i]["words"]:
        if x[0].lower().strip(".,!?:;…'\"«»").startswith(pref.lower()):
            c += 1
            if c == n: return x[1]
    return ini(i)
def fc(i): return ini(i + 1) if i + 1 < len(LIN) else DUR

CAMS = [(1.0, 1.12, 0, -40, 0, -20), (1.14, 1.02, -50, 30, 0, 0), (1.0, 1.1, 60, -60, 0, 0), (1.1, 1.0, 0, 0, -40, 0), (1.0, 1.15, -60, 40, 20, -20)]
_ci = [0]
def cam_auto():
    _ci[0] += 1; return CAMS[_ci[0] % len(CAMS)]
PLANO = {"plano": (1150, 900), "grupo": (1150, 760), "medio": (1480, 1500), "close": (1780, 2000), "longe": (1060, 560)}

class Pers:
    def __init__(self, fn, mr=False, sobs=("normal",), bocas=None, pose="baixo", prop=""):
        self.fn, self.mr, self.sobs, self.bocas, self.pose, self.prop = fn, mr, sobs, bocas, pose, prop
    def __call__(self, pid): return self.fn(pid)
def mr(pose="baixo", sob="convencido", prop="", boca="fechada"):
    return Pers(lambda p: mr_square(p, pose=pose, sob=sob, prop=prop, boca=boca), mr=True, sobs=(sob, "normal"), pose=pose, prop=prop)
def bon(roupa="camisa", cor="#d97b37", cabelo="curto", cc="#6b3a1e", extra="", pose="baixo", sob="normal", boca="fechada", prop="", sobs=None, bocas=None):
    return Pers(lambda p: boneco(p, roupa=roupa, cor=cor, cabelo=cabelo, cor_cabelo=cc, extra_cabeca=extra, pose=pose, sob=sob, boca=boca, prop=prop),
                sobs=sobs or (sob,), bocas=bocas or (boca, "o"), pose=pose, prop=prop)

def S(cid, i0, i1=None, bg="escritorio", luz="quente", chars=(), sts=(), fx=(), corte="chicote", cam=None, blur=0, agua_y=None, agua_cor="50,80,50",
      ex=None, post=None, a=None, b=None, fala=True, cameo=True):
    i1 = i0 if i1 is None else i1
    a = (0 if i0 == 0 else ini(i0)) if a is None else a; b = fc(i1) if b is None else b
    c = Cena(cid, a, b, bg, luz, cam or cam_auto(), corte=corte, blur_bg=blur)
    pids, occ, cabs = [], [], []
    for k, (fn, x, pl) in enumerate(chars):
        pid = f"{cid}{k}"; pe, h = PLANO[pl] if isinstance(pl, str) else pl
        c.personagem(f'<g id="{pid}-act">{fn(pid)}</g>', x, pe, h); pids.append(pid)
        wd = h * 300 / 460; occ.append((x - wd * 0.36, pe - h * 0.86, x + wd * 0.36, pe)); topo = pe - h * 440 / 460
        cabs.append((x - wd * 0.2, topo + h * 0.04, x + wd * 0.2, topo + h * 0.39))
    if agua_y: c.svg(agua(cid, agua_y, agua_cor), "pers")
    for f in fx:
        if f[0] == "confete": c.svg(confete(cid, wt(f[1], f[2]) if f[2] else ini(f[1])), "frente")
    if ex: ex(c)
    c.fechar()
    INFO.append({"cid": cid, "a": c.ini, "b": c.fim, "occ": occ, "mr": any(fn.mr for fn, _, _ in chars), "cameo": cameo, "idx": len(cenas) - 1, "cabs": cabs, "zoom": max(c.cam[0], c.cam[1])})
    for pid, (fn, x, pl) in zip(pids, chars):
        if fn.mr:
            if fala: boca(pid, max(a, ini(i0)), min(b, LIN[i1]["fim"]))
            vida(pid, a, b, fn.sobs)
        else: vida(pid, a, b, fn.sobs, fn.bocas)
    for n, s in enumerate(sts):
        i, pref, txt, est = s[:4]; x, y, r, fs = (list(s[4:]) + [960, 140, random.choice([-4, -3, 3, 4]), 110][len(s[4:]):])[:4]
        pr_, nn_ = (str(pref).split("|") + ["1"])[:2]
        t = wt(i, pr_, int(nn_)) if pref else ini(i)
        st(f"st{cid}{n}", t, b, txt, est, x, y, r, fs)
    for f in fx:
        t = wt(f[1], f[2]) if f[2] else ini(f[1])
        if f[0] == "treme": treme(cid, t, 14, 6); som("impact-bass-1.mp3", t, 0.3)
        if f[0] == "soco": soco(cid, t, 1.12)
    n0 = len(js)
    if post: post(cid, pids, a, b)
    novo = "\n".join(js[n0:])
    for pid, (fn, x, pl) in zip(pids, chars):
        atuar(pid, a, b, fala=fn.mr and fala, sob=fn.sobs[0], bracos=not fn.prop and f'"#{pid}-bE"' not in novo,
              cabeca=f'"#{pid}-cab"' not in novo, base=fn.pose, lado=1 if x < 960 else -1)
    return pids

def titulo(cid, i, bg, luz, num, nome, sub=None):
    def ex(c):
        c.svg(grande(f"{cid}n", num, 960, 380, 220, "#ffd60a"), "topo"); c.svg(grande(f"{cid}t", nome, 960, 600, 100, "#fff"), "topo")
        if sub: c.svg(grande(f"{cid}s", sub, 960, 760, 70, "#e9f5a0"), "topo")
    def post(cid_, p, a, b):
        de(f"{cid}n", a, 0.35, "scale: 2.6, opacity: 0", "scale: 1, opacity: 1", "power3.out"); treme(cid, a + 0.3, 12, 5); som("impact-bass-2.mp3", a + 0.3, 0.45)
        de(f"{cid}t", a + 0.6, 0.35, "y: 60, opacity: 0", "y: 0, opacity: 1", "back.out(2)")
        if sub: de(f"{cid}s", a + 1.0, 0.3, "y: 40, opacity: 0", "y: 0, opacity: 1")
    S(cid, i, i, bg, luz, ex=ex, post=post, cam=(1.0, 1.15, -100, 60, 0, 0), cameo=False)

def icone(id_, svg, x, y, wd, h, vb="0 0 200 200", t=None):
    """desenho que aparece com 'pop' no tempo t"""
    def ex(c): c.svg(desenho(id_, svg, x, y, wd, h, vb), "pers")
    def post(cid, p, a, b):
        tt = a + 0.1 if t is None else t
        esconde(id_); de(id_, tt, 0.25, "scale: 0, opacity: 1", "scale: 1, opacity: 1", "back.out(3)"); som("pop.mp3", tt, 0.35)
    return ex, post
def tchau(pid, t0, t1):
    t, k = t0, 0
    while t < t1 - 0.3:
        pose(pid, t, "acena" if k % 2 == 0 else "acena2", 0.16); t += 0.22; k += 1
    expr(pid, t0, sob="convencido", bo="sorrisao"); pulo(f"#{pid}-act", t0 + 0.3, 30); pulo(f"#{pid}-act", t0 + 1.2, 22)
    st("sttchau", t0 + 0.2, t1, "MR. SQUARINGTON", "br", 640, 340, 3, 110)
POSE["acena2"] = ((14, 8), (120, 150))
def junta(*fs):
    def f(*a):
        for x in fs:
            if x: x(*a)
    return f

# ---------------------------------------------------------------- desenhos extras
K = "#111"
CACCA = f'<path d="M30 150 Q20 120 60 112 Q40 84 80 72 Q66 40 100 30 Q110 50 120 54 Q150 70 136 92 Q176 104 160 132 Q190 150 160 166 L40 166 Q20 160 30 150 Z" fill="#7a4a22" stroke="{K}" stroke-width="8" stroke-linejoin="round"/><circle cx="80" cy="120" r="7" fill="#fff"/><circle cx="116" cy="120" r="7" fill="#fff"/>'
CACCA_BRANCA = CACCA.replace("#7a4a22", "#e9e2cf")
TOPO = f'<ellipse cx="100" cy="120" rx="70" ry="42" fill="#7d7d85" stroke="{K}" stroke-width="7"/><circle cx="166" cy="100" r="30" fill="#7d7d85" stroke="{K}" stroke-width="7"/><circle cx="160" cy="70" r="14" fill="#c9a0a0" stroke="{K}" stroke-width="5"/><circle cx="178" cy="96" r="5" fill="#e63946"/><path d="M30 130 Q-10 150 10 180" stroke="{K}" stroke-width="7" fill="none"/><path d="M194 108 L214 104 M194 114 L214 118" stroke="{K}" stroke-width="3"/>'
MAIALE = f'<ellipse cx="100" cy="110" rx="80" ry="55" fill="#2a1a1a" stroke="{K}" stroke-width="7"/><circle cx="170" cy="96" r="38" fill="#2a1a1a" stroke="{K}" stroke-width="7"/><ellipse cx="200" cy="104" rx="14" ry="11" fill="#5a2a2a"/><circle cx="168" cy="84" r="6" fill="#ff2b2b"/><path d="M150 64 L158 44 L170 62 Z" fill="#2a1a1a"/><path d="M50 160 L50 190 M80 162 L80 192 M120 162 L120 192 M150 158 L150 188" stroke="#2a1a1a" stroke-width="14"/>'
SGABELLO = f'<rect x="30" y="60" width="140" height="70" rx="20" fill="#8e1b2e" stroke="{K}" stroke-width="8"/><ellipse cx="100" cy="72" rx="34" ry="12" fill="#2a0a0a"/><path d="M40 130 L30 190 M160 130 L170 190 M70 130 L66 190 M130 130 L134 190" stroke="#c9a227" stroke-width="10"/><rect x="26" y="124" width="148" height="12" fill="#f2c230" stroke="{K}" stroke-width="5"/>'
COROA = f'<path d="M78 20 L84 -24 L104 4 L120 -30 L136 4 L156 -24 L162 20 Z" fill="#f2c230" stroke="{K}" stroke-width="5" stroke-linejoin="round"/><circle cx="120" cy="2" r="6" fill="#e63946"/>'
BARBA = f'<path d="M70 96 Q72 150 120 160 Q168 150 170 96 Q150 118 120 116 Q90 118 70 96 Z" fill="#b5651d" stroke="{K}" stroke-width="5"/>'
LOUROS = f'<path d="M66 30 Q120 0 174 30" stroke="#3e8e2a" stroke-width="10" fill="none"/>' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="11" ry="6" fill="#4caf50" stroke="{K}" stroke-width="2.5" transform="rotate({r} {x} {y})"/>' for x, y, r in [(76, 24, -40), (94, 14, -25), (112, 9, -10), (130, 9, 10), (148, 14, 25), (166, 24, 40)])
BALDE = f'<g transform="translate(0 10)"><path d="M-22 -26 L22 -26 L16 22 L-16 22 Z" fill="#9aa3ad" stroke="{K}" stroke-width="4"/><path d="M-22 -26 Q0 -50 22 -26" stroke="{K}" stroke-width="3" fill="none"/></g>'
PA = f'<g transform="rotate(20)"><rect x="-3" y="-70" width="6" height="70" fill="#8a5a2b" stroke="{K}" stroke-width="2"/><path d="M-16 0 L16 0 L12 30 L-12 30 Z" fill="#9aa3ad" stroke="{K}" stroke-width="3"/></g>'
TOALHA = f'<path d="M-18 -10 L18 -10 L16 26 L-16 26 Z" fill="#fff" stroke="{K}" stroke-width="4"/><path d="M-16 0 L16 0" stroke="#c9a227" stroke-width="3"/>'
CADERNO = f'<rect x="-18" y="-30" width="36" height="44" fill="#f5ecd0" stroke="{K}" stroke-width="4"/><path d="M-12 -18 L12 -18 M-12 -8 L12 -8 M-12 2 L8 2" stroke="#555" stroke-width="2"/>'
LUPA = f'<circle cx="0" cy="-22" r="16" fill="#cfe9f3" stroke="{K}" stroke-width="5"/><path d="M8 -10 L18 6" stroke="{K}" stroke-width="7"/>'
FACA = f'<path d="M0 0 L0 -14 L36 -20 L36 -12 Z" fill="#cfd5db" stroke="{K}" stroke-width="3"/><rect x="-16" y="-14" width="16" height="10" fill="#6b3a1e" stroke="{K}" stroke-width="3"/>'
TACA = f'<path d="M-14 -40 L14 -40 Q16 -16 0 -12 Q-16 -16 -14 -40 Z" fill="#fde8f0" stroke="{K}" stroke-width="4"/><path d="M0 -12 L0 6 M-10 6 L10 6" stroke="{K}" stroke-width="4"/>'
PERGAMENA = f'<rect x="-22" y="-34" width="44" height="50" fill="#f5e6c4" stroke="{K}" stroke-width="4"/><circle cx="0" cy="12" r="8" fill="#c1121f" stroke="{K}" stroke-width="3"/>'
BORSA = f'<path d="M-18 -10 Q-26 24 0 26 Q26 24 18 -10 Z" fill="#c9a26b" stroke="{K}" stroke-width="4"/><path d="M-10 -12 L10 -12" stroke="{K}" stroke-width="5"/><text x="0" y="16" text-anchor="middle" font-family="Bangers" font-size="22">$</text>'
CANDELA = f'<rect x="-6" y="-30" width="12" height="30" fill="#f5ecd0" stroke="{K}" stroke-width="3"/><path d="M0 -44 Q8 -36 0 -30 Q-8 -36 0 -44 Z" fill="#ffb703"/><circle cx="0" cy="-36" r="36" fill="#ffd36b" opacity=".2"/>'
LAPIDE = f'<path d="M30 190 L30 70 Q30 20 100 20 Q170 20 170 70 L170 190 Z" fill="#9aa0a6" stroke="{K}" stroke-width="8"/><text x="100" y="100" text-anchor="middle" font-family="Bangers" font-size="40" fill="#333">RICHARD</text><text x="100" y="146" text-anchor="middle" font-family="Bangers" font-size="34" fill="#333">1326</text>'
LAPIDE_RIP = re.sub(r'<text.*?</text>', '', LAPIDE) + '<text x="100" y="125" text-anchor="middle" font-family="Bangers" font-size="54" fill="#333">R.I.P.</text>'
MACHADO = f'<rect x="92" y="20" width="16" height="170" fill="#6b3a1e" stroke="{K}" stroke-width="5"/><path d="M108 30 Q190 40 180 110 Q140 100 108 96 Z" fill="#9aa3ad" stroke="{K}" stroke-width="6"/>'
CANE = f'<ellipse cx="100" cy="120" rx="56" ry="30" fill="#c8a26b" stroke="{K}" stroke-width="6"/><circle cx="156" cy="92" r="26" fill="#c8a26b" stroke="{K}" stroke-width="6"/><ellipse cx="146" cy="78" rx="9" ry="16" fill="#8a5a2b" stroke="{K}" stroke-width="4"/><circle cx="164" cy="88" r="4" fill="{K}"/><circle cx="180" cy="98" r="5" fill="{K}"/><path d="M60 146 L56 180 M86 148 L86 182 M116 148 L118 182 M140 144 L144 178" stroke="{K}" stroke-width="7"/><path d="M44 110 Q20 90 30 70" stroke="{K}" stroke-width="7" fill="none"/>'
GAS = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9acd32" opacity=".55"/>' for x, y, r in [(40, 140, 40), (90, 110, 50), (150, 130, 44), (110, 60, 36)])
PODIO = f'<rect x="70" y="80" width="60" height="120" fill="#f2c230" stroke="{K}" stroke-width="6"/><rect x="10" y="120" width="60" height="80" fill="#cfd5db" stroke="{K}" stroke-width="6"/><rect x="130" y="140" width="60" height="60" fill="#cd7f32" stroke="{K}" stroke-width="6"/><text x="100" y="150" text-anchor="middle" font-family="Bangers" font-size="44">1</text><text x="40" y="175" text-anchor="middle" font-family="Bangers" font-size="40">2</text><text x="160" y="185" text-anchor="middle" font-family="Bangers" font-size="36">3</text>'
FEDOR = lambda id_, x, y: "".join(f'<svg id="{id_}{k}" style="position:absolute; left:{x + k*120}px; top:{y}px; width:80px; height:300px; opacity:0" viewBox="0 0 90 320"><path d="M45 320 Q0 260 45 200 Q90 140 45 80 Q0 30 45 0" stroke="#8fd14f" stroke-width="14" fill="none" stroke-linecap="round"/></svg>' for k in range(4))
def fedor_post(id_, t):
    for k in range(4): de(f"{id_}{k}", t + k * 0.07, 0.5, "opacity: 0, y: 80", "opacity: .95, y: 0")

# personagens recorrentes
ROMANO = lambda **k: bon(roupa="nobre", cor="#f4f1ea", cabelo="curto", cc="#2b1d14", **k)
LAVANDAIO = lambda **k: bon(cor="#e8dcc0", cabelo="baguncado", cc="#2b1d14", extra=SUJEIRA, **k)
IMPERATORE = lambda **k: bon(roupa="nobre", cor="#6a1b9a", cabelo="careca", extra=LOUROS, **k)
VITTORIANA = lambda **k: bon(roupa="vestido", cor="#6b6b78", cabelo="coque", cc="#888", extra=LENCO, **k)
SIGNORE = lambda **k: bon(roupa="nobre", cor="#3b2f2f", cabelo="careca", extra=CARTOLA, **k)
TOSHER = lambda **k: bon(cor="#6b5b3a", cabelo="careca", extra=LENCO + SUJEIRA, **k)
SVUOTATORE = lambda **k: bon(cor="#5c4a32", cabelo="baguncado", cc="#3b2414", extra=SUJEIRA, **k)
CONCIATORE = lambda **k: bon(cor="#8a6a4a", cabelo="careca", extra=SUJEIRA, **k)
RE = lambda **k: bon(roupa="nobre", cor="#b71c1c", cabelo="curto", cc="#b5651d", extra=BARBA + COROA, **k)
NORRIS = lambda **k: bon(roupa="nobre", cor="#1b5e20", cabelo="curto", cc="#3b2414", **k)
REGINA = lambda **k: bon(roupa="vestido", cor="#4a148c", cabelo="longo", cc="#2b1d14", extra=COROA, **k)

# ================================================================ OBJETOS NAS PALAVRAS-CHAVE
PIPI = GOTA.replace("#d62828", "#f2d024")
ICONES = [
    (("sangue", "sanguinavano"), GOTA, "0 0 110 150"),
    (("pipì", "ammoniaca"), PIPI, "0 0 110 150"),
    (("cacca", "purezza"), CACCA, "0 0 200 200"),
    (("topi",), TOPO, "0 0 220 200"),
    (("maiali",), MAIALE, "0 0 220 200"),
    (("moneta", "monete"), MOEDA, "-12 -20 24 24"),
    (("stipendio", "denaro", "guadagnava", "pagato", "prezzo", "tassa", "euro", "pagavano", "commercio", "ricchi", "miseria", "spiccioli"), BORSA, "-34 -26 68 60"),
    (("re", "regno", "corte", "regina", "maestà", "imperatore", "reale", "reali"), COROA, "70 -40 100 70"),
    (("cuore",), CORACAO, "0 0 120 120"),
    (("candela", "mezzanotte", "notte"), CANDELA, "-40 -80 80 84"),
    (("lanterna",), LANTERNA, "-30 -40 60 70"),
    (("giustiziato", "tagliare"), MACHADO, "0 0 200 200"),
    (("gas", "odore", "puzza", "puzzava", "puzzolente"), GAS, "0 0 200 200"),
    (("secchio",), BALDE, "-30 -50 60 80"),
    (("pala",), PA, "-40 -80 80 110"),
    (("coltello",), FACA, "-20 -40 60 60"),
    (("vino", "annata"), TACA, "-24 -46 48 56"),
    (("cane",), CANE, "0 0 200 200"),
    (("scrittore", "appunti", "intervistò", "storici"), CADERNO, "-24 -36 48 54"),
    (("esaminava", "controllava", "controllare", "dimostrato"), LUPA, "-22 -44 46 54"),
    (("accusato", "accusa", "titoli", "terre"), PERGAMENA, "-28 -40 56 60"),
    (("febbre",), TERMOMETRO, "-24 -40 40 48"),
    (("annegò",), LAPIDE_RIP, "0 0 200 200"),
    (("sgabello",), SGABELLO, "0 0 200 200"),
    (("acino", "uva"), UVA, "0 0 170 200"),
    (("orologio", "ore", "anni", "mesi"), RELOGIO, "-34 -60 68 72"),
]
