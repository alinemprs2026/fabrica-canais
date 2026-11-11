# Mr. Squarington — gerador de episódio no estilo "gato eleito":
# contorno grosso e limpo, cores fortes, etiquetas em Bangers, legenda com palavra-chave amarela,
# zoom na palavra forte, câmera tremendo no impacto, corte "chicote" com desfoque, câmera em 3 camadas.
# Todas as marcações de tempo são presas às palavras da narração (w(frase, palavra)).
# Só o Mr. Squarington fala (boca sincronizada); os outros fazem só caras e bocas.
import json, os, random, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
sys.path.insert(0, "work")
from bonecos import *

T = json.load(open("work/tempos.json", encoding="utf-8"))  # narração do episódio
BOCA_LV = json.load(open("work/boca.json"))
LIN = T["linhas"]
W, H = 1920, 1080
DUR = round(T["total"] + 3.0, 2)
random.seed(11)

def w(i, k=0):
    """início da palavra k da frase i (k negativo conta do fim)"""
    return LIN[i]["words"][k][1]
def ini(i): return LIN[i]["ini"]
def fim(i): return LIN[i]["fim"]

cenas, js, cortes, sts, sons = [], [], [], [], []
def J(s): js.append(s)
def som(f, t, v=0.4, d=None): sons.append((f, round(t, 2), v, d))

LUZ = {
    "quente": "radial-gradient(ellipse at 30% 30%, rgba(255,190,110,.25), rgba(80,30,0,.22) 75%)",
    "noite": "linear-gradient(rgba(20,40,110,.38), rgba(5,10,40,.5))",
    "madrugada": "linear-gradient(rgba(150,190,200,.18), rgba(30,60,60,.28))",
    "esgoto": "radial-gradient(ellipse at 50% 60%, rgba(120,140,40,.12), rgba(10,20,5,.55) 80%)",
    "fria": "linear-gradient(rgba(190,220,255,.12), rgba(30,40,70,.2))",
    "dourada": "radial-gradient(ellipse at 50% 20%, rgba(255,215,120,.35), rgba(60,30,0,.3) 80%)",
    "marrom": "linear-gradient(rgba(110,70,20,.45), rgba(40,20,0,.55))",
    "neutra": "linear-gradient(rgba(0,0,0,0), rgba(0,0,0,.1))",
}
FILTRO_PERS = {"noite": "brightness(.8) saturate(.9)", "esgoto": "brightness(.78)", "marrom": "brightness(.85) sepia(.25)"}

class Cena:
    def __init__(self, cid, a, b, bg, luz="neutra", cam=(1.0, 1.08, 0, 0, 0, 0), ease="sine.inOut", corte="chicote", blur_bg=0):
        self.cid, self.ini, self.fim = cid, round(a, 3), round(b, 3)
        self.bg, self.luz, self.cam, self.ease, self.corte, self.blur_bg = bg, luz, cam, ease, corte, blur_bg
        self.pers, self.frente, self.fundo_extra, self.topo = [], [], [], []
    def personagem(self, g, x, pe, h):
        wd = h * 300 / 460; top = pe - h * 440 / 460
        self.pers.append(f'<svg class="pers" viewBox="-30 -50 300 460" style="left:{x - wd/2:.0f}px; top:{top:.0f}px; width:{wd:.0f}px; height:{h:.0f}px">{g}</svg>')
    def svg(self, html, camada="pers"):
        {"pers": self.pers, "frente": self.frente, "fundo": self.fundo_extra, "topo": self.topo}[camada].append(html)
    def fechar(self):
        c, d = self.cid, round(self.fim - self.ini + 0.05, 3)
        blur = f"filter: blur({self.blur_bg}px);" if self.blur_bg else ""
        cenas.append(f'''<div id="c-{c}" class="clip cena" data-start="{self.ini}" data-duration="{d}">
  <div id="l0-{c}" class="cam"><img class="bg" src="assets/hd/{self.bg}.jpg" style="{blur}"/>{"".join(self.fundo_extra)}</div>
  <div id="l1-{c}" class="cam" style="filter:{FILTRO_PERS.get(self.luz, "none")}">{"".join(self.pers)}</div>
  <div class="luz" style="background:{LUZ[self.luz]}"></div>
  <div id="l2-{c}" class="cam">{"".join(self.frente)}</div>
  <div id="l3-{c}" class="cam">{"".join(self.topo)}</div>
</div>''')
        z0, z1, x0, x1, y0, y1 = self.cam
        for lay, prof in (("l0", 0.45), ("l1", 1.0), ("l2", 1.6)):
            s0, s1 = 1 + (z0 - 1) * prof, 1 + (z1 - 1) * prof
            J(f'tl.fromTo("#{lay}-{c}", {{ scale: {s0:.4f}, x: {x0*prof:.1f}, y: {y0*prof:.1f} }}, {{ scale: {s1:.4f}, x: {x1*prof:.1f}, y: {y1*prof:.1f}, duration: {d}, ease: "{self.ease}" }}, {self.ini});')
        if self.ini > 0 and self.corte == "chicote":
            J(f'tl.fromTo("#c-{c}", {{ scale: 1.14, filter: "blur(18px)" }}, {{ scale: 1, filter: "blur(0px)", duration: 0.26, ease: "power3.out" }}, {self.ini});')
            cortes.append(self.ini); som("whoosh-short.mp3", self.ini - 0.08, 0.3)
        return self

