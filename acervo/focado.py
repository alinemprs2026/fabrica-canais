# Medição focada dos concorrentes diretos + caça de canais do nicho em IT/ES/PT por títulos típicos
import subprocess, statistics, json, concurrent.futures as cf, collections, datetime
def yd(args):
    return subprocess.run(["uvx", "yt-dlp", "--no-warnings", *args], capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout
CONHECIDOS = ["Chat History", "Lost Legacy", "Dumb Doggo", "Sam O'Nella Academy", "Barely Evolved", "Primordia", "Bernard", "Simple History",
              "Colossal Cranium", "Academia Play", "CuriosaMente", "Good Enough Animation", "The Infographics Show", "Sideprojects"]
CACA = ["por qué apestaba ser animado", "peores trabajos de la historia animación", "la vida de un esclavo romano animado", "historia de la humanidad animada graciosa",
        "perché faceva schifo essere", "i peggiori lavori della storia", "la vita nel medioevo animazione", "storia dell'umanità animata",
        "por que era horrível ser", "os piores empregos da história", "como era a vida na idade média desenho", "história da humanidade animada"]
def acha_canal(nome):
    for l in yd(["--flat-playlist", "--print", "%(channel)s|%(channel_url)s", f"ytsearch10:{nome} animated"]).splitlines():
        c, _, u = l.partition("|")
        if c.strip().lower() == nome.lower() and u.startswith("http"): return nome, u
    return nome, None
def caca(q):
    return [l.split("|", 3) for l in yd(["--flat-playlist", "--print", "%(channel)s|%(channel_url)s|%(view_count)s|%(title)s", f"ytsearch15:{q}"]).splitlines()]
alvos = {}
with cf.ThreadPoolExecutor(8) as ex:
    for nome, u in ex.map(acha_canal, CONHECIDOS):
        if u: alvos[u] = ("conhecido", nome)
    vistos = collections.Counter(); info = {}
    for res in ex.map(caca, CACA):
        for p in res:
            if len(p) == 4 and p[1].startswith("http"): vistos[p[1]] += 1; info[p[1]] = p[0]
    for u, n in vistos.most_common(25):
        alvos.setdefault(u, ("caça", info[u]))
def mede(item):
    url, (tipo, nome) = item
    vids = []
    for l in yd(["--flat-playlist", "--playlist-items", "1-20", "--print", "%(view_count)s|%(duration)s|%(title)s", url + "/videos"]).splitlines():
        p = l.split("|", 2)
        if len(p) == 3 and p[0].isdigit(): vids.append((int(p[0]), p[1], p[2]))
    meta = yd(["--skip-download", "--playlist-items", "1", "--print", "%(channel_follower_count)s|%(upload_date)s", url + "/videos"]).strip().split("|")
    m20 = yd(["--skip-download", "--playlist-items", str(max(1, len(vids))), "--print", "%(upload_date)s", url + "/videos"]).strip()
    return tipo, nome, url, vids, meta, m20
out = []
with cf.ThreadPoolExecutor(8) as ex:
    for tipo, nome, url, vids, meta, m20 in ex.map(mede, alvos.items()):
        if not vids: continue
        v = [x[0] for x in vids]
        try:
            dias = (datetime.date.fromisoformat(f"{meta[1][:4]}-{meta[1][4:6]}-{meta[1][6:]}") - datetime.date.fromisoformat(f"{m20[:4]}-{m20[4:6]}-{m20[6:]}")).days
            ritmo = round(len(v) / max(1, dias) * 30, 1)
        except Exception: ritmo = None
        out.append({"tipo": tipo, "canal": nome, "url": url, "inscritos": meta[0] if meta else "?", "ultimo": meta[1] if len(meta) > 1 else "?",
                    "mediana": statistics.median(v), "ritmo_mes": ritmo, "dur_min": round(statistics.median([float(x[1] or 0) for x in vids]) / 60, 1),
                    "top": [f"{x[0]/1e6:.2f}M {x[2][:80]}" for x in sorted(vids, reverse=True)[:3]]})
json.dump(out, open("focado.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(out))
