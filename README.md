# Max's Poo Crew — sitio nuevo

`index.html` más la carpeta `img/`. No tiene dependencias, no necesita build, no llama
a ningún CDN. Se sube tal cual a Netlify, Vercel, Cloudflare Pages, GitHub Pages o
cualquier hosting compartido.

## Qué subir

Solo `index.html` y `img/`. La carpeta `_source/` son los originales sin procesar
(5.6 MB) y **no hace falta subirla** — está ahí por si algún día se necesita reencuadrar
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

## Lo único que falta conectar: el formulario

El formulario de "Claim your free first cleanup" hoy arma un correo con todos los datos
y abre el cliente de mail del visitante hacia `maxspoocrew@outlook.com`. Funciona, pero
depende de que la persona tenga mail configurado y le dé a "enviar".

Para que llegue directo a la bandeja de Mike sin ese paso, hay que apuntarlo a un
servicio de formularios. Con Formspree son dos cambios en `index.html`:

1. En el `<form id="quoteForm">`, agregar `action="https://formspree.io/f/XXXXXXX"`
   y `method="POST"`.
2. En el bloque `form.addEventListener("submit", ...)`, borrar el `e.preventDefault()`
   y la línea `window.location.href = href;`.

Netlify Forms es aún más simple si se hospeda ahí: basta con agregar `netlify` al `<form>`.

## Datos que hay que revisar con Mike antes de publicar

Todo el contenido salió del sitio actual (maxspoocrew.com). Vale la pena confirmar:

- **Precios.** Están los tres grupos (1 perro / 2 perros / 3+) con las cuatro
  frecuencias, tal cual la página de pricing actual.
- **Privacy Policy y Terms & Conditions.** En el footer apuntan a `#` porque el sitio
  actual las tiene como páginas aparte. Hay que pegarles la URL real o crear las páginas.
- **Redes sociales.** El sitio actual no mostraba ninguna. Si Mike tiene Facebook o
  Instagram, conviene agregarlas al footer.

## Detalles técnicos que ya vienen resueltos

- Datos estructurados de `LocalBusiness` y `FAQPage` para Google (horarios, dirección,
  teléfono, zona de servicio, precios).
- Meta tags de Open Graph para cuando compartan el link por WhatsApp o Facebook.
- Tema claro y oscuro; respeta la preferencia del sistema del visitante.
- `prefers-reduced-motion`: si alguien tiene animaciones desactivadas en su sistema,
  los perros se quedan quietos y todo sigue legible.
- Responsive de 390px hasta escritorio. En celular el botón del header cambia a
  "Call", que es lo que más se toca en un negocio local.
