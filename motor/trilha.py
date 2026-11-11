# Trilha "curiosa" de pizzicato + fagote leve, em Ré menor, 108 bpm. Gera assets/trilha.wav
import numpy as np, wave
SR = 44100; BPM = 108; B = 60 / BPM; DUR = 580
t_total = np.zeros(int(SR * DUR))
def nota(f, ini, dur, amp=0.3, tipo="pizz"):
    n = int(SR * dur); t = np.arange(n) / SR
    if tipo == "pizz":
        env = np.exp(-t * 9)
        s = np.sin(2*np.pi*f*t) + 0.45*np.sin(2*np.pi*2*f*t)*np.exp(-t*14) + 0.2*np.sin(2*np.pi*3*f*t)*np.exp(-t*20)
    elif tipo == "baixo":
        env = np.exp(-t * 5)
        s = np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2*f*t)
    else:  # fagote: sopro suave
        env = np.minimum(1, t / 0.04) * np.exp(-t * 1.6)
        s = sum(np.sin(2*np.pi*k*f*t) / k**1.3 for k in range(1, 6)) * (1 + 0.004*np.sin(2*np.pi*5*t))
    i = int(SR * ini); j = min(len(t_total), i + n)
    t_total[i:j] += (amp * env * s)[: j - i]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
# progressão Dm - Bb - Gm - A (4 compassos de 4 tempos)
acordes = [(50, [62, 65, 69]), (46, [62, 65, 70]), (43, [62, 67, 70]), (45, [61, 64, 69])]
melodia = [74, None, 72, 74, 77, None, 76, 74, 72, None, 70, 72, 69, None, None, None,
           74, None, 76, 77, 79, None, 77, 76, 74, None, 73, None, 69, None, 73, None]
c = 0; t = 0.0
while t < DUR - 2:
    raiz, tri = acordes[c % 4]
    for b in range(4):
        tb = t + b * B
        nota(hz(raiz - 12 if b % 2 == 0 else raiz - 5), tb, 0.6, 0.38, "baixo")
        if b in (1, 3):
            for k, m in enumerate(tri): nota(hz(m), tb + k * 0.012, 0.35, 0.09)
        for h in range(2):  # colcheias da melodia
            m = melodia[((c * 8) + b * 2 + h) % len(melodia)]
            if m and (c // 4) % 2 == 1: nota(hz(m - 12), tb + h * B / 2, 0.5, 0.12, "fagote")
            elif m: nota(hz(m), tb + h * B / 2, 0.3, 0.13)
    c += 1; t += 4 * B
t_total /= np.max(np.abs(t_total)) * 1.25
fade = int(SR * 2); t_total[-fade:] *= np.linspace(1, 0, fade)
pcm = (t_total * 32767).astype(np.int16)
w = wave.open('assets/trilha.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('ok')
