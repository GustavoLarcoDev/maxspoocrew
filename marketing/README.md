# /marketing/ — todo el material, en una página

`index.html` es **la** página. Antes esto estaba repartido en `/cards`, `/flyers`,
`/newdesign`, `/animation`, `/print` y `/ads`; ahora es una sola, con **tres ejemplos de cada
formato** y el resto retirado.

```
marketing/
  index.html        la página
  src/              las fuentes, un archivo por pieza
  scenes/           las tres animaciones (SVG + CSS)
  pdf/              lo que recibe la imprenta
  img/              las vistas previas de la página
  video/            animaciones y los dos comerciales
  build.py          fuentes -> pdf/ + img/
  build_video.py    escenas -> video/ + portada
```

## Qué hay

| Formato | Trim | Piezas |
|---|---|---|
| Tarjetas de presentación | 3.5 × 2 in | `card-classic` `card-quiet` `card-band` |
| Door hangers | 4.5 × 11 in | `hanger-vp-street` `hanger-vp-price` `hanger-vp-photo` |
| Flyers carta | 8.5 × 11 in | `flyer-i-free` `flyer-j-health` `flyer-q-move` |
| Rack cards | 3.75 × 8.25 in | `rack-i-free` `rack-j-health` `rack-q-move` |
| Mini cards | 3.75 × 8.25 in | `mini-1-sit` `mini-2-lie` `mini-3-pair` |
| Imanes de vehículo | 18×12, 12×8, 24×6 in | `magnet-door` `magnet-compact` `magnet-tailgate` |
| Piezas con foto | 8.5×11, 18×12 in | `ai-ad-lawn` `ai-ad-crest` `ai-magnet-portrait` |
| Animaciones | 720 × 1280, 11 s | `scene-1-morning` `scene-2-golden` `scene-5-both` |

Más los dos comerciales, que son dos y no tres: son las únicas piezas que necesitan material
filmado, y filmar es la parte cara.

## Cómo se compila

```bash
pip install -r requirements.txt
python build.py                  # todo el impreso
python build.py hanger           # solo lo que coincida
python build_video.py            # las animaciones
```

Necesita Chrome, y ffmpeg para el video.

**El tamaño sale del propio archivo.** `build.py` lee la regla `@page { size: W in H in }` de cada
fuente en vez de tener una lista aparte, así que el pliego no se puede desincronizar del arte.

**Si una hoja se desborda, el build falla.** Cada fuente declara cuántas hojas es con
`<meta name="pages">`. Las hojas no llevan `overflow:hidden` a propósito: si el contenido no cabe,
Chrome lo empuja a una página extra, el conteo no cuadra y el build sale con error. Así se
descubrió que dos de los tres door hangers se pasaban — se les recortó texto, que es lo único que
sirve cuando `.cta` lleva `margin-top:auto` y se come el espacio que liberes.

## Los door hangers

Van a **4.5 × 11 in, que es la medida de Vistaprint** (pliego 4.75 × 11.25 con sangrado).

**No son 4.25 × 11.** Esa medida existe, pero es de GotPrint y Conquest. Subir un 4.25 a Vistaprint
termina en un escalado.

**El agujero no se dibuja.** Lo troquela Vistaprint con su propia matriz, y un agujero dibujado que
no coincide con la matriz es peor que ninguno. Lo que sí se hace es dejar **las primeras 2.5 in del
pliego sin nada que importe**, así que caiga donde caiga, corta color plano o pasto y no una
palabra.

Eso deja menos de cinco pulgadas para el argumento, y por eso la tipografía acá es más chica que en
las rack cards aunque el pliego sea más grande.

## Las animaciones

Cada escena es un HTML: SVG y CSS, sin librerías. El texto de la placa va **encima** de la escena,
nunca dibujado adentro — un teléfono dentro de una imagen no se corrige sin rehacer la imagen.

Las tres comparten `scenes/_scene.css` y **un solo reloj de 11 segundos**. Los tiempos de recogida
salen resueltos de la velocidad a la que camina la persona y la posición de cada montón, no puestos
a ojo.

`build_video.py` lanza Chrome una vez por fotograma y le pide a la escena que se posicione sola con
`?t=` — abrir `scenes/scene-1-morning.html?t=6.3` congela el bucle en el segundo 6.3. El reloj
virtual de Chrome no sirve para esto: `transform` y `opacity` corren en el compositor, donde no
llega, y los 275 fotogramas salen idénticos.

## Los dos datos que estaban mal en todo

Hasta agosto de 2026, **todas** las piezas y el sitio decían:

- "St. Louis & St. Charles **County**" — es **Counties**, son dos condados.
- "Mon–**Sat**" — es **Mon–Sun**, la cuadrilla trabaja todos los días.

Las piezas de acá ya están corregidas, y `index.html` también, incluidos los datos estructurados
que le decían a Google que el negocio cerraba los domingos. **Lo impreso antes de esa fecha lleva
el texto viejo**, y conviene revisarlo antes de una reimpresión y no después.

Salieron del sitio, que es de donde se copiaron: el sitio venía atrasado respecto del negocio.

## El eslogan

El impreso lleva **"We scoop it. You enjoy it."**, que es el H1 del sitio.

Las animaciones cierran con **"We scoop your yard. You enjoy it."**, que es lo que se pidió. Son
dos líneas distintas dando vueltas; conviene decidir cuál queda. Ya pasó una vez que una pieza
salió con un eslogan que no era de la casa (*"No pile left behind"*, que además parafraseaba a un
competidor) y hubo que rehacerla.
