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

## El código QR

`src/qr-site.svg` apunta a `https://maxspoocrew.com` con corrección de errores alta, que es
la que aguanta que el impreso se raye o se moje. Para regenerarlo:

```bash
pip install segno
python -c "import segno; segno.make('https://maxspoocrew.com', error='h').save('src/qr-site.svg', scale=10, border=0, dark='#331411')"
```

## Antes de mandar a imprimir

- **La postal EDDM tiene un espacio marcado en rojo donde va el número de permiso.** Sin
  ese número el correo no la acepta. Sale de tu propio papeleo de EDDM Retail.
- **Los precios están escritos en el arte.** Si cambian en la web, hay que cambiarlos en
  `sheet-rates.html`, `trifold-l-plans.html`, `card-visit.html` y `postcard-eddm.html` y
  volver a compilar.
- El teléfono, el correo y la dirección salen del sitio: 618-719-3802,
  maxspoocrew@outlook.com, 229 Chesterfield Business Pkwy, Chesterfield, MO 63005.
