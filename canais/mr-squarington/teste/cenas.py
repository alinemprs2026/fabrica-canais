# SHORT 1 — Il lavandaio romano (vertical; Mr. Squarington narra embaixo)
exec(open('work/cenas_lib.py', encoding='utf-8').read())
SHORT = {"t1": "LAVORI SCHIFOSI DELLA STORIA", "t2": "PESTAVA LA PIPÌ", "bg": "escritorio"}
F = 130
def E(i, pref, txt, est="am", x=960, y=140, r=None): return (i, pref, txt, est, x, y, r if r is not None else random.choice([-4, -3, 3, 4]), F)
def pisa(cid, p, a, b): J(f'tl.fromTo("#{p}", {{ y: 0 }}, {{ y: -40, duration: 0.22, yoyo: true, repeat: {int((b-a)/0.22)}, ease: "power1.out", immediateRender: false }}, {a});')
FIGLIO = lambda **k: bon(roupa="nobre", cor="#2e7d32", cabelo="curto", **k)

S("a", 0, 0, "lavanderia", chars=[(LAVANDAIO(sob="nojo", boca="nojo", pose="alto"), 960, (1250, 800))], agua_y=850, agua_cor="200,170,40", corte="nenhum",
  sts=[E(0, "pestare", "PESTARE LA PIPÌ", "am"), E(0, "ore", "PER ORE", "vm", 960, 330)], fx=[("treme", 0, "pipì")],
  post=lambda c, p, a, b: pisa(c, p[0], wt(0, "pestare"), b))
S("b", 1, 1, "roma", chars=[(ROMANO(sob="convencido", boca="sorriso", pose="cintura"), x, "grupo") for x in (660, 1260)],
  sts=[E(1, "toghe", "TOGHE BIANCHE", "br"), E(1, "detersivo", "NIENTE DETERSIVO", "vm", 960, 330)])
S("c", 2, 2, "lavanderia", chars=[(LAVANDAIO(sob="surpreso", boca="o", pose="aponta"), 700, "plano")],
  sts=[E(2, "pipì", "LA PIPÌ", "am"), E(2, "ammoniaca", "AMMONIACA", "br", 1250, 330), E(2, "macchie", "VIA LE MACCHIE!", "vm", 960, 520)], fx=[("soco", 2, "pipì")])
S("d", 3, 3, "roma", chars=[(ROMANO(sob="duvida", boca="fechada", pose="cintura"), 1150, "plano")], sts=[E(3, "contribuire", "CONTRIBUIRE...", "br")],
  ex=lambda c: c.svg(desenho("vaso3", POTE.replace('translate(0 6)', 'translate(60 60) scale(2)'), 640, 760, 140, 160, "0 0 120 140"), "pers"))
S("e", 4, 5, "roma", chars=[(LAVANDAIO(sob="nojo", boca="nojo", pose="carrega", prop=POTE), 960, "plano")],
  sts=[E(4, "pieni", "PIENI", "br", 560, 160), E(4, "caldi", "CALDI", "vm", 960, 160), E(5, None, "TRABALLANTI", "am", 1360, 160)],
  post=lambda c, p, a, b: (anda(p[0], a, b), J(f'tl.fromTo("#{p[0]}", {{ rotation: -4 }}, {{ rotation: 4, duration: 0.2, yoyo: true, repeat: {int((b-a)/0.2)}, svgOrigin: "120 390", immediateRender: false }}, {a});')))
S("f", 6, 6, "lavanderia", chars=[(LAVANDAIO(sob="nojo", boca="nojo", pose="ombros"), 960, (1250, 800))], agua_y=850, agua_cor="200,170,40",
  sts=[E(6, "vasca", "NELLA VASCA", "br"), E(6, "piedi", "A PIEDI NUDI", "vm", 960, 330)], fx=[("treme", 6, "piedi")])
S("g", 7, 8, "lavanderia", chars=[(LAVANDAIO(sob="preoc", boca="aberta", pose="alto"), 960, (1250, 800))], agua_y=850, agua_cor="200,170,40",
  sts=[E(7, None, "PESTAVA", "am", 960, 140, -5), E(8, None, "TUTTO IL GIORNO", "vm", 960, 330)], post=lambda c, p, a, b: pisa(c, p[0], a, b))
S("h", 9, 9, "palacio", "dourada", [(IMPERATORE(sob="convencido", boca="sorrisao", pose="dedo"), 960, "plano")],
  sts=[E(9, "vespasiano", "VESPASIANO", "br"), E(9, "tassa", "TASSA SULLA PIPÌ", "am", 960, 330)], fx=[("treme", 9, "tassa")],
  post=lambda c, p, a, b: som("caixa.mp3", wt(9, "tassa"), 0.5))
S("i", 10, 10, "palacio", "dourada", [(IMPERATORE(sob="convencido", boca="sorrisao", pose="aponta", prop=MOEDA), 760, "plano"), (FIGLIO(sob="nojo", boca="nojo"), 1300, "plano")],
  sts=[E(10, "protestò", "FIGLIO DISGUSTATO", "br"), E(10, "puzza", "PUZZA?", "am", 960, 330, 4)], post=lambda c, p, a, b: som("moeda.mp3", wt(10, "moneta"), 0.5))
S("j", 11, 11, "palacio", "dourada", [(FIGLIO(sob="surpreso", boca="o"), 960, (1500, 1400))], sts=[E(11, None, "NO!", "vm", 960, 160, -5)], corte="seco")
S("k", 12, 12, "palacio", "dourada", [(IMPERATORE(sob="convencido", boca="sorrisao", pose="alto"), 960, "plano")], fx=[("confete", 12, "denaro")],
  ex=lambda c: c.svg(grande("den12", "IL DENARO NON PUZZA", 960, 220, 120, "#ffd60a"), "topo"),
  post=lambda c, p, a, b: (esconde("den12"), de("den12", wt(12, "denaro"), 0.35, "scale: 0, opacity: 1", "scale: 1, opacity: 1", "back.out(2.5)"), som("brilho.mp3", wt(12, "denaro"), 0.3, 2)))
S("l", 13, 13, "lavanderia", chars=[(LAVANDAIO(sob="nojo", boca="triste"), 960, "plano")], ex=lambda c: c.svg(FEDOR("fd13", 700, 420), "frente"),
  sts=[E(13, "moltissimo", "MOLTISSIMO", "vm")], post=lambda c, p, a, b: (fedor_post("fd13", wt(13, "lavandaio")), som("mosca.mp3", wt(13, "lavandaio"), 0.4, 2)))
S("m", 14, 14, "escada", "dourada", [(LAVANDAIO(sob="preoc", boca="aberta", pose="acena"), 960, "plano")],
  sts=[E(14, "seguimi", "SEGUIMI!", "am"), E(14, "peggio", "È PEGGIO", "vm", 960, 330)])
