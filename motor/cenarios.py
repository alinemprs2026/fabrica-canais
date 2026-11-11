# Gera os cenários novos pedidos no episodio.json (Pollinations, grátis) e prepara em alta (assets/hd/<id>.jpg).
# Fila respeitando o limite grátis (1 imagem a cada ~45 s), com novas tentativas.
import json, os, subprocess, sys, time, urllib.parse, urllib.request
EP = json.load(open("work/episodio.json", encoding="utf-8"))
ESTILO = ", 2D cartoon background illustration, flat colors, clean lines, no people, no text, wide establishing shot, vibrant, detailed"
pedidos = [(k, v) for k, v in EP.get("cenarios", {}).items() if not os.path.exists(f"assets/hd/{k}.jpg")]
print(len(pedidos), "cenários novos")
for n, (nome, prompt) in enumerate(pedidos):
    url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt + ESTILO) + f"?width=1024&height=576&nologo=true&seed={abs(hash(nome)) % 99999}"
    for tent in range(6):
        try:
            dado = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "fabrica-canais"}), timeout=180).read()
            if len(dado) > 20000:
                open(f"work/{nome}_raw.jpg", "wb").write(dado); break
        except Exception as e:
            print("  tentativa", tent + 1, nome, e)
        time.sleep(50)
    else:
        print("  FALHOU", nome, "(vai usar cenário padrão)"); continue
    # corta a marca d'água de baixo e aumenta para 2304 px com nitidez
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"work/{nome}_raw.jpg", "-vf",
                    "crop=iw:ih*0.94:0:0,scale=2304:1231:flags=lanczos,unsharp=5:5:0.8", "-q:v", "3", f"assets/hd/{nome}.jpg"], check=True)
    print("  ok", nome)
    if n < len(pedidos) - 1: time.sleep(47)