# ---------------------------------------------------------------- animação
def boca(p, t0, t1):
    ant = None
    for f in range(int(t0 * 30), int(t1 * 30), 2):
        lv = max(BOCA_LV[f:f+2]) if f < len(BOCA_LV) else 0
        if lv != ant:
            J(f'tl.set("#{p}-boca", {{ attr: {{ d: "{BOCA[FALA[lv]]}" }} }}, {f/30:.3f});'); ant = lv
    J(f'tl.set("#{p}-boca", {{ attr: {{ d: "{BOCA["fechada"]}" }} }}, {t1:.3f});')

def expr(p, t, sob=None, bo=None, olho=None):
    if sob: J(f'tl.set("#{p}-sob", {{ attr: {{ d: "{SOB[sob]}" }} }}, {t:.2f});')
    if bo: J(f'tl.set("#{p}-boca", {{ attr: {{ d: "{BOCA[bo]}" }} }}, {t:.2f});')
    if olho is not None: J(f'tl.to("#{p}-pup", {{ x: {olho[0]}, y: {olho[1]}, duration: 0.07 }}, {t:.2f});')

def piscar(p, ts):
    for t in ts: J(f'tl.fromTo("#{p}-pal", {{ attr: {{ height: 0 }} }}, {{ attr: {{ height: 38 }}, duration: 0.05, yoyo: true, repeat: 1, immediateRender: false }}, {t:.2f});')

def vida(p, t0, t1, sobs=("normal",), bocas=None):
    """caras e bocas: olhos, sobrancelhas e (para quem não fala) boca trocando a cada 0,25–0,6 s"""
    t = t0 + 0.15
    while t < t1 - 0.15:
        if len(sobs) > 1 and random.random() < .6: expr(p, t, sob=random.choice(sobs))
        if bocas and random.random() < .7: expr(p, t, bo=random.choice(bocas))
        t += random.uniform(0.25, 0.6)
    t = t0 + random.uniform(0.4, 1.2)
    while t < t1 - 0.3:
        piscar(p, [t]); t += random.uniform(1.8, 3.2)
    expr(p, t0, olho=(0, 0)); t = t0 + random.uniform(1.5, 3.0)
    while t < t1 - 0.8:
        expr(p, t, olho=(random.choice([-5, 5]), random.choice([0, 2]))); expr(p, t + random.uniform(0.35, 0.6), olho=(0, 0))
        t += random.uniform(2.5, 4.5)

def pose(p, t, nome, dur=0.16, prop=True):
    (e1, e2), (d1, d2) = POSE[nome]
    dE, hE = braco("E", e1, e2); dD, hD = braco("D", d1, d2)
    for parte, val in ((f"{p}-bE", f'd: "{dE}"'), (f"{p}-bD", f'd: "{dD}"'), (f"{p}-mE", f"cx: {hE[0]}, cy: {hE[1]}"), (f"{p}-mD", f"cx: {hD[0]}, cy: {hD[1]}")):
        J(f'tl.to("#{parte}", {{ attr: {{ {val} }}, duration: {dur}, ease: "back.out(1.8)" }}, {t:.2f});')
    if prop: J(f'tl.to("#{p}-prop", {{ attr: {{ transform: "translate({hD[0]} {hD[1]})" }}, duration: {dur}, ease: "back.out(1.8)" }}, {t:.2f});')

def balanca(p, t0, t1, amp=3, per=0.4):
    J(f'tl.fromTo("#{p}-cab", {{ rotation: -{amp} }}, {{ rotation: {amp}, duration: {per}, yoyo: true, repeat: {max(1, int((t1-t0)/per))}, ease: "sine.inOut", svgOrigin: "120 118", immediateRender: false }}, {t0:.2f});')

def mostra(sel, t, op=1, dur=0.1): J(f'tl.to("#{sel}", {{ opacity: {op}, duration: {dur} }}, {t:.2f});')
def esconde(*sels): J(f'tl.set("{",".join("#"+s for s in sels)}", {{ opacity: 0 }}, 0);')

def anda(p, t0, t1, passo=0.2):
    n = int((t1 - t0) / passo)
    J(f'tl.fromTo("#{p}-pE", {{ attr: {{ d: "M102 266 Q96 330 84 386" }} }}, {{ attr: {{ d: "M102 266 Q108 330 116 386" }}, duration: {passo}, yoyo: true, repeat: {n}, ease: "sine.inOut", immediateRender: false }}, {t0:.2f});')
    J(f'tl.fromTo("#{p}-pD", {{ attr: {{ d: "M138 266 Q144 330 156 386" }} }}, {{ attr: {{ d: "M138 266 Q132 330 124 386" }}, duration: {passo}, yoyo: true, repeat: {n}, ease: "sine.inOut", immediateRender: false }}, {t0:.2f});')

def de(sel, t, dur, a, b, ease="power2.out"):
    J(f'tl.fromTo("#{sel}", {{ {a} }}, {{ {b}, duration: {dur}, ease: "{ease}", immediateRender: false }}, {t:.2f});')

def soco(cid, t, esc=1.1):
    """zoom rápido na palavra forte (na camada dos personagens)"""
    J(f'tl.fromTo("#l1-{cid}", {{ scale: "+=0" }}, {{ scale: "+={esc-1:.2f}", duration: 0.12, ease: "power2.out", immediateRender: false }}, {t:.2f});')

def treme(cid, t, forca=16, n=7):
    for k in range(n): J(f'tl.set("#c-{cid}", {{ x: {random.randint(-forca, forca)}, y: {random.randint(-forca, forca)} }}, {t + k*0.035:.3f});')
    J(f'tl.set("#c-{cid}", {{ x: 0, y: 0 }}, {t + n*0.035:.3f});')

def st(i, a, b, txt, est="am", x=960, y=150, r=-3, fs=110):
    sts.append((i, round(a, 2), round(b, 2), txt, est, x, y, r, fs)); som("pop.mp3", a, 0.35)

