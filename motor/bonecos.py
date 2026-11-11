# Personagens no formato do desenho dela: cabeça quadrada cor de pele, olhos grandes, corpo retangular,
# braços e pernas de linha fina, mãos redondas pequenas, traço feito à mão (filtro #rabisco).
# viewBox 0 0 240 400 · pés em y=390 · ombros em (76,128) e (164,128)
import math
K = "#111"
PELE = "#fde3c8"

SOB = {  # sobrancelhas
    "normal": "M90 42 L112 40 M130 40 L152 42",
    "bravo": "M90 36 L112 46 M130 46 L152 36",
    "preoc": "M90 46 L112 36 M130 36 L152 46",
    "surpreso": "M90 32 L112 28 M130 28 L152 32",
    "duvida": "M90 42 L112 42 M130 32 L152 38",
    "nojo": "M90 38 L112 46 M130 40 L152 34",
    "convencido": "M90 40 L112 42 M130 36 L152 34",
    "triste": "M90 48 L112 38 M130 38 L152 48",
}

def boca_d(w, top, bot, cy=96):
    """Boca sempre com os mesmos comandos (para trocar/animar). top/bot = deslocamento das curvas."""
    return f"M{121-w} {cy} Q121 {cy+top} {121+w} {cy} Q121 {cy+bot} {121-w} {cy} Z"

BOCA = {
    "fechada": boca_d(9, 1, 2),
    "sorriso": boca_d(14, 2, 13),
    "sorrisao": boca_d(17, -2, 20),
    "o": boca_d(7, -11, 11),
    "aberta": boca_d(12, -7, 14),
    "triste": boca_d(11, -9, -5),
    "nojo": boca_d(12, 4, -3),
    "fala1": boca_d(9, -1, 5), "fala2": boca_d(10, -3, 9), "fala3": boca_d(11, -5, 12), "fala4": boca_d(12, -7, 15),
}
FALA = ["fechada", "fala1", "fala2", "fala3", "fala4"]

CABELO = {
    "curto": "M64 32 Q66 2 100 6 Q122 -6 146 6 Q178 6 178 36 Q170 22 152 24 Q140 14 120 20 Q100 12 86 24 Q72 22 64 42 Z",
    "baguncado": "M60 36 Q58 8 84 6 Q90 -8 110 2 Q124 -10 140 2 Q160 -6 168 10 Q186 14 180 42 Q172 26 154 26 Q146 18 126 22 Q106 14 90 26 Q74 24 60 42 Z",
    "topete": "M62 36 Q58 6 92 2 Q112 -24 156 -10 Q186 -2 180 38 Q172 22 150 22 Q128 10 104 20 Q84 16 72 30 Z",
    "longo": "M58 44 Q54 0 120 2 Q186 0 182 44 L186 150 Q176 160 168 140 L168 42 Q150 24 120 24 Q90 24 72 42 L72 140 Q64 160 54 150 Z",
    "coque": "M64 36 Q64 6 120 6 Q176 6 176 36 Q160 22 120 22 Q80 22 64 36 Z M104 8 Q100 -22 120 -24 Q140 -22 136 8 Z",
    "careca": "",
}

def braco(lado, a1, a2, L1=62, L2=58):
    """lado 'E' (esquerda da tela) ou 'D'. Ângulos em graus a partir de 'para baixo'; positivo = para fora."""
    sx, sy = (76, 128) if lado == "E" else (164, 128)
    d = -1 if lado == "E" else 1
    ex = sx + L1 * math.sin(math.radians(a1)) * d; ey = sy + L1 * math.cos(math.radians(a1))
    hx = ex + L2 * math.sin(math.radians(a2)) * d; hy = ey + L2 * math.cos(math.radians(a2))
    return f"M{sx} {sy} Q{ex:.1f} {ey:.1f} {hx:.1f} {hy:.1f}", (round(hx, 1), round(hy, 1))

