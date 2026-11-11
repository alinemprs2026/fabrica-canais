# THUMB AUTOMÁTICA a partir de work/episodio.json -> "thumb": {"estilo": "B"|"C", "texto": [l1, l2], "objeto": <desenho>,
#   "alvo": <personagem opcional, só B>, "vomito": bool (B), "verde": bool, "cor": "#hex" (fundo do C)}
# B = fundo branco + texto preto + seta vermelha + Mr. Squarington com nojo fazendo a ação (estilo da campeã de 2,9 mi)
# C = rosto gigante do Mr. Squarington em choque + objeto + fundo de cor chapada com raios (estilo mascote em close)
# Uso (dentro do projeto do episódio): python work/thumb.py <saida.png>
import json, os, re, shutil, subprocess, sys
sys.path.insert(0, "work")
from bonecos import *
lib = open("work/cenas_lib.py", encoding="utf-8").read()
for nome in ("CACCA", "CACCA_BRANCA", "TOPO", "MAIALE", "SGABELLO", "LAPIDE", "LAPIDE_RIP", "MACHADO", "CANE", "GAS", "PODIO", "COROA", "BARBA", "LOUROS", "TACA", "K"):
    m = re.search(rf"^{nome} = .*$", lib, re.M)
    if m: exec(m.group(0))
mot = open("work/motor.py", encoding="utf-8").read()
for nome in ("GOTA", "UVA", "CORACAO"):
    exec(re.search(rf"^{nome} = .*$", mot, re.M).group(0))
PIPI = GOTA.replace("#d62828", "#f2d024")
DES = {"CACCA": (CACCA, "0 0 200 200"), "CACCA_BRANCA": (CACCA_BRANCA, "0 0 200 200"), "TOPO": (TOPO, "0 0 220 200"), "MAIALE": (MAIALE, "0 0 220 200"),
       "SGABELLO": (SGABELLO, "0 0 200 200"), "LAPIDE": (LAPIDE_RIP, "0 0 200 200"), "MACHADO": (MACHADO, "0 0 200 200"), "CANE": (CANE, "0 0 200 200"),
       "GAS": (GAS, "0 0 200 200"), "PODIO": (PODIO, "0 0 200 200"), "GOTA": (GOTA, "0 0 110 150"), "PIPI": (PIPI, "0 0 110 150"), "UVA": (UVA, "0 0 170 200"),
       "CORACAO": (CORACAO, "0 0 120 120"), "COROA": (COROA, "70 -40 100 70"), "TACA": (TACA, "-24 -46 48 56"), "RELOGIO": (RELOGIO, "-34 -66 68 76"),
       "BORSA": ('<path d="M-18 -10 Q-26 24 0 26 Q26 24 18 -10 Z" fill="#c9a26b" stroke="#111" stroke-width="4"/><path d="M-10 -12 L10 -12" stroke="#111" stroke-width="5"/>', "-34 -26 68 60")}
PRESET = {"RE": dict(roupa="nobre", cor="#b71c1c", cabelo="curto", cor_cabelo="#b5651d", extra_cabeca=BARBA + COROA),
          "REGINA": dict(roupa="vestido", cor="#4a148c", cabelo="longo", cor_cabelo="#2b1d14", extra_cabeca=COROA),
          "IMPERATORE": dict(roupa="nobre", cor="#6a1b9a", cabelo="careca", extra_cabeca=LOUROS),
          "ROMANO": dict(roupa="nobre", cor="#f4f1ea", cabelo="curto", cor_cabelo="#2b1d14"),
          "SIGNORE": dict(roupa="nobre", cor="#3b2f2f", cabelo="careca", extra_cabeca=CARTOLA)}
ep = json.load(open("work/episodio.json", encoding="utf-8")); T = ep.get("thumb", {})
estilo = T.get("estilo", "C"); txt = [str(x).upper() for x in (T.get("texto") or [ep["titulo"]])][:2]
obj = DES.get(T.get("objeto"), DES["GOTA"])

def pers(g, x, pe, h, extra=""):
    wd = h * 300 / 460; top = pe - h * 440 / 460
    return f'<svg viewBox="-30 -50 300 460" style="position:absolute; overflow:visible; left:{x - wd/2:.0f}px; top:{top:.0f}px; width:{wd:.0f}px; height:{h}px;{extra}">{g}</svg>'
OLHOS = '<circle cx="102" cy="64" r="16" fill="#fff" stroke="#111" stroke-width="5"/><circle cx="140" cy="64" r="16" fill="#fff" stroke="#111" stroke-width="5"/>'
def verde(g): return g.replace('rx="9" fill="#fde3c8"', 'rx="9" fill="#bfe08f"', 1)
def boca_custom(g, p, novo): return re.sub(rf'<path id="{p}-boca" d="[^"]*"[^>]*/>', novo, g)
def suor(g, p): return g.replace(f'id="{p}-suor" d="M174 26 Q184 44 174 52 Q164 44 174 26 Z" fill="#8fd3ff" stroke="#111" stroke-width="2.5" opacity="0"',
                                 f'id="{p}-suor" d="M174 26 Q184 44 174 52 Q164 44 174 26 Z" fill="#8fd3ff" stroke="#111" stroke-width="2.5" opacity="1"')
