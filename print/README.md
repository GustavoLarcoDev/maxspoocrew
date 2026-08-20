# Material impreso

`index.html` es la galería para elegir piezas. `pdf/` son los archivos que se le mandan
a la imprenta y `img/` son las vistas previas que salen en la galería.

## Lo que tiene fuente editable

Las piezas nuevas se generan desde HTML en `src/`. Las viejas (los primeros 41 archivos)
existen solo como PDF terminado — para cambiarles algo hay que rehacerlas como fuente
primero.

| Fuente | Pieza | Trim |
|---|---|---|
| `trifold-l-plans.html` | Tríptico con la matriz completa de precios | 11 × 8.5 in |
| `flyer-f-commercial.html` | Flyer para HOA y administradoras | 8.5 × 11 in |
| `flyer-g-reset.html` | Flyer de limpieza única, sin plan | 8.5 × 11 in |
| `sheet-rates.html` | Lista de precios de una página | 8.5 × 11 in |
| `postcard-eddm.html` | Postal de correo directo USPS EDDM | 9 × 6.5 in |
| `card-business.html` | Tarjeta de presentación | 3.5 × 2 in |
| `card-referral.html` | Tarjeta de referidos ($20 y $20) | 4 × 6 in |
| `card-visit.html` | Tarjeta "estuvimos aquí" para la reja | 4 × 6 in |
| `magnet-door.html` | Imán de puerta, camioneta | 18 × 12 in |
| `magnet-compact.html` | Imán de puerta, auto | 12 × 8 in |
| `magnet-tailgate.html` | Tira para la tapa trasera | 24 × 6 in |
| `ai-ad-lawn.html` | Anuncio con foto generada | 8.5 × 11 in |
| `ai-ad-crest.html` | Afiche retro con escudo generado | 8.5 × 11 in |
| `ai-magnet-portrait.html` | Imán con retrato generado | 18 × 12 in |
| `ai-magnet-emblem.html` | Imán con emblema retro generado | 12 × 8 in |
| `ai-sticker-round.html` | Calcomanía redonda troquelada | 6 in ø |
| `ai-sticker-bumper.html` | Calcomanía de paragolpes | 10 × 3 in |
| `flyer-h-price.html` … `flyer-q-move.html` | Los diez flyers carta | 8.5 × 11 in |
| `rack-h-price.html` … `rack-q-move.html` | Los mismos diez, verticales | 3.75 × 8.25 in |
| `simple-1-scoop.html` … `simple-3-barefoot.html` | Los tres simples: foto, logo, una línea | 8.5 × 11 in |
| `mini-1-sit.html` … `mini-3-pair.html` | Lo mínimo: foto, logo, eslogan, teléfono, web, QR | 3.75 × 8.25 in |

Los diez flyers H–Q comparten `src/_flyer.css` y las diez rack cards comparten
`src/_rack.css`; los dos esqueletos traen la cabecera, el cuerpo, el CTA, el pie y la
regla `@page`. Por eso cada archivo lleva casi puro contenido: veinte piezas que discuten
diez cosas tienen que seguir pareciendo de la misma empresa. Se ven lado a lado en
**`/flyers/`**.

La rack card entra **un tercio del texto** que la hoja carta, y esa es toda la
restricción del formato. Cada tarjeta se queda con una idea y para. La tarjeta de
comparación tuvo que soltar la tabla entera: tres columnas de tildes en 3.15 in de ancho
vivo no es una tabla, es un examen de la vista — va como tres bloques apilados.

Ojo con una trampa de los dos esqueletos: `.cta` usa `margin-top:auto`, así que se come
cualquier espacio que liberes achicando márgenes y la altura total no se mueve. Si una
pieza se desborda hay que **sacar contenido**, no apretar el espaciado.

## Cómo se compila

```bash
pip install -r requirements.txt      # solo PyMuPDF, para las vistas previas
python build.py                      # todo
python build.py magnet               # solo lo que coincida con "magnet"
```

`build.py` manda cada HTML a Chrome sin interfaz, guarda el PDF en `pdf/` y de ahí saca un
JPG por página en `img/`. No hay paso manual: la vista previa que se ve en la galería sale
del mismo archivo que recibe la imprenta.

Chrome se busca en las rutas típicas de Windows, macOS y Linux; si está en otro lado, se
edita `CHROME_CANDIDATES` en `build.py`.

## Las dos comprobaciones que hace el build

**El tamaño sale del propio archivo.** `build.py` lee la regla `@page { size: W in H in }`
de cada fuente en lugar de tener una lista aparte, así que el tamaño del pliego no se puede
desincronizar del arte.

**Si una hoja se desborda, el build falla.** Cada fuente declara cuántas hojas es con
`<meta name="pages" content="N">`. Las hojas *no* llevan `overflow:hidden` a propósito: si
el contenido no cabe, Chrome lo empuja a una página extra, el conteo no cuadra y `build.py`
sale con error. Recortar el sobrante lo escondería, y un flyer con el pie cortado no se
nota hasta que llega la caja de la imprenta.

Ojo con esto: el desborde puede aparecer solo en medio impreso. Un pliego puede medir
exactamente 11.25 in en pantalla y aun así partirse al imprimir, porque el interlineado y
la fragmentación no se resuelven igual. El conteo de páginas del build es la autoridad, no
lo que se mida en el navegador. Si una pieza se desborda por poco, hay que quitarle
contenido de verdad — reducir márgenes no sirve cuando hay un `margin-top:auto` que se come
el espacio que liberaste.

## Sangrado y dobleces