POSE = {  # (ângulos braço E), (ângulos braço D)
    "baixo": ((14, 8), (14, 8)),
    "cintura": ((40, -50), (40, -50)),
    "cha": ((14, 8), (22, -110)),          # mão direita na frente do peito (xícara)
    "bebe": ((14, 8), (30, -160)),         # leva a xícara à boca
    "dedo": ((14, 8), (40, 175)),          # indicador para cima, ao lado do rosto
    "aponta": ((14, 8), (95, 92)),         # aponta para o lado
    "alto": ((150, 170), (150, 170)),      # braços para cima (comemorar / desespero)
    "ombros": ((60, 120), (60, 120)),      # "sei lá"
    "desculpa": ((30, -95), (30, -95)),    # mãos juntas no peito
    "relogio": ((14, 8), (25, -120)),      # segura o relógio na frente
    "segura": ((30, -70), (30, -70)),      # segura algo na frente da barriga
    "carrega": ((70, 40), (70, 40)),       # carrega dois baldes/potes
    "acena": ((14, 8), (140, 175)),
    "chora": ((40, -150), (40, -150)),     # mãos no rosto
}

def roupa_svg(tipo, cor):
    if tipo == "terno":
        return (f'<rect x="72" y="116" width="96" height="152" rx="6" fill="#1f4e9c" stroke="{K}" stroke-width="6"/>'
                f'<path d="M100 117 L120 160 L140 117 Z" fill="#fff" stroke="{K}" stroke-width="3" stroke-linejoin="round"/>'
                f'<path d="M115 119 L125 119 L129 152 L120 172 L111 152 Z" fill="{K}"/>'
                f'<path d="M100 117 L114 176 M140 117 L126 176" stroke="{K}" stroke-width="3" fill="none"/>'
                f'<circle cx="120" cy="200" r="3.5" fill="{K}"/><circle cx="120" cy="226" r="3.5" fill="{K}"/>'
                # relógio de bolso dourado com corrente (marca do Mr. Squarington)
                f'<path d="M122 200 Q140 214 150 206" stroke="#e8b923" stroke-width="3" fill="none" stroke-dasharray="4 2"/>'
                f'<rect x="144" y="204" width="20" height="10" rx="2" fill="#173a75" stroke="{K}" stroke-width="2.5"/>'
                f'<circle cx="152" cy="202" r="8" fill="#f2c230" stroke="{K}" stroke-width="2.5"/><circle cx="152" cy="202" r="4" fill="#fff6d0"/>')
    if tipo == "vestido":
        return (f'<path d="M78 116 L162 116 L176 300 L64 300 Z" fill="{cor}" stroke="{K}" stroke-width="6" stroke-linejoin="round"/>'
                f'<path d="M84 200 L156 200" stroke="{K}" stroke-width="3"/>')
    if tipo == "jaleco":
        return (f'<rect x="72" y="116" width="96" height="160" rx="6" fill="#f3f3f3" stroke="{K}" stroke-width="6"/>'
                f'<path d="M120 116 L120 276" stroke="{K}" stroke-width="3"/><rect x="132" y="150" width="22" height="20" fill="none" stroke="{K}" stroke-width="3"/>')
    if tipo == "nobre":
        return (f'<rect x="72" y="116" width="96" height="152" rx="6" fill="{cor}" stroke="{K}" stroke-width="6"/>'
                f'<path d="M96 117 L120 140 L144 117" fill="#fff" stroke="{K}" stroke-width="3"/>'
                f'<rect x="72" y="240" width="96" height="12" fill="#e8b923" stroke="{K}" stroke-width="3"/>')
    return f'<rect x="72" y="116" width="96" height="152" rx="6" fill="{cor}" stroke="{K}" stroke-width="6"/>'