# ---------------------------------------------------------------- elementos de cena
def borrao(x, y, wd, h, cor="#1a120c", forma="ellipse", op=0.85, blur=22):
    if forma == "ellipse": el = f'<ellipse cx="{wd/2}" cy="{h/2}" rx="{wd/2}" ry="{h/2}" fill="{cor}"/>'
    elif forma == "junco": el = "".join(f'<path d="M{wd*k/7:.0f} {h} Q{wd*k/7+random.randint(-30,30):.0f} {h/2} {wd*k/7+random.randint(-40,40):.0f} {random.randint(0, int(h/3))}" stroke="{cor}" stroke-width="{random.randint(10,22)}" fill="none" stroke-linecap="round"/>' for k in range(8))
    elif forma == "abajur": el = f'<path d="M{wd*.2} {h*.35} L{wd*.8} {h*.35} L{wd*.65} 0 L{wd*.35} 0 Z" fill="#f0c070"/><rect x="{wd*.46}" y="{h*.35}" width="{wd*.08}" height="{h*.6}" fill="{cor}"/>'
    else: el = f'<rect width="{wd}" height="{h}" fill="{cor}"/>'
    return f'<svg style="position:absolute; left:{x}px; top:{y}px; width:{wd}px; height:{h}px; overflow:visible; opacity:{op}; filter:blur({blur}px)" viewBox="0 0 {wd} {h}">{el}</svg>'

def particulas(cid, n, t0, t1, cor="255,230,180"):
    out = []
    for k in range(n):
        x, y, r = random.randint(0, W), random.randint(0, H), random.randint(2, 6)
        out.append(f'<div id="po-{cid}-{k}" style="position:absolute; left:{x}px; top:{y}px; width:{r*2}px; height:{r*2}px; border-radius:50%; background:rgba({cor},.55); filter:blur(1.5px)"></div>')
        J(f'tl.fromTo("#po-{cid}-{k}", {{ x: 0, y: 0 }}, {{ x: {random.randint(-80, 80)}, y: {random.randint(-120, 40)}, duration: {t1-t0+0.1:.2f}, ease: "none" }}, {t0:.2f});')
    return "".join(out)

def chuva(cid, n, t0, t1):
    out = []
    for k in range(n):
        x, y0, v = random.randint(-200, W), random.randint(-1200, 0), random.uniform(1700, 2400)
        out.append(f'<div id="ch-{cid}-{k}" style="position:absolute; left:{x}px; top:0; width:4px; height:{random.randint(40,90)}px; background:rgba(200,220,255,.6); rotate:12deg"></div>')
        J(f'tl.fromTo("#ch-{cid}-{k}", {{ y: {y0}, x: 0 }}, {{ y: {y0 + v*(t1-t0+0.1):.0f}, x: {-0.21*v*(t1-t0+0.1):.0f}, duration: {t1-t0+0.1:.2f}, ease: "none" }}, {t0:.2f});')
    return "".join(out)

def confete(cid, t, n=40):
    out = []
    for k in range(n):
        out.append(f'<div id="cf-{cid}-{k}" style="position:absolute; left:{random.randint(20, 1900)}px; top:-60px; width:24px; height:36px; border:4px solid #111; background:{random.choice(["#ffd60a", "#e63946", "#2c6fbb", "#2e7d32", "#fff"])}"></div>')
        J(f'tl.fromTo("#cf-{cid}-{k}", {{ y: {random.randint(-400, 0)}, rotation: 0 }}, {{ y: {random.randint(1150, 1500)}, rotation: {random.randint(-720, 720)}, duration: {random.uniform(1.2, 1.7):.2f}, ease: "power1.in", immediateRender: false }}, {t + random.uniform(0, 0.25):.2f});')
    return "".join(out)

def agua(cid, topo, cor="54,84,52", op=0.8):
    return f'<div style="position:absolute; left:-300px; right:-300px; top:{topo}px; bottom:-400px; background:linear-gradient(rgba({cor},{op-0.2}), rgba({cor},{op}) 30%); border-top:6px solid rgba(230,250,230,.7)"></div>'

def grande(id_, html, x, y, tam=150, cor="#fff"):
    return f'<div id="{id_}" style="position:absolute; left:{x}px; top:{y}px; width:0; height:0"><div style="position:absolute; translate:-50% -50%; white-space:nowrap; font-family:Bangers; font-size:{tam}px; letter-spacing:.03em; color:{cor}; -webkit-text-stroke:{max(8, tam//9)}px #111; paint-order:stroke fill; text-shadow:0 10px 0 #111">{html}</div></div>'

def desenho(id_, svg_inner, x, y, wd, h, vb="0 0 200 200"):
    return f'<svg id="{id_}" style="position:absolute; left:{x}px; top:{y}px; width:{wd}px; height:{h}px; overflow:visible" viewBox="{vb}">{svg_inner}</svg>'

GOTA = '<path d="M55 6 Q100 80 90 110 Q80 144 55 144 Q30 144 20 110 Q10 80 55 6 Z" fill="#d62828" stroke="#111" stroke-width="8"/>'
UVA = "".join(f'<circle cx="{x}" cy="{y}" r="24" fill="#6a2c91" stroke="#111" stroke-width="6"/>' for x, y in [(45,60),(85,60),(125,60),(65,100),(105,100),(85,140)]) + '<path d="M85 36 Q90 10 110 6" stroke="#2e7d32" stroke-width="9" fill="none"/>'
CORACAO = '<path d="M60 108 L14 60 Q-6 30 20 12 Q44 0 60 26 Q76 0 100 12 Q126 30 106 60 Z" fill="#e63946" stroke="#111" stroke-width="7"/><path d="M60 26 L52 50 L66 64 L54 90" stroke="#111" stroke-width="6" fill="none"/>'
BALAO_CEL = '<rect x="0" y="0" width="560" height="110" rx="26" fill="#25d366" stroke="#111" stroke-width="7"/><path d="M60 108 L40 150 L100 108" fill="#25d366" stroke="#111" stroke-width="7"/>'


