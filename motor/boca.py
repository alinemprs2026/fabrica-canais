# Boca sincronizada: volume da voz (assets/voz.wav) a cada 1/30 s -> nível 0..4 (work/boca.json)
import json, subprocess, numpy as np
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'assets/voz.wav', '-ac', '1', '-ar', '24000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
n = len(x) // 800
db = 20 * np.log10(np.sqrt((x[:n*800].reshape(n, 800) ** 2).mean(1)) + 1e-9)
voz = db > -40
q1, q2, q3 = np.percentile(db[voz], [18, 51, 95])
lv = np.where(~voz, 0, np.where(db < q1, 1, np.where(db < q2, 2, np.where(db < q3, 3, 4))))
json.dump([int(v) for v in lv], open('work/boca.json', 'w'))
print(len(lv), np.bincount(lv))
