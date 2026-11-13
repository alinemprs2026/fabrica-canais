# Diretor: desenhos de saúde, apresentador(a) próprio(a) com boca sincronizada, e chaves para desligar o Mr. Squarington no canto
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "motor"))
p = "cenas_auto.py"; s = open(p, encoding="utf-8").read()
def t(a, b):
    global s
    assert a in s, a[:70]; s = s.replace(a, b, 1)
t("SOBS, BOCAS, POSES = set(SOB), set(BOCA), set(POSE)",
  """exec(open('work/desenhos_saude.py', encoding='utf-8').read())
DESENHOS.update(SAUDE); globals().update(PROPS_SAUDE); SVG_NOMES += list(PROPS_SAUDE)
SOBS, BOCAS, POSES = set(SOB), set(BOCA), set(POSE)""")
t('''    if p == "mr": return mr(pose, sob, prop, boca)''',
  '''    if p == "mr": return mr(pose, sob, prop, boca)
    if p == "host":   # apresentador(a) do canal: fala com a boca sincronizada (como o Mr. Squarington)
        extra = "".join(globals()[e] for e in c.get("extra", []) if e in EXTRA_NOMES)
        kw = dict(roupa=ok(c.get("roupa"), {"camisa", "terno", "vestido", "jaleco", "nobre"}, "camisa"), cor=c.get("cor", "#3a9a8a"),
                  cabelo=ok(c.get("cabelo"), set(CABELO), "longo"), cor_cabelo=c.get("cc", "#3b2414"), extra_cabeca=extra)
        return Pers(lambda pid: boneco(pid, pose=pose, sob=sob, boca=boca, prop=prop, **kw), mr=True, sobs=(sob, "normal"), pose=pose, prop=prop)''')
t('''      fala=sc.get("fala", True))''', '''      fala=sc.get("fala", True), cameo=EP.get("cameo", True))''')
s += '''
# canal sem os objetos automáticos de história (ex.: saúde)
if EP.get("icones_auto") is False:
    ICONES = []
'''
open(p, "w", encoding="utf-8").write(s); print("ok")