def boneco(p, roupa="camisa", cor="#d97b37", cabelo="curto", cor_cabelo="#6b3a1e", pose="baixo", sob="normal", boca="fechada",
           extra_cabeca="", prop="", mecha=False, pernas=True):
    """Retorna o <g> do personagem. Partes animáveis: #p-cab, #p-pup, #p-sob, #p-boca, #p-bE/#p-bD, #p-mE/#p-mD,
    #p-prop (segue a mão direita), #p-suor, #p-lag, #p-pE/#p-pD (pernas)."""
    (e1, e2), (d1, d2) = POSE[pose]
    dE, hE = braco("E", e1, e2); dD, hD = braco("D", d1, d2)
    cab = CABELO[cabelo]
    cab_svg = f'<path d="{cab}" fill="{cor_cabelo}" stroke="{K}" stroke-width="5" stroke-linejoin="round"/>' if cab else ""
    if mecha:
        cab_svg += f'<path d="M112 -14 Q134 -30 160 -12 Q144 2 120 8 Z" fill="#fff" stroke="{K}" stroke-width="2.5"/>'
    pernas_svg = (f'<path id="{p}-pE" d="M102 266 Q101 330 98 388" stroke="{K}" stroke-width="6" fill="none" stroke-linecap="round"/>'
                  f'<path id="{p}-pD" d="M138 266 Q139 330 142 388" stroke="{K}" stroke-width="6" fill="none" stroke-linecap="round"/>'
                  f'<path d="M84 390 L100 389 M140 389 L156 390" stroke="{K}" stroke-width="5" stroke-linecap="round"/>') if pernas else ""
    return f'''<g id="{p}">
  <ellipse cx="120" cy="392" rx="58" ry="9" fill="#000" opacity=".22"/>
  {pernas_svg}
  {roupa_svg(roupa, cor)}
  <path id="{p}-bE" d="{dE}" stroke="{K}" stroke-width="6" fill="none" stroke-linecap="round"/>
  <circle id="{p}-mE" cx="{hE[0]}" cy="{hE[1]}" r="8" fill="{PELE}" stroke="{K}" stroke-width="4.5"/>
  <g id="{p}-cab">
    <path d="M68 58 Q56 64 68 74 M172 58 Q184 64 172 74" stroke="{K}" stroke-width="3" fill="{PELE}"/>
    <rect x="68" y="10" width="104" height="110" rx="9" fill="{PELE}" stroke="{K}" stroke-width="6"/>
    {cab_svg}
    <circle cx="102" cy="64" r="16" fill="#fff" stroke="{K}" stroke-width="5"/><circle cx="140" cy="64" r="16" fill="#fff" stroke="{K}" stroke-width="5"/>
    <g id="{p}-pup"><circle cx="104" cy="66" r="6" fill="{K}"/><circle cx="142" cy="66" r="6" fill="{K}"/></g>
    <rect id="{p}-pal" x="84" y="46" width="76" height="0" fill="{PELE}"/>
    <path id="{p}-sob" d="{SOB[sob]}" stroke="{K}" stroke-width="6.5" stroke-linecap="round" fill="none"/>
    <path id="{p}-boca" d="{BOCA[boca]}" fill="#3a1010" stroke="{K}" stroke-width="3" stroke-linejoin="round"/>
    <path id="{p}-suor" d="M174 26 Q184 44 174 52 Q164 44 174 26 Z" fill="#8fd3ff" stroke="{K}" stroke-width="2.5" opacity="0"/>
    <g id="{p}-lag" opacity="0"><path d="M98 80 Q94 110 100 150 M140 80 Q144 110 138 150" stroke="#6cc4ff" stroke-width="7" fill="none" stroke-linecap="round"/></g>
    {extra_cabeca}
  </g>
  <path id="{p}-bD" d="{dD}" stroke="{K}" stroke-width="6" fill="none" stroke-linecap="round"/>
  <g id="{p}-prop" transform="translate({hD[0]} {hD[1]})">{prop}</g>
  <circle id="{p}-mD" cx="{hD[0]}" cy="{hD[1]}" r="8" fill="{PELE}" stroke="{K}" stroke-width="4.5"/>
</g>'''

def mr_square(p="sq", pose="baixo", sob="normal", boca="fechada", prop=""):
    return boneco(p, roupa="terno", cabelo="topete", cor_cabelo="#2b1d14", pose=pose, sob=sob, boca=boca, mecha=True, prop=prop)