FEDOR = lambda xs: "".join(f'<path d="M{x} 300 Q{x-40} 240 {x} 180 Q{x+40} 120 {x} 60 Q{x-30} 20 {x} -10" stroke="#111" stroke-width="34" fill="none" stroke-linecap="round"/><path d="M{x} 300 Q{x-40} 240 {x} 180 Q{x+40} 120 {x} 60 Q{x-30} 20 {x} -10" stroke="#7cc242" stroke-width="20" fill="none" stroke-linecap="round"/>' for x in xs)
MOSCA = lambda x, y, s=1: f'<g transform="translate({x} {y}) scale({s})"><ellipse rx="14" ry="10" fill="#111"/><ellipse cx="-9" cy="-13" rx="11" ry="8" fill="#e8f1fb" stroke="#111" stroke-width="3"/><ellipse cx="9" cy="-13" rx="11" ry="8" fill="#e8f1fb" stroke="#111" stroke-width="3"/></g>'
def tam_txt(t, larg, base):  # fonte que cabe na largura
    return int(min(base, larg / max(1, len(t)) / 0.47))
TOPO_HTML = '''<!doctype html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>@font-face { font-family: "Bangers"; src: url("assets/fonts/Bangers-Regular.ttf"); }
* { margin:0; padding:0; box-sizing:border-box; } html, body { width:1920px; height:1080px; overflow:hidden; }
#root { position:relative; width:1920px; height:1080px; overflow:hidden; } .t { position:absolute; font-family:Bangers; line-height:.88; paint-order:stroke fill; white-space:nowrap; }</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="1920" data-height="1080">'''
FIM = '</div><script>window.__timelines = { main: gsap.timeline({ paused: true }) };</script></body></html>'

