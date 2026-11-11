# Estudo dos virais dos campeões em inglês: todos os vídeos longos de cada canal, quanto cada um ficou acima da mediana do canal.
import subprocess, statistics, json, concurrent.futures as cf
acervo = json.load(open("D:/CANAIS DARK/fabrica-canais/acervo/concorrentes.json", encoding="utf-8"))["canais"]
canais = [c for c in acervo if c["idioma"] == "EN" and c["papel"].startswith("referencia")]
def yd(args):
    return subprocess.run(["uvx", "yt-dlp", "--no-warnings", *args], capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout
def todos(c):
    vids = []
    for l in yd(["--flat-playlist", "--print", "%(view_count)s|%(duration)s|%(id)s|%(title)s", c["url"] + "/videos"]).splitlines():
        p = l.split("|", 3)
        if len(p) == 4 and p[0].isdigit() and float(p[1] or 0) >= 120: vids.append({"views": int(p[0]), "min": round(float(p[1]) / 60, 1), "id": p[2], "titulo": p[3]})
    return c, vids
base = []
with cf.ThreadPoolExecutor(6) as ex:
    for c, vids in ex.map(todos, canais):
        if not vids: print("sem dados:", c["canal"]); continue
        med = statistics.median(v["views"] for v in vids)
        for i, v in enumerate(vids):
            v.update(canal=c["canal"], mediana_canal=med, fator=round(v["views"] / med, 2), recencia=i)
        base += vids
        print(f'{c["canal"]:22} {len(vids):4} vídeos longos | mediana {med/1e3:8.0f}k')
json.dump(base, open("virais_en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nTOP 60 VIRAIS (vezes acima da mediana do próprio canal):")
for v in sorted(base, key=lambda v: v["fator"], reverse=True)[:60]:
    print(f'{v["fator"]:5.1f}x {v["views"]/1e6:6.2f}M {v["min"]:5}min  {v["canal"][:16]:16}  {v["titulo"][:90]}')