# ---------------------------------------------------------------- ATUAÇÃO (linguagem corporal automática)
INFO = []   # uma entrada por cena: tempos, onde estão os personagens, se tem o Mr., índice do html
GESTOS_FALA = ["dedo", "aponta", "ombros", "desculpa", "cintura", "dedo", "baixo", "alto", "ombros", "aponta"]
REACAO = {"nojo": ["chora", "desculpa", "ombros"], "preoc": ["chora", "desculpa", "segura"], "triste": ["chora", "segura"],
          "bravo": ["aponta", "cintura", "alto"], "surpreso": ["alto", "chora"], "duvida": ["ombros", "cintura"]}
def _batidas(r, t0, t1, g0, g1):
    """momentos de movimento presos ao início das palavras (ou espaçados, se ninguém fala)"""
    ws = [x[1] for l in LIN for x in l["words"] if t0 + 0.25 <= x[1] <= t1 - 0.4]
    out, nxt = [], t0 + r.uniform(0.2, 0.5)
    for t in ws:
        if t >= nxt: out.append(t); nxt = t + r.uniform(g0, g1)
    if not ws:
        t = nxt
        while t < t1 - 0.4: out.append(t); t += r.uniform(g0, g1)
    return out
def pulo(A, t, h=24):
    J(f'tl.fromTo("{A}", {{ y: 0 }}, {{ y: -{h}, duration: 0.13, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }}, {t:.2f});')
    J(f'tl.fromTo("{A}", {{ scaleY: 1, scaleX: 1 }}, {{ scaleY: 0.88, scaleX: 1.08, svgOrigin: "120 390", duration: 0.07, yoyo: true, repeat: 1, immediateRender: false }}, {t + 0.26:.2f});')
def tremido(r, A, t, d=0.3, f=5):
    n = int(d / 0.035)
    for k in range(n): J(f'tl.set("{A}", {{ x: {r.randint(-f, f)} }}, {t + k * 0.035:.3f});')
    J(f'tl.set("{A}", {{ x: 0 }}, {t + n * 0.035:.3f});')
def recua(r, A, t, rot, lado):
    J(f'tl.fromTo("{A}", {{ x: 0, rotation: {rot:.1f} }}, {{ x: {-28 * lado}, rotation: {-9 * lado}, svgOrigin: "120 390", duration: 0.16, ease: "power3.out", immediateRender: false }}, {t:.2f});')
    tremido(r, A, t + 0.18, 0.25, 4)
    J(f'tl.fromTo("{A}", {{ x: {-28 * lado}, rotation: {-9 * lado} }}, {{ x: 0, rotation: {rot:.1f}, svgOrigin: "120 390", duration: 0.3, ease: "power2.inOut", immediateRender: false }}, {t + 0.5:.2f});')
def atuar(pid, t0, t1, fala=False, sob="normal", bracos=True, cabeca=True, base="baixo", lado=1):
    r = random.Random(pid); A = f"#{pid}-act"; O = 'svgOrigin: "120 390"'
    if t1 - t0 < 0.5: return
    n = max(1, int((t1 - t0) / 0.5))   # respiração / balanço do corpo
    J(f'tl.fromTo("{A}", {{ scaleY: 1, scaleX: 1 }}, {{ scaleY: 1.03, scaleX: 0.985, {O}, duration: 0.5, yoyo: true, repeat: {n}, ease: "sine.inOut", immediateRender: false }}, {t0:.2f});')
    rot, cab, k = 0.0, 0.0, 0
    for t in (_batidas(r, t0, t1, 0.6, 1.1) if fala else _batidas(r, t0, t1, 0.75, 1.5)):
        k += 1
        if fala:  # apresentador: corpo e cabeça acompanham a fala, braços gesticulam
            nr = r.choice([-1, 1]) * r.uniform(2, 5) if rot == 0 else -rot * r.uniform(0.6, 1.2)
            J(f'tl.fromTo("{A}", {{ rotation: {rot:.1f} }}, {{ rotation: {nr:.1f}, {O}, duration: 0.28, ease: "back.out(2.2)", immediateRender: false }}, {t:.2f});'); rot = nr
            if cabeca:
                nc = r.choice([-1, 1]) * r.uniform(3, 8)
                J(f'tl.fromTo("#{pid}-cab", {{ rotation: {cab:.1f} }}, {{ rotation: {nc:.1f}, svgOrigin: "120 118", duration: 0.22, ease: "back.out(2.5)", immediateRender: false }}, {t + 0.05:.2f});'); cab = nc
            if bracos and k % 2 == 1:
                pose(pid, t, r.choice([x for x in GESTOS_FALA if not (x == "aponta" and lado < 0)]), 0.18)
            if k % 5 == 0: pulo(A, t + 0.1, 18)
        else:     # quem só reage: caras e bocas com o corpo inteiro
            e = r.random()
            if sob == "nojo" and e < 0.5: recua(r, A, t, rot, lado)
            elif sob in ("preoc", "triste") and e < 0.5: tremido(r, A, t, 0.35, 5)
            elif sob == "bravo" and e < 0.5: pulo(A, t, 26); tremido(r, A, t + 0.3, 0.2, 6)
            elif e < 0.35: pulo(A, t, r.choice([18, 26, 34]))
            else:
                nr = r.choice([-1, 1]) * r.uniform(3, 8)
                J(f'tl.fromTo("{A}", {{ rotation: {rot:.1f} }}, {{ rotation: {nr:.1f}, {O}, duration: 0.3, ease: "back.out(2.4)", immediateRender: false }}, {t:.2f});'); rot = nr
            if cabeca and r.random() < 0.6:
                nc = r.choice([-1, 1]) * r.uniform(4, 10)
                J(f'tl.fromTo("#{pid}-cab", {{ rotation: {cab:.1f} }}, {{ rotation: {nc:.1f}, svgOrigin: "120 118", duration: 0.2, ease: "back.out(3)", immediateRender: false }}, {t + 0.12:.2f});'); cab = nc
            if bracos and k % 2 == 0 and t + 0.95 < t1:
                pose(pid, t + 0.05, r.choice(REACAO.get(sob, ["ombros", "acena", "alto", "cintura"])), 0.18)
                pose(pid, t + 0.8, base, 0.22)

