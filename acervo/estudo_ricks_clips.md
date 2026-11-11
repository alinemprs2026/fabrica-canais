# Estudo do estilo Ricks Clips (análise quadro a quadro, 1 quadro/s, 6 maiores sucessos)

Canal só de shorts: 150 shorts, 170 mil inscritos, 424 milhões de views, mediana 670 mil, recentes 9–28 milhões.
Vídeos estudados: Why Perfect Railroads Don't Work (28M), The Job Nobody Wants in Japan (17M), Why Sailors Carried Storm Oil (15M),
The Window That Breaks Japan's Gambling Law (15M), What the Grave Bell Really Meant (12M), The Burglar Who Only Moved Furniture (9,2M).
Folhas: `pesquisa/ricks/*_1fps_*.jpg`.

## Fórmula das histórias ("irreais mas verdadeiras")
- Título = objeto/pessoa + mistério: "The Ancient Jar That Warned an Empire", "Why Perfect Railroads Don't Work", "The Job Nobody Wants in Japan",
  "What the Grave Bell Really Meant", "The Burglar Who Only Moved Furniture", "Why Humans Can't Pick Random Numbers".
- 45–65 s. Gancho = paradoxo dito como fato. Um personagem comum, conflito que escala, explicação do mecanismo com analogia, virada irônica no fim.
- Temas: engenharia/física do cotidiano, leis estranhas, história, psicologia, Japão, golpes e truques.

## Câmera (o que mais diferencia)
- QUASE NÃO HÁ CORTE SECO: 0 a 2 cortes por vídeo. Câmera contínua que voa de um lugar ao outro.
- Lente grande-angular (perspectiva exagerada). Câmera BAIXA, na altura do chão/trilho, com linhas que fogem para o horizonte.
- Primeiro plano gigante e desfocado (botão, cabeça, trilho) com o assunto atrás → profundidade.
- Planos aéreos enormes (cânion, estação, escritório visto de cima) contra personagem minúsculo → escala.
- Transições: chicote com borrão de movimento (riscos coloridos), dissolve/dupla exposição em saltos de tempo,
  personagem/objeto passando na frente da câmera e "limpando" a tela, atravessar porta/janela.
- Close extremo em objeto que explica (fresta no trilho, calendário, relógio, moeda, celular, jornal) — "insert" a cada 5–8 s.
- Nada parado: empurrões lentos, giros em volta, subidas de grua.

## Luz e sombra
- Sol forte com sombras projetadas nítidas dos personagens no chão 3D.
- Feixes de luz (janela/teto de vidro). Cor conta o tempo: dia azul/terracota, pôr do sol rosa/laranja, noite azul.
- Explicação científica com COR: trilho aquecendo muda de roxo → rosa → amarelo brilhante.
- Leve vinheta, saturação alta, céu com nuvens macias.

## Personagens
- 2D chapado (cabeça grande branca, contorno preto grosso, corpo de tubo com roupa, braços/pernas de linha) dentro do 3D.
- Inclinam para a câmera em closes; expressões trocam o tempo todo; rosto muda de cor (roxo de raiva), fumaça, gota de suor.
- Chapéus e roupas definem o papel (boné listrado = operário, chapéu-coco = chefe, cartola = rico).

## Mundo 3D
- Construído com formas simples + texturas pintadas (pedra, madeira, tijolo, piso), contorno de tinta, cores saturadas.
- Texto dentro da cena (faixas, jornais, placas, calendário) carrega a informação.

## Legenda
- 1 palavra por vez, branca com contorno preto, pequena, fixa em ~70% da altura.

## Medidas numéricas (fluxo óptico 6 amostras/s, quadro 180x320) — `pesquisa/ricks/medidas.json`
- Câmera parada (movimento < 1,5): **0 segundos** em 127 s medidos. Movimento médio 28–30 px/s (≈ 1/6 da largura por segundo).
- Zoom: predominam empurrões de **+5 a +25 % por segundo**; afastamentos rápidos (−10 a −30 %/s) só em viradas/revelações.
- Panorâmicas laterais de até 25–33 px/s nas viagens entre lugares; tilts fortes (±15–20 px/s) em subidas de grua.
- **Mudança forte de imagem a cada ~1,5–2 s** (corte, chicote com borrão ou dissolve) — mais rápido do que parece a olho.
- Saturação média 110–124 (alta); brilho varia 60–200 por cena (dia claro, interior escuro, explicação estourada).
- Regra para o nosso motor 3D: troca visual a cada 1,5–2 s, câmera sempre andando (mínimo ~8 px/s), push-in como padrão,
  pull-back rápido nas revelações, chicote com borrão entre lugares, saturação alta.

## Lições do vídeo "Fiz 10 Vídeos Virais no Claude" (LABS, transcrito em `pesquisa/video-ref/transcricao.txt`)
- Analisar 1 quadro/s com 3 medidas (folhas de quadros, movimento de câmera, cores) e transformar em números.
- Roteiro: absurdo na 1ª frase → ano e lugar → contexto → problema escalando → virada → frase final irônica. ~86 palavras em 30 s, narração rápida quase sem pausa.
- Personagens planos iluminados como reais (sombra no chão), mundo 3D de verdade com contorno preto, luz quente.
- Voz grátis clonada localmente: Voicebox (alternativa à voz robótica).
