# Max's Poo Crew — sitio nuevo

`index.html` más la carpeta `img/`. No tiene dependencias, no necesita build, no llama
a ningún CDN. Se sube tal cual a Netlify, Vercel, Cloudflare Pages, GitHub Pages o
cualquier hosting compartido.

## Las carpetas

| Carpeta | Qué es |
|---|---|
| `index.html` + `img/` | El sitio. Es lo único que hace falta subir para la web pública |
| `marketing/` | **Todo el material, en una página**: tres ejemplos de cada formato y las fuentes que los generan |
| `ops/` `plan/` `board/` | Herramientas internas: operación, plan, tablero |
| `social/` `client-map/` | Planificador de publicaciones y mapa de clientes |
| `quote/` | Redirección a la sección `#quote`. **No borrar:** es a donde apuntan todos los QR impresos |
| `_source/` | Los originales sin procesar. No hace falta subirla |

En agosto de 2026 `/cards`, `/flyers`, `/newdesign`, `/animation`, `/print` y `/ads` se
juntaron en `/marketing`. Estaban repartidas seis páginas de revisión con material
repetido; ahora es una sola con tres ejemplos por formato. Lo que se retiró sigue en el
historial de git.

## Dos datos que estaban mal en todo

Hasta esa misma fecha, el sitio y las 40 y pico de piezas decían **"St. Louis & St. Charles
County"** y **"Mon–Sat"**. Es **Counties** —son dos condados— y **Mon–Sun**, porque la
cuadrilla trabaja todos los días. Ya está corregido acá y en los datos estructurados, que
le venían diciendo a Google que el negocio cerraba los domingos. **Lo impreso antes lleva
el texto viejo.**

## Qué subir

Para la web pública, solo `index.html` y `img/`. `marketing/` es material interno
(está marcado `noindex`). La carpeta `_source/` son los originales sin procesar y **no hace
falta subirla** — está ahí por si algún día se necesita reencuadrar
una foto desde el archivo grande.

## Las imágenes

Todas salieron de maxspoocrew.com. Las recorté y las convertí a WebP; las siete juntas
pesan unos 620 KB, contra los 5.6 MB de los originales.

| Archivo | Qué es | Dónde se usa |
|---|---|---|
| `logo-mark.webp` | Los dos perros del logo, fondo transparente | Header |
| `logo-full.webp` | Logo completo, fondo transparente | Footer |
| `max-simon.webp` | Max y Simon echados juntos | Antes de la sección About |
| `max.webp` / `simon.webp` | Retratos recortados de cada uno | Tarjetas "Meet Max and Simon" |
| `mike-simon.webp` | Mike con Simon | Columna derecha de About |
| `banner.webp` | Banner promocional | Arriba del formulario de contacto |
| `og-banner.jpg` | Banner de Facebook | Vista previa al compartir el link |

La foto del golden corriendo (`Daycare-Homepage-Max-K9.webp`) no se usa. El original
sigue en `_source/` por si algún día se quiere recuperar.

Al logo le quité el fondo blanco con un relleno por inundación desde las esquinas, así
que los blancos internos (hocicos, el letrero) se conservaron y el logo se ve bien tanto
sobre crema como sobre café oscuro.

**Confirmar con Mike:** identifiqué a Max como el labrador chocolate y a Simon como el
negro. Lo deduje de la placa del collar en la foto y del nombre del archivo
`Mike-K9-Simon` (donde aparece con el negro). Vale la pena que él lo confirme antes de
publicar, porque los nombres aparecen en los pies de foto.

## Probarlo localmente

```
cd maxspoocrew
python3 -m http.server 8787
```

Y abrir http://localhost:8787

## El formulario

El formulario de solicitud es el embed oficial de **Jobber**. Las solicitudes
entran directo a la cuenta de Jobber de Max's Poo Crew — ya no dependen de que
el visitante tenga cliente de correo configurado.

El embed carga desde `d3ey4dbjkt2f6s.cloudfront.net`, así que necesita internet.
Si un bloqueador de anuncios o una conexión lenta impiden que cargue, aparece un
botón de respaldo que abre el mismo formulario en una pestaña nueva.

La tarjeta que lo contiene se queda blanca en ambos temas a propósito: Jobber
trae su propia hoja de estilos clara, y sobre nuestro fondo oscuro el formulario
quedaría con texto oscuro sobre oscuro.

## Datos que hay que revisar con Mike antes de publicar

Todo el contenido salió del sitio actual (maxspoocrew.com). Vale la pena confirmar:

- **Precios.** Están los tres grupos (1 perro / 2 perros / 3+) con las cuatro
  frecuencias, tal cual la página de pricing actual.
- **Privacy Policy y Terms & Conditions.** En el footer apuntan a `#` porque el sitio
  actual las tiene como páginas aparte. Hay que pegarles la URL real o crear las páginas.
- **Cuál perro es cuál.** Max es el labrador chocolate y Simon el negro, deducido de
  la placa del collar y del nombre de un archivo. Los nombres salen en los pies de foto.
- **Redes sociales.** El sitio actual no mostraba ninguna. Si Mike tiene Facebook o
  Instagram, conviene agregarlas al footer.
- **Horario y zona.** Ya corregidos a Mon–Sun y "Counties" en plural, según lo confirmó
  Mike en agosto de 2026.

## Detalles técnicos que ya vienen resueltos

- Datos estructurados de `LocalBusiness` y `FAQPage` para Google (horarios, dirección,
  teléfono, zona de servicio, precios).
- Meta tags de Open Graph para cuando compartan el link por WhatsApp o Facebook.
- Tema claro y oscuro; respeta la preferencia del sistema del visitante.
- `prefers-reduced-motion`: si alguien tiene animaciones desactivadas en su sistema,
  los perros se quedan quietos y todo sigue legible.
- Responsive de 390px hasta escritorio. En celular el botón del header cambia a
  "Call", que es lo que más se toca en un negocio local.


## Paleta

El rojo base es **#981818**, muestreado directamente del logo y del banner de
Facebook — no es un rojo inventado, es el de la marca. A partir de ahí:

- `--brand` `#C4221B` — botones y acentos
- `--brand-ink` `#A81C14` — texto de acento (contraste 6.9 sobre el fondo)
- `--brand-deep` `#981818` — sombras y estados hover

Los fondos, textos y bordes están todos inclinados hacia el rojo, así que la
página se lee roja de base y no como un crema con acentos encima.

Todas las combinaciones de texto pasan WCAG AA (4.5:1) en tema claro y oscuro.
En oscuro el rojo del botón sube a `#D63A2E` porque `#C4221B` con texto blanco
se quedaba en 3.87 — por debajo del mínimo.