# ================================================================ CENAS (arquivo do episódio)
exec(open(sys.argv[1], encoding='utf-8').read())


# ---------------------------------------------------------------- PASSES GLOBAIS
def bate(a, b, m=0): return not (a[2] + m <= b[0] or b[2] + m <= a[0] or a[3] + m <= b[1] or b[3] + m <= a[1])
def stbox(txt, x, y, fs): wd = len(txt) * fs * 0.47 + 90; return (x - wd / 2, y, x + wd / 2, y + fs + 34)
def cena_em(t): return next((sc for sc in INFO if sc["a"] <= t < sc["b"]), None)

SH = globals().get("SHORT")
XMIN, XMAX = (200, 1720) if SH else (30, 1890)   # área visível do palco (no short as bordas são cortadas)
# A) Mr. Squarington aparece no canto das cenas em que ele não está (reage e fala)
nc = 0
for sc in INFO:
    if SH or sc["mr"] or not sc["cameo"] or sc["b"] - sc["a"] < 2.0: continue
    nc += 1
    if nc % 3 == 0: continue
    hh = 760; wd = hh * 300 / 460; pe = 1250
    for x in ([235, 1685] if nc % 2 else [1685, 235]):
        box = (x - wd * 0.36, 540, x + wd * 0.36, 1080)
        if not any(bate(box, o, -30) for o in sc["occ"]): break
    else: continue
    pid, rr = f"cm{sc['cid']}", random.Random(sc["cid"])
    t0, t1 = sc["a"] + 0.15, sc["b"]
    sob = rr.choice(["nojo", "duvida", "convencido", "surpreso", "nojo", "preoc"])
    lado = 1 if x < 960 else -1
    g = mr_square(pid, pose=rr.choice(["aponta", "dedo", "cintura"] if lado > 0 else ["dedo", "cintura", "ombros"]), sob=sob)
    cenas.append(f'<div id="{pid}c" class="clip" data-start="{sc["a"]}" data-duration="{round(sc["b"] - sc["a"], 3)}" style="position:absolute; inset:0; overflow:hidden; z-index:16">'
                 f'<div id="{pid}-in" style="position:absolute; inset:0"><svg class="pers" viewBox="-30 -50 300 460" style="position:absolute; overflow:visible; left:{x - wd/2:.0f}px; top:{pe - hh*440/460:.0f}px; width:{wd:.0f}px; height:{hh}px">'
                 f'<g id="{pid}-act">{g}</g></svg></div></div>')
    de(f"{pid}-in", t0, 0.32, f"y: 520, rotation: {-8 * lado}", "y: 0, rotation: 0", "back.out(1.7)"); som("whoosh-short.mp3", t0, 0.22)
    if t1 - t0 > 1.2: J(f'tl.to("#{pid}-in", {{ y: 560, duration: 0.2, ease: "power2.in" }}, {t1 - 0.22:.2f});')
    boca(pid, t0, t1); vida(pid, t0, t1, (sob, "normal"))
    atuar(pid, t0 + 0.35, t1 - 0.25, fala=True, sob=sob, lado=lado)
    sc["occ"].append(box); sc["cabs"].append((x - wd * 0.2, pe - hh * 440 / 460 + hh * 0.04 + 0, x + wd * 0.2, pe - hh * 440 / 460 + hh * 0.39))

# B) etiquetas nunca uma em cima da outra: muda de lugar ou encerra a anterior
def cabecas(a_, b_):
    out = []
    for sc in INFO:
        if sc["a"] < b_ and sc["b"] > a_:
            z = sc.get("zoom", 1.0) * 1.08
            for (x0, y0, x1, y1) in sc.get("cabs", []):
                out.append((960 + (x0 - 960) * z, 540 + (y0 - 540) * z, 960 + (x1 - 960) * z, 540 + (y1 - 540) * z))
    return out