if estilo == "B":
    POSE["limpa"] = ((14, 8), (78, 50))
    PANO = '<g transform="rotate(10) scale(2.6)"><path d="M-14 -14 Q0 -20 16 -12 L18 16 Q2 22 -16 16 Z" fill="#fff" stroke="#111" stroke-width="3"/><path d="M-8 2 Q-2 -6 6 0 Q12 8 2 10 Q-8 12 -8 2 Z" fill="#7a4a22"/></g>'
    mb = suor(boneco("mb", roupa="terno", cabelo="topete", cor_cabelo="#2b1d14", pose="limpa", sob="nojo", mecha=True, pernas=False, prop=PANO), "mb")
    if T.get("verde", True): mb = verde(mb)
    mb = mb.replace(OLHOS + '\n    <g id="mb-pup"><circle cx="104" cy="66" r="6" fill="#111"/><circle cx="142" cy="66" r="6" fill="#111"/></g>',
                    '<path d="M88 54 L112 64 L88 74 M154 54 L130 64 L154 74" stroke="#111" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/><g id="mb-pup"></g>')
    vom = T.get("vomito", True)
    mb = boca_custom(mb, "mb", ('<circle cx="86" cy="96" r="15" fill="#9acd32" stroke="#111" stroke-width="4"/><circle cx="156" cy="96" r="15" fill="#9acd32" stroke="#111" stroke-width="4"/>' if vom else "")
                     + '<ellipse cx="121" cy="100" rx="22" ry="16" fill="#3a1010" stroke="#111" stroke-width="4"/><ellipse cx="121" cy="103" rx="17" ry="11" fill="' + ("#9acd32" if vom else "#ff6f91") + '"/>')
    VOM = ('<svg viewBox="0 0 460 560" style="position:absolute; left:400px; top:690px; width:460px; height:560px; overflow:visible"><g stroke-linejoin="round">'
           '<path d="M370 -4 Q394 -2 398 16 Q392 110 330 200 Q300 250 310 300 Q270 300 250 350 Q230 400 260 430 Q200 450 150 420 Q100 470 40 440 Q-10 470 -60 430 Q-40 380 0 370 Q-20 320 30 300 Q20 250 80 230 Q90 170 160 150 Q200 90 280 60 Q330 30 370 -4 Z" fill="#9acd32" stroke="#111" stroke-width="12"/>'
           '<path d="M360 14 Q300 70 240 120 Q170 180 120 260" stroke="#c6e86a" stroke-width="26" fill="none" stroke-linecap="round"/></g>'
           + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9acd32" stroke="#111" stroke-width="7"/>' for x, y, r in ((-60, 230, 26), (-110, 340, 20), (10, 150, 18), (120, 60, 22), (60, -20, 12)))
           + '</svg>') if vom else ""
    alvo = T.get("alvo")
    if alvo:
        kw = dict(PRESET.get(alvo.get("p"), dict(roupa=alvo.get("roupa", "nobre"), cor=alvo.get("cor", "#b71c1c"), cabelo=alvo.get("cabelo", "curto"), cor_cabelo=alvo.get("cc", "#3b2414"))))
        direita = pers(boneco("rb", pose=alvo.get("pose", "cintura"), sob=alvo.get("sob", "convencido"), boca=alvo.get("boca", "sorrisao"), pernas=False, **kw), 1320, 1150, 1000)
        direita += f'<svg viewBox="{obj[1]}" style="position:absolute; left:1100px; top:700px; width:440px; height:440px; overflow:visible">{obj[0]}</svg>'
    else:
        direita = f'<svg viewBox="{obj[1]}" style="position:absolute; left:1080px; top:330px; width:640px; height:640px; overflow:visible">{obj[0]}</svg>'
    fs = min(tam_txt(t, 1000, 190) for t in txt)
    html = TOPO_HTML + f'''<div style="position:absolute; inset:0; background:#fff"></div>
<svg viewBox="0 0 360 320" style="position:absolute; left:1100px; top:150px; width:420px; height:380px; overflow:visible">{FEDOR((60, 180, 300))}</svg>
{direita}
{pers(mb, 780, 1420, 1150)}{VOM}
<svg viewBox="0 0 600 200" style="position:absolute; left:1200px; top:40px; width:600px; height:200px; overflow:visible">{MOSCA(60, 90, 1.6)}{MOSCA(330, 40, 1.3)}{MOSCA(520, 140, 1.5)}</svg>
''' + "".join(f'<div class="t" style="left:70px; top:{50 + k * (fs + 10)}px; font-size:{fs}px; color:#111">{t}</div>' for k, t in enumerate(txt)) + f'''
<svg viewBox="0 0 360 340" style="position:absolute; left:120px; top:{80 + len(txt) * (fs + 10)}px; width:360px; height:340px; overflow:visible">
<path d="M30 30 Q60 230 300 260" stroke="#e63946" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M262 205 L340 266 L250 310 Z" fill="#e63946" stroke="#e63946" stroke-width="10" stroke-linejoin="round"/></svg>''' + FIM
else:
    mc = suor(mr_square("mc", pose="chora", sob="surpreso"), "mc")
    if T.get("verde", True): mc = verde(mc)
    mc = mc.replace(OLHOS, '<circle cx="100" cy="62" r="22" fill="#fff" stroke="#111" stroke-width="5"/><circle cx="142" cy="62" r="22" fill="#fff" stroke="#111" stroke-width="5"/>')
    mc = mc.replace('<circle cx="104" cy="66" r="6" fill="#111"/><circle cx="142" cy="66" r="6" fill="#111"/>', '<circle cx="94" cy="66" r="4" fill="#111"/><circle cx="136" cy="66" r="4" fill="#111"/>')
    mc = boca_custom(mc, "mc", '<path d="M98 116 Q100 86 121 86 Q142 86 144 116 Q121 106 98 116 Z" fill="#3a1010" stroke="#111" stroke-width="3.5" stroke-linejoin="round"/>')
    fs = min(tam_txt(t, 820, 180) for t in txt)
    cores = ["#fff", "#e63946"]
    html = TOPO_HTML + f'''<div style="position:absolute; inset:0; background:{T.get("cor", "#ffd60a")}"></div>
<div style="position:absolute; inset:-400px; background:repeating-conic-gradient(from 0deg at 50% 50%, rgba(255,255,255,.35) 0 8deg, transparent 8deg 22deg); translate:420px 120px"></div>
{pers(mc, 1390, 2875, 3300)}
<svg viewBox="0 0 360 320" style="position:absolute; left:230px; top:250px; width:460px; height:380px; overflow:visible">{FEDOR((20, 190, 360))}</svg>
<svg viewBox="{obj[1]}" style="position:absolute; left:150px; top:500px; width:620px; height:620px; overflow:visible">{obj[0]}</svg>
<svg viewBox="0 0 600 260" style="position:absolute; left:140px; top:330px; width:600px; height:260px; overflow:visible">{MOSCA(60, 120, 1.7)}{MOSCA(500, 60, 1.4)}</svg>
''' + "".join(f'<div class="t" style="left:60px; top:{40 + k * (fs + 0)}px; font-size:{fs}px; color:{cores[k % 2]}; -webkit-text-stroke:{max(10, fs // 8)}px #111; text-shadow:0 12px 0 #111; rotate:-3deg">{t}</div>' for k, t in enumerate(txt)) + FIM

os.makedirs("work/thumb/assets", exist_ok=True)
if not os.path.exists("work/thumb/assets/fonts"): shutil.copytree("assets/fonts", "work/thumb/assets/fonts")
for f in ("package.json", "hyperframes.json", "meta.json"):
    if os.path.exists(f): shutil.copy(f, "work/thumb/")
open("work/thumb/index.html", "w", encoding="utf-8").write(html)
subprocess.run("npx --yes hyperframes@0.9.28 snapshot -o snap --at 0.5 --no-end --timeout 120000", shell=True, cwd="work/thumb", capture_output=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "work/thumb/snap/frame-00-at-0.5s.png", "-vf", "scale=1280:720:flags=lanczos", sys.argv[1]], check=True)
print("thumb ok:", sys.argv[1])