# ---------- objetos
XICARA = f'<g transform="translate(-4 -18) scale(1.45)"><path d="M-16 0 L16 0 L12 22 L-12 22 Z" fill="#fff" stroke="{K}" stroke-width="3"/><path d="M16 5 Q28 8 15 16" stroke="{K}" stroke-width="3" fill="none"/><path d="M-22 24 L22 24" stroke="{K}" stroke-width="6"/><path d="M-6 -6 Q-2 -14 -6 -22 M4 -6 Q8 -14 4 -22" stroke="#bbb" stroke-width="2" fill="none"/></g>'
RELOGIO = f'<g transform="translate(0 -24) scale(1.3)"><circle r="22" fill="#f2c230" stroke="{K}" stroke-width="6"/><circle r="16" fill="#fff6d0" stroke="{K}" stroke-width="2"/><path d="M0 0 L0 -11 M0 0 L8 4" stroke="{K}" stroke-width="3" stroke-linecap="round"/><rect x="-5" y="-30" width="10" height="8" fill="#f2c230" stroke="{K}" stroke-width="3"/></g>'
POTE = f'<g transform="translate(0 6)"><path d="M-22 -30 Q-28 0 -18 24 L18 24 Q28 0 22 -30 Z" fill="#c8794a" stroke="{K}" stroke-width="5"/><path d="M-24 -30 L24 -30" stroke="{K}" stroke-width="5"/><path d="M-12 -24 Q0 -20 12 -24" stroke="#f0d060" stroke-width="5"/></g>'
VIDRO_SANG = f'<g transform="translate(0 -6)"><rect x="-22" y="-40" width="44" height="54" rx="8" fill="#cfe9f3" opacity=".85" stroke="{K}" stroke-width="5"/><rect x="-24" y="-46" width="48" height="10" rx="3" fill="#8a5a2b" stroke="{K}" stroke-width="3"/><path d="M-12 -14 q6 -8 12 0 q6 8 12 0 M-14 2 q6 -6 12 0 q6 6 12 0" stroke="#3b2414" stroke-width="7" fill="none" stroke-linecap="round"/></g>'
TERMOMETRO = f'<g transform="rotate(-30)"><rect x="-4" y="-34" width="8" height="34" rx="4" fill="#fff" stroke="{K}" stroke-width="2.5"/><circle cy="2" r="6" fill="#e63946" stroke="{K}" stroke-width="2.5"/></g>'
CAIXA = f'<g transform="translate(-10 -10)"><rect x="-28" y="-26" width="56" height="44" fill="#c49a5a" stroke="{K}" stroke-width="5"/><path d="M-28 -12 L28 -12 M0 -26 L0 -12" stroke="{K}" stroke-width="3"/></g>'
MOEDA = f'<circle r="7" cy="-8" fill="#f2c230" stroke="{K}" stroke-width="2.5"/>'
LANTERNA = f'<g transform="translate(0 4)"><path d="M0 -26 L0 -14" stroke="{K}" stroke-width="3"/><rect x="-11" y="-14" width="22" height="28" rx="4" fill="#ffd36b" stroke="{K}" stroke-width="3"/><circle r="40" fill="#ffd36b" opacity=".18"/></g>'
FONE = f'<path d="M66 40 Q120 -14 174 40" stroke="{K}" stroke-width="6" fill="none"/><rect x="58" y="44" width="16" height="26" rx="6" fill="#333" stroke="{K}" stroke-width="3"/><path d="M66 70 Q72 96 100 100" stroke="{K}" stroke-width="3" fill="none"/>'
BONE = f'<path d="M64 30 Q120 -16 176 30 L176 36 L64 36 Z" fill="#e63946" stroke="{K}" stroke-width="5"/><path d="M150 32 L206 40 L176 40 Z" fill="#e63946" stroke="{K}" stroke-width="5"/>'
CARTOLA = f'<rect x="84" y="-38" width="72" height="48" fill="#222" stroke="{K}" stroke-width="5"/><rect x="66" y="6" width="108" height="12" rx="4" fill="#222" stroke="{K}" stroke-width="5"/>'
LENCO = f'<path d="M64 34 Q120 -8 176 34 L170 50 Q120 22 70 50 Z" fill="#7d8f5a" stroke="{K}" stroke-width="5"/>'
SUJEIRA = '<g opacity=".55"><circle cx="90" cy="96" r="7" fill="#5b4a2e"/><circle cx="150" cy="40" r="6" fill="#5b4a2e"/><circle cx="160" cy="100" r="5" fill="#5b4a2e"/></g>'

def sanguessuga(p, s=1.0):
    return (f'<g id="{p}"><g transform="scale({s})"><path d="M-30 0 Q-28 -16 0 -16 Q30 -16 32 0 Q30 14 0 14 Q-28 14 -30 0 Z" fill="#3b2414" stroke="{K}" stroke-width="3"/>'
            f'<path d="M-16 -14 Q-12 0 -16 13 M-2 -16 Q2 0 -2 14 M12 -15 Q16 0 12 13" stroke="#5c3a20" stroke-width="2.5" fill="none"/>'
            f'<circle cx="-22" cy="-3" r="2.5" fill="#fff"/></g></g>')