sts.sort(key=lambda s_: s_[1]); fila = []
for s_ in sts:
    i_, a_, b_, txt, est, x, y, r_, fs = s_
    CB = cabecas(a_, b_)
    def colide(xx, yy, f_=None):
        bb = stbox(txt, xx, yy, f_ or fs)
        return [o for o in fila if o[2] > a_ + 0.05 and bate(bb, stbox(o[3], o[5], o[6], o[8]), 22)]
    def rosto(xx, yy, f_=None): return any(bate(stbox(txt, xx, yy, f_ or fs), c_, 10) for c_ in CB)
    if colide(x, y) or rosto(x, y):
        cands = sorted([(x, y + d) for d in (190, 380, -190)] + [(xx, yy) for xx in (420, 520, 960, 1400, 1500) for yy in (140, 330, 520, 680)],
                       key=lambda p_: abs(p_[0] - x) + abs(p_[1] - y))
        achou = False
        for f_ in (fs, int(fs * 0.8), int(fs * 0.65)):
            for xx, yy in cands:
                bb = stbox(txt, xx, yy, f_)
                if bb[0] < XMIN or bb[2] > XMAX or yy < 40 or bb[3] > 860: continue
                if not colide(xx, yy, f_) and not rosto(xx, yy, f_): x, y, fs, achou = xx, yy, f_, True; break
            if achou: break
        if not achou:
            for o in colide(x, y): o[2] = max(o[1] + 0.2, a_ - 0.02)
    bb = stbox(txt, x, y, fs)  # não deixa sair da tela
    if bb[0] < XMIN: x += XMIN - bb[0]
    if bb[2] > XMAX: x -= bb[2] - XMAX
    fila.append([i_, a_, b_, txt, est, x, y, r_, fs])
sts[:] = [tuple(o) for o in fila]

# C) objetos que surgem nas palavras-chave (ICONES vem do arquivo do episódio)
ICON_SLOTS = [(330, 330), (1590, 330), (330, 590), (1590, 590), (600, 360), (1320, 360)] if SH else [(250, 330), (1670, 330), (250, 590), (1670, 590), (560, 360), (1360, 360)]
usados, ultimo, ni = {}, {}, 0
for li, l in enumerate(LIN):
    for wd_ in l["words"]:
        pal = wd_[0].lower().strip(".,!?:;…'\"«»")
        for k_, (chaves, svg_, vb_) in enumerate(globals().get("ICONES", [])):
            if not any(pal == c_ or (c_.endswith("*") and pal.startswith(c_[:-1])) for c_ in chaves): continue
            t = wd_[1]; sc = cena_em(t)
            if not sc or sc["b"] - t < 0.8 or t - ultimo.get(k_, -99) < 6: continue
            if usados.get(sc["cid"], 0) >= 2 or svg_[:80] in cenas[sc["idx"]]: continue
            ativos = [stbox(o[3], o[5], o[6], o[8]) for o in sts if o[1] < sc["b"] and o[2] > t]
            for (x, y) in ICON_SLOTS:
                box = (x - 105, y - 105, x + 105, y + 105)
                if not any(bate(box, o, 10) for o in sc["occ"] + ativos + sc.get("ic", [])): break
            else: continue
            sc.setdefault("ic", []).append(box); usados[sc["cid"]] = usados.get(sc["cid"], 0) + 1; ultimo[k_] = t; ni += 1
            iid = f"ic{ni}"
            cenas.append(f'<div id="{iid}c" class="clip" data-start="{t:.3f}" data-duration="{sc["b"] - t:.3f}" style="position:absolute; left:{x}px; top:{y}px; width:0; height:0; z-index:15">'
                         f'<svg id="{iid}" viewBox="{vb_}" style="position:absolute; left:-95px; top:-95px; width:190px; height:190px; overflow:visible">{svg_}</svg></div>')
            J(f'tl.fromTo("#{iid}", {{ scale: 0, rotation: -25 }}, {{ scale: 1, rotation: 0, duration: 0.3, ease: "back.out(3)", immediateRender: false }}, {t:.2f});')
            J(f'tl.fromTo("#{iid}", {{ rotation: -6, y: 0 }}, {{ rotation: 6, y: -10, duration: 0.45, yoyo: true, repeat: {max(1, int((sc["b"] - t) / 0.45))}, ease: "sine.inOut", immediateRender: false }}, {t + 0.3:.2f});')
            som("pop.mp3", t, 0.3)
            break
print("apresentador no canto:", sum(1 for c_ in cenas if c_.startswith('<div id="cm')), "objetos:", ni)

# ---------------------------------------------------------------- etiquetas, flash, grão
for (i, a, b, txt, est, x, y, r, fs) in sts:
    cenas.append(f'<div id="{i}" class="clip adw" data-start="{a}" data-duration="{round(b-a,2)}" style="left:{x}px; top:{y}px">'
                 f'<div class="ad {est}" id="{i}-in" style="--r:{r}deg; --fs:{fs}px">{txt}</div></div>')
    J(f'tl.fromTo("#{i}-in", {{ scale: 0, rotation: {r-14} }}, {{ scale: 1, rotation: {r}, duration: 0.28, ease: "back.out(2.6)" }}, {a});')
J('tl.set("#flash", { opacity: 0 }, 0);')
for c0 in cortes: J(f'tl.fromTo("#flash", {{ opacity: 0.3 }}, {{ opacity: 0, duration: 0.14, immediateRender: false }}, {c0});')
J(f'tl.fromTo("#grao", {{ x: 0, y: 0 }}, {{ x: 40, y: -30, duration: 0.1, repeat: {int(DUR/0.1)}, ease: "steps(1)", yoyo: true }}, 0);')