Todas las piezas llevan **1/8 in (0.125 in) de sangrado por lado**, así que el pliego mide
0.25 in más que el trim en cada dimensión. El texto vivo se mantiene al menos 0.25 in
adentro del corte.

En los trípticos, el panel que se dobla hacia adentro va **1/16 in más angosto** que los
otros dos (3.6042 / 3.6979 / 3.6979 in). Sin esa holgura el doblez se abomba. Si la
imprenta ofrece "emparejar" los paneles, hay que decir que no.

## Tipografías

Archivo y Archivo Black están en `src/fonts/` y se cargan con `@font-face` desde el disco,
no desde Google Fonts. Una vez un PDF salió con la tipografía de reserva porque la red
falló en mitad del build, y eso no se ve hasta que el trabajo está impreso. La licencia
(SIL Open Font License) está en `src/fonts/OFL.txt`.

## Las piezas "AI reimagine"

El arte de `src/img-ai/` se generó con `gpt-image-2`. **Ninguna imagen tiene una sola letra
adentro, a propósito.** El texto generado dentro de una imagen no se puede editar, se
escribe mal en tamaños chicos y se deshace al reescalarlo a medida de imprenta. Entonces
las imágenes son solo imágenes y cada palabra encima es texto real del HTML: cambiar un
precio es editar una línea, no volver a generar nada.

El escudo retro se pidió con la cinta **en blanco** justamente para poder ponerle texto
encima después. Por eso la misma ilustración dice "NO PILE LEFT BEHIND" en el afiche y el
teléfono en la calcomanía redonda, sin regenerarse.

### Hasta dónde se pueden agrandar

El arte generado sale a un tamaño fijo de píxeles, así que cada pieza tiene techo:

| Pieza | Resolución efectiva |
|---|---|
| `ai-ad-lawn` | ~176 dpi |
| `ai-ad-crest` | ~160 dpi |
| `ai-magnet-portrait` | ~125 dpi |
| `ai-magnet-emblem` | ~125 dpi |
| `ai-sticker-round` | ~164 dpi |
| `ai-sticker-bumper` | más de 400 dpi |

Los 125 dpi de los imanes son normales para gráfica vehicular, que se lee a varios pies —
y son la razón por la que la foto del 18×12 va en un panel y no estirada a lo ancho.

**No agrandar ninguna de estas a un cartel de 24×18 ni a un wrap de vehículo.** A ese
tamaño los mismos archivos caen debajo de 65 dpi y el pelo de los perros se pone blando.
Para algo más grande hay que volver a generar el arte en tamaño mayor; los prompts están
en `Claude Images/prompts/` fuera de este repo.

## Los códigos QR

Hay uno por formato, no uno solo. Todos van a `https://maxspoocrew.com/` pero cada uno se
etiqueta a sí mismo — `?utm_source=trifold&utm_medium=print`, `flyer`, `rack`, `card`,
`eddm`, `ratecard`, `hanger`, `menu` — así Analytics puede decir **qué pieza** trae los
escaneos y no solo que "el impreso funciona". Las 41 piezas originales ya usaban esa
convención; los nombres se conservan igual para que los datos viejos y los nuevos caigan
en el mismo balde.

```bash
pip install segno
python make_qr.py        # reescribe los ocho SVG en src/
```

Tres detalles del generador que no son cosméticos:

- **`border=4`** — la zona de silencio que pide la norma. Sin ella el lector no tiene de
  dónde agarrarse y el escaneo se vuelve poco fiable *de una forma que solo aparece en
  papel*. Los QR se generaron una vez con `border=0` y decodificaban a veces sí y a veces
  no según la pieza; en papel eso es una tirada perdida.
- **`light="#ffffff"`** — campo blanco explícito, para que el código lleve su propio
  contraste en vez de heredar lo que el arte le ponga detrás.
- **`error='h'`** — la corrección de errores alta, que aguanta que el impreso se raye o se
  moje.

### Comprobar que escanean

```bash
pip install opencv-python-headless pymupdf
python checkqr.py
```

Decodifica el QR **del PDF ya renderizado**, no del SVG, y falla si alguna pieza deja de
escanear o pierde su etiqueta. Un QR que no lee no se descubre en pantalla. Tarda unos
minutos porque prueba varias resoluciones: en una hoja cargada el detector se engancha con
una línea de tabla o el borde de una foto y reporta "no hay QR" cuando sí lo hay.

Las piezas sin QR a propósito son los carteles, los imanes y las calcomanías: se leen desde
un auto en movimiento, donde nadie está escaneando nada.

## El eslogan

Es **"We scoop it. You enjoy it."**, el H1 del sitio y el `og:title`. Sale de ahí, no se
inventa.

Tres piezas —el imán de puerta 18×12 y los dos anuncios AI— salieron una vez con *"No pile
left behind"*, que **no es de Max's Poo Crew**: se escribió para estas maquetas y además
parafrasea de cerca la línea de un competidor, lo cual en el costado de una camioneta es un
problema. Ya están las tres corregidas. Si alguna se llegó a imprimir, esas son las que hay
que reimprimir.

## Antes de mandar a imprimir

- **La postal EDDM tiene un espacio marcado en rojo donde va el número de permiso.** Sin
  ese número el correo no la acepta. Sale de tu propio papeleo de EDDM Retail.
- **Los precios están escritos en el arte.** Si cambian en la web, hay que cambiarlos en
  `sheet-rates.html`, `trifold-l-plans.html`, `card-visit.html` y `postcard-eddm.html` y
  volver a compilar.
- El teléfono, el correo y la dirección salen del sitio: 636-681-4832,
  maxspoocrew@outlook.com, 229 Chesterfield Business Pkwy, Chesterfield, MO 63005.
