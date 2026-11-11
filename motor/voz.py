# Narração rápida: edge-tts +12%. Mede os silêncios no próprio áudio (não nos tempos das palavras),
# encurta pausas internas > 0,22 s para 0,14 s, corta sobras do início/fim e junta as frases
# com 0,08 s (0,35 s antes das frases marcadas com "|"). Gera assets/voz.wav e work/tempos.json
import asyncio, json, os, re, subprocess, edge_tts
import os as _os
VOZ, RATE, MAXGAP, NOVO_GAP, GAP, GAP_PIADA = _os.environ.get('VOZ', 'it-IT-DiegoNeural'), _os.environ.get('RATE', '+10%'), 0.22, 0.14, 0.08, 0.35
def ff(*a): return subprocess.run(['ffmpeg', '-y', '-hide_banner', *a], capture_output=True, text=True)
def dur(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
def silencios(f):
    log = ff('-i', f, '-af', 'silencedetect=noise=-38dB:d=0.12', '-f', 'null', '-').stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
    fim = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    D = dur(f)
    while len(fim) < len(ini): fim.append(D)
    return list(zip(ini, fim)), D
async def main():
    import sys
    linhas = [l for l in open(sys.argv[1], encoding='utf-8').read().split('\n') if l.strip() and not l.startswith('#')]
    out, t, parts = [], 0.25, []
    for i, raw in enumerate(linhas):
        piada = raw.startswith('|'); txt = raw.lstrip('|'); words = []
        cache = f'work/voz/l{i:03d}.json'  # reaproveita a frase se o texto não mudou
        if os.path.exists(cache) and json.load(open(cache, encoding='utf-8'))['txt'] == txt:
            words = json.load(open(cache, encoding='utf-8'))['words']
        else:
            with open(f'work/voz/l{i:03d}.mp3', 'wb') as f:
                async for ch in edge_tts.Communicate(txt, VOZ, rate=RATE, boundary='WordBoundary').stream():
                    if ch['type'] == 'audio': f.write(ch['data'])
                    elif ch['type'] == 'WordBoundary': words.append([ch['text'], ch['offset']/1e7, (ch['offset']+ch['duration'])/1e7])
            json.dump({'txt': txt, 'words': words}, open(cache, 'w', encoding='utf-8'), ensure_ascii=False)
        sil, D = silencios(f'work/voz/l{i:03d}.mp3')
        # trechos de fala = complemento dos silêncios
        fala, pos = [], 0.0
        for a, b in sil:
            if a > pos: fala.append([pos, a])
            pos = b
        if pos < D: fala.append([pos, D])
        fala[0][0] = max(0, fala[0][0] - 0.03); fala[-1][1] = min(D, fala[-1][1] + 0.06)
        # junta trechos separados por pausa curta
        segs = [fala[0][:]]
        for a, b in fala[1:]:
            if a - segs[-1][1] <= MAXGAP: segs[-1][1] = b
            else: segs.append([a, b])
        if i: t += GAP_PIADA if piada else GAP
        def novo_t(x):  # tempo original -> tempo no áudio editado
            acc = 0.0
            for k, (a, b) in enumerate(segs):
                if x < a: return acc
                if x <= b: return acc + (x - a)
                acc += (b - a) + (NOVO_GAP if k < len(segs) - 1 else 0)
            return acc
        filt = [f'[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[s{k}]' for k, (a, b) in enumerate(segs)]
        filt += [f'aevalsrc=0:d={NOVO_GAP}:s=24000[z{k}]' for k in range(len(segs) - 1)]
        ordem = ''.join(f'[s{k}]' + (f'[z{k}]' if k < len(segs) - 1 else '') for k in range(len(segs)))
        r = ff('-i', f'work/voz/l{i:03d}.mp3', '-filter_complex', ';'.join(filt) + f';{ordem}concat=n={len(segs)*2-1}:v=0:a=1[o]', '-map', '[o]', '-ar', '24000', f'work/voz/c{i:03d}.wav')
        assert r.returncode == 0, r.stderr[-500:]
        L = dur(f'work/voz/c{i:03d}.wav')
        out.append({'ini': round(t, 3), 'fim': round(t + L, 3), 'texto': txt,
                    'words': [[w[0], round(t + novo_t(w[1]), 3), round(t + novo_t(w[2]), 3)] for w in words]})
        parts.append((i, t)); t += L
    # junta tudo em sequência (silêncio entre frases + frase), bom para muitas frases
    with open('work/voz/lista.txt', 'w') as f:
        pos = 0.0
        for i, s in parts:
            if s - pos > 0.001:
                ff('-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', f'{s-pos:.3f}', f'work/voz/g{i:03d}.wav'); f.write(f"file 'g{i:03d}.wav'\n")
            f.write(f"file 'c{i:03d}.wav'\n"); pos = s + dur(f'work/voz/c{i:03d}.wav')
    r = ff('-f', 'concat', '-safe', '0', '-i', 'work/voz/lista.txt', '-ar', '48000', 'assets/voz.wav')
    assert r.returncode == 0, r.stderr[-500:]
    json.dump({'linhas': out, 'total': round(t, 2)}, open('work/tempos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('total', round(t, 2))
asyncio.run(main())