GRAO = "data:image/svg+xml;utf8," + "<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 .9 0'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>"
CSS = f"""
@font-face {{ font-family: "Bangers"; src: url("assets/fonts/Bangers-Regular.ttf"); }}
#root {{ position: absolute; inset: 0; overflow: hidden; background: #000; }}
.cena {{ position: absolute; inset: 0; overflow: hidden; }}
.cam {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
.bg {{ position: absolute; left: -192px; top: -75px; width: 2304px; height: 1231px; object-fit: cover; filter: saturate(1.15) contrast(1.05); }}
.pers {{ position: absolute; overflow: visible; }}
.luz {{ position: absolute; inset: 0; pointer-events: none; mix-blend-mode: multiply; }}
.cx {{ position: absolute; width: 150px; height: 110px; background: #b5834a; border: 6px solid #111; font-family: Bangers; font-size: 28px; text-align: center; padding-top: 22px; color: #111; line-height: 1; }}
.adw {{ position: absolute; width: 0; height: 0; z-index: 20; }}
.ad {{ position: absolute; left: 0; top: 0; translate: -50% 0; white-space: nowrap; font-family: "Bangers", sans-serif; line-height: 1;
  letter-spacing: .03em; padding: 10px 36px 2px; border: 7px solid #111; border-radius: 20px; box-shadow: 10px 10px 0 #111; rotate: var(--r); font-size: var(--fs); }}
.am {{ background: #ffd60a; color: #111; }} .br {{ background: #fff; color: #111; }}
.vm {{ background: #e63946; color: #fff; -webkit-text-stroke: 3px #111; }} .pt {{ background: #111; color: #ffd60a; }}
#flash {{ position: absolute; inset: 0; z-index: 38; background: #fff; opacity: 0; pointer-events: none; }}
#vinheta {{ position: absolute; inset: 0; z-index: 40; pointer-events: none; background: radial-gradient(ellipse at 50% 50%, transparent 58%, rgba(0,0,0,.4) 100%); }}
#grao {{ position: absolute; inset: -60px; z-index: 41; pointer-events: none; opacity: .06; background-image: url("{GRAO}"); mix-blend-mode: overlay; }}
"""
corpo = "\n".join(cenas) + (f'<div id="flash" class="clip" data-start="0" data-duration="{DUR}"></div>'
                            f'<div id="vinheta" class="clip" data-start="0" data-duration="{DUR}"></div><div id="grao" class="clip" data-start="0" data-duration="{DUR}"></div>')

