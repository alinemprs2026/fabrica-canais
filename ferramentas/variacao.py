# MOTOR DE VARIAÇÃO (contra "conteúdo inautêntico" do YouTube)
#   briefing <canal_dir> <longo|short>  -> sorteia formato/gancho/estrutura/final sem repetir os últimos e sugere temas livres
#   similar  <canal_dir> <episodio.json> -> reprova se o roteiro/título parecer demais com algum anterior do canal
#   registra <canal_dir> <episodio.json> -> grava no histórico do canal (depois de aprovado e produzido)
import json, os, random, re, sys, datetime
FORMATOS = {
    "longo": ["ranking numerado (7 a 10 itens, do menos ao mais chocante, com reviravolta no nº1)",
              "imersão em 2ª pessoa: 'Your Life as...' — um dia inteiro, da manhã à noite, na pele da pessoa",
              "'Why It Sucked to Be...' — lista de motivos crescentes, cada um com uma cena encenada",
              "'Why You Wouldn't Survive...' — o espectador tenta sobreviver a uma série de perigos e falha",
              "mito vs verdade: 6-8 'fatos' que todo mundo acredita, desmontados um a um",
              "história de UM personagem real absurdo, em ordem cronológica, com final inesperado",
              "linha do tempo: como algo evoluiu do pior para o atual, época por época"],
    "short": ["um fato chocante explicado em 3 viradas", "pergunta no gancho respondida só no fim", "mini-ranking de 3",
              "'POV: você é...' em 45 segundos", "mito desmentido com prova", "a história real absurda de uma pessoa"],
}
GANCHOS = ["pergunta direta ao espectador", "afirmação chocante na 1ª frase", "comparação com a vida moderna (o seu emprego/casa/médico)",
           "começar no meio da ação (in medias res)", "número absurdo logo de cara", "promessa de reviravolta no final"]
FINAIS = ["piada de callback com o começo", "lição irônica para o espectador", "gancho para o próximo episódio",
          "reviravolta final + bordão", "pergunta para os comentários ligada ao tema"]
RITMOS = ["frases curtíssimas e secas", "narrador indignado", "narrador fingindo calma diante do absurdo", "narrador fazendo pausas dramáticas"]
def hist(canal):
    p = os.path.join(canal, "historico.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
def texto(ep): return " ".join(f for c in ep["cenas"] for f in c.get("falas", [])).lower()
def shingles(t, n=5):
    w = re.findall(r"[a-zà-ü']+", t.lower()); return {" ".join(w[i:i+n]) for i in range(len(w) - n + 1)}
def jacc(a, b): return len(a & b) / max(1, len(a | b))
def briefing(canal, formato):
    H = [h for h in hist(canal) if h.get("formato") == formato]
    cfg = json.load(open(os.path.join(canal, "canal.json"), encoding="utf-8"))
    rnd = random.Random(datetime.date.today().isoformat() + canal + formato)
    escolhe = lambda opcoes, chave, n: rnd.choice([o for o in opcoes if o not in [h.get(chave) for h in H[-n:]]] or opcoes)
    temas = json.load(open(cfg["banco_temas"], encoding="utf-8")) if os.path.exists(cfg.get("banco_temas", "")) else []
    usados = {h.get("tema", "").lower() for h in hist(canal)}
    livres = [t for t in temas if t["titulo"].lower() not in usados][:8]
    return {"canal": cfg["nome"], "idioma": cfg["idioma"], "formato": formato,
            "estrutura": escolhe(FORMATOS[formato], "estrutura", 3), "gancho": escolhe(GANCHOS, "gancho", 2),
            "final": escolhe(FINAIS, "final", 2), "ritmo": escolhe(RITMOS, "ritmo", 1),
            "temas_sugeridos": livres, "ultimos_titulos": [h.get("titulo") for h in hist(canal)[-15:]]}
def similar(canal, caminho):
    ep = json.load(open(caminho, encoding="utf-8")); s = shingles(texto(ep)); tw = set(re.findall(r"\w+", ep["titulo"].lower()))
    pior = (0, None)
    for h in hist(canal):
        if not os.path.exists(h.get("arquivo", "")): continue
        old = json.load(open(h["arquivo"], encoding="utf-8"))
        j = jacc(s, shingles(texto(old))); jt = jacc(tw, set(re.findall(r"\w+", old["titulo"].lower())))
        if j > pior[0]: pior = (j, old["titulo"])
        if jt > 0.6: return False, f"título parecido demais com '{old['titulo']}' ({jt:.0%})"
    if pior[0] > 0.08: return False, f"texto {pior[0]:.0%} igual a '{pior[1]}' (máx 8%)"
    return True, f"ok (maior semelhança {pior[0]:.1%})"
def registra(canal, caminho, briefing_usado=None):
    ep = json.load(open(caminho, encoding="utf-8")); H = hist(canal)
    b = briefing_usado or {}
    H.append({"data": datetime.date.today().isoformat(), "titulo": ep["titulo"], "tema": ep.get("tema", ep["titulo"]), "formato": ep["formato"],
              "estrutura": b.get("estrutura"), "gancho": b.get("gancho"), "final": b.get("final"), "ritmo": b.get("ritmo"), "arquivo": caminho})
    json.dump(H, open(os.path.join(canal, "historico.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "briefing": print(json.dumps(briefing(sys.argv[2], sys.argv[3]), ensure_ascii=False, indent=1))
    elif cmd == "similar":
        ok, msg = similar(sys.argv[2], sys.argv[3]); print("APROVADO" if ok else "REPROVADO", msg); sys.exit(0 if ok else 1)
    elif cmd == "registra":
        b = json.load(open(sys.argv[4], encoding="utf-8")) if len(sys.argv) > 4 else None; registra(sys.argv[2], sys.argv[3], b); print("registrado")