def comp(cid, corpo, css, js_, fundo="#000", w=W, h=H):
    return f'''<template>
  <style>{css} #root {{ background: {fundo}; }}</style>
  <div id="root" data-composition-id="{cid}" data-width="{w}" data-height="{h}">
    {corpo}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {js_}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''
os.makedirs("compositions", exist_ok=True)
open("compositions/video.html", "w", encoding="utf-8").write(comp("video", corpo, CSS, "\n".join(js)))

# ---------------------------------------------------------------- legenda (estilo gato): Bangers, palavra a palavra, chaves em amarelo
CHAVE = {"pior", "emprego", "domingo", "onze", "fofo", "inveja", "esgoto", "fossa", "xixi", "nojento", "pegadinha", "disputados", "desculpas",
         "trabalhar", "sete", "sanguessugas", "sanguessuga", "sangue", "febre", "cabeça", "coração", "adivinha", "uva", "frança", "milhões",
         "madrugada", "gelado", "isca", "você", "uma", "cinco", "vinte", "italiano", "pobres", "feridas", "miséria", "fresco", "feder"}
words = [x for l in LIN for x in l["words"]]
grupos, k = [], 0
while k < len(words):  # 1–2 palavras por vez: palavra curta gruda na seguinte
    g = [words[k]]
    if len(words[k][0].strip(".,!?")) <= 3 and k + 1 < len(words) and words[k+1][1] - words[k][2] < 0.25:
        g.append(words[k+1]); k += 1
    grupos.append(g); k += 1
lh = []
for n, g in enumerate(grupos):
    a = g[0][1]; e = min(grupos[n+1][0][1], g[-1][2] + 0.4) if n + 1 < len(grupos) else g[-1][2] + 0.6
    lh.append(f'<div id="lg{n}" class="clip lg" data-start="{a}" data-duration="{round(e-a,2)}"><span>{" ".join(x[0] for x in g).strip(".")}</span></div>')
LEG_TOP, LEG_FS, LW, LH_ = (1222, 64, 1080, 1920) if SH else (900, 52, W, H)
open("compositions/legendas.html", "w", encoding="utf-8").write(comp("legendas", "".join(lh), """
@font-face { font-family: "Mont"; src: url("assets/fonts/Montserrat.ttf"); font-weight: 100 900; }
#root { position: absolute; inset: 0; pointer-events: none; }
.lg { position: absolute; left: 0; right: 0; top: LEG_TOPpx; text-align: center; }
.lg span { display: inline-block; font-family: "Mont", sans-serif; font-weight: 800; font-size: LEG_FSpx; color: #fff;
  -webkit-text-stroke: 6px #111; paint-order: stroke fill; text-shadow: 0 3px 6px rgba(0,0,0,.5); }""".replace("LEG_TOP", str(LEG_TOP)).replace("LEG_FS", str(LEG_FS)), "", fundo="transparent", w=LW, h=LH_))


# ---------------------------------------------------------------- SHORT: moldura (título em cima, Mr. Squarington narrando embaixo)
if SH:
    BAND_TOP, ESC = 470, 0.68
    BAND_H = round(1080 * ESC); BAND_X = round((1080 - 1920 * ESC) / 2)
    js_ep, js = js, []
    pid = "apr"; hh, pe, x = 1000, 2240, 540; wd = hh * 300 / 460
    fim_fala = LIN[-1]["fim"]
    g = mr_square(pid, pose="dedo", sob="convencido")
    boca(pid, 0, fim_fala); vida(pid, 0.2, DUR, ("convencido", "normal", "nojo", "surpreso", "duvida"))
    atuar(pid, 0.3, fim_fala, fala=True, sob="convencido")
    t, k = fim_fala + 0.15, 0
    while t < DUR - 0.3:
        pose(pid, t, "acena" if k % 2 == 0 else "acena2", 0.16); t += 0.22; k += 1
    expr(pid, fim_fala + 0.1, sob="convencido", bo="sorrisao")
    J('tl.fromTo("#tt1", { scale: 1.15 }, { scale: 1, duration: 0.35, ease: "back.out(2)" }, 0);')
    J('tl.fromTo("#tt2", { scale: 1.3 }, { scale: 1, duration: 0.4, ease: "back.out(2.5)" }, 0);')
    J(f'tl.fromTo("#tt2", {{ rotation: -2 }}, {{ rotation: 2, duration: 0.6, yoyo: true, repeat: {int(DUR / 0.6)}, ease: "sine.inOut", immediateRender: false }}, 0.6);')
    J(f'tl.fromTo("#apr-in", {{ y: 90 }}, {{ y: 0, duration: 0.35, ease: "back.out(2)" }}, 0);')
    t1 = SH.get("t1", ""); t2 = SH.get("t2", "")
    corpo_m = f"""
<img src="assets/hd/{SH.get('bg', 'escritorio')}.jpg" style="position:absolute; left:-700px; top:{BAND_TOP + BAND_H - 40}px; width:2400px; height:{1920 - BAND_TOP - BAND_H + 80}px; object-fit:cover; filter: blur(6px) brightness(.75)"/>
<div style="position:absolute; left:0; top:0; width:1080px; height:{BAND_TOP}px; background: repeating-linear-gradient(-45deg, #173a75 0 40px, #1f4e9c 40px 80px); border-bottom: 10px solid #111"></div>
<div style="position:absolute; left:0; top:{BAND_TOP + BAND_H}px; width:1080px; height:10px; background:#111"></div>
<div style="position:absolute; left:0; right:0; top:44px; text-align:center; font-family:Bangers; font-size:46px; letter-spacing:.12em; color:#fff; opacity:.85">MR. SQUARINGTON</div>
<div id="tt1" style="position:absolute; left:0; right:0; top:120px; text-align:center; font-family:Bangers; font-size:78px; color:#fff; -webkit-text-stroke:9px #111; paint-order:stroke fill; text-shadow:0 7px 0 #111">{t1}</div>
<div style="position:absolute; left:0; right:0; top:230px; text-align:center"><div id="tt2" style="display:inline-block; font-family:Bangers; font-size:{SH.get('fs2', 104)}px; line-height:1.02; color:#111; background:#ffd60a; padding:10px 34px 2px; border:8px solid #111; border-radius:22px; box-shadow:10px 10px 0 #111">{t2}</div></div>
<div id="apr-in" style="position:absolute; inset:0"><svg class="pers" viewBox="-30 -50 300 460" style="position:absolute; overflow:visible; left:{x - wd/2:.0f}px; top:{pe - hh*440/460:.0f}px; width:{wd:.0f}px; height:{hh}px"><g id="apr-act">{g}</g></svg></div>
"""
    css_m = '@font-face { font-family: "Bangers"; src: url("assets/fonts/Bangers-Regular.ttf"); } #root { position:absolute; inset:0; overflow:hidden; } .pers { position:absolute; overflow:visible; }'
    open("compositions/moldura.html", "w", encoding="utf-8").write(comp("moldura", corpo_m, css_m, "\n".join(js), fundo="#111", w=1080, h=1920))
    js = js_ep

# ---------------------------------------------------------------- áudio
def dur_arq(f):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "assets/" + f], capture_output=True, text=True).stdout) - 0.02, 2)
audio, ocup = [], {}
for n, (f, s, v, d) in enumerate(sorted(sons, key=lambda x: x[1])):
    s = max(0, s); d = min(d, dur_arq(f)) if d else dur_arq(f)
    fx = next(k for k in range(20, 90) if ocup.get(k, -1) <= s)
    ocup[fx] = s + d + 0.01
    audio.append(f'<audio id="a{n}" class="clip" src="assets/{f}" data-start="{s}" data-duration="{d}" data-track-index="{fx}" data-volume="{v}"></audio>')
IW, IH = (1080, 1920) if SH else (W, H)
if SH:
    VIDEO_HOST = (f'<div id="moldura" data-composition-id="moldura" data-composition-src="compositions/moldura.html" data-start="0" data-duration="{DUR}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:0"></div>'
                  f'<div id="faixa" style="position:absolute; left:0; top:{BAND_TOP}px; width:1080px; height:{BAND_H}px; overflow:hidden; z-index:1">'
                  f'<div id="video" data-composition-id="video" data-composition-src="compositions/video.html" data-start="0" data-duration="{DUR}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="position:absolute; left:{BAND_X}px; top:0; width:{W}px; height:{H}px; transform:scale({ESC}); transform-origin:0 0"></div></div>')
else:
    VIDEO_HOST = f'<div id="video" data-composition-id="video" data-composition-src="compositions/video.html" data-start="0" data-duration="{DUR}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:1"></div>'
index = f'''<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={IW}, height={IH}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {IW}px; height: {IH}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{IW}" data-height="{IH}">
      {VIDEO_HOST}
      <div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html" data-start="0" data-duration="{DUR}" data-track-index="2" data-track-kind="captions" data-width="{IW}" data-height="{IH}" style="z-index:2"></div>
      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-duration="{dur_arq('voz.wav')}" data-track-index="12" data-volume="1"></audio>
      <audio id="trilha" class="clip" src="assets/trilha.wav" data-start="0" data-duration="{DUR}" data-track-index="13" data-volume="0.2"></audio>
      {chr(10).join("      " + a for a in audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
open("index.html", "w", encoding="utf-8").write(index)
print("ok", DUR, "cenas:", len(cenas) - len(sts), "cortes chicote:", len(cortes), "etiquetas:", len(sts))
