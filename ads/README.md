# /ads/ — plan de captación y contenido listo para publicar

`index.html` es la página: la estrategia, diez anuncios listos para copiar y pegar, y los
dos comerciales. Las imágenes de los anuncios no se generan acá — salen de `/print/`, que
es material que ya existía.

## Los comerciales

Se arman en dos pasos, y esa separación es a propósito.

**1. El material filmado** lo genera Sora (`sora-2`) con
`Claude Images/make_video.py`, fuera de este repo. Vertical 720×1280, doce segundos, que
es el clip más largo que da Sora de una sola pasada. El archivo crudo se guarda en
`src/raw/`.

**2. La placa de cierre** es `src/endcard.html`, HTML de verdad renderizado a 720×1280 con
Chrome sin interfaz y pegado al final del clip por `build_video.py`.

```bash
python build_video.py     # lee src/raw/*.mp4, escribe video/*.mp4
```

Necesita **ffmpeg** en el PATH (`winget install Gyan.FFmpeg`) y Chrome.

### Por qué separado

A Sora **no se le pide texto ni el logo**. Las letras generadas salen mal escritas a este
tamaño y no se pueden corregir sin volver a generar el clip entero. El logo, el teléfono,
la web y la oferta viven en un archivo HTML.

El beneficio práctico: si cambia el número o la oferta, se edita `src/endcard.html`, se
corre `build_video.py` y **los dos comerciales quedan rehechos en segundos, sin material
filmado nuevo**.

### La estructura del clip terminado

```
material filmado (12 s)  →  cross-fade 0.6 s  →  placa de cierre (2.5 s)
```

Los subtítulos van con la herramienta de Meta, no quemados en el archivo, por la misma
razón: el feed se mira sin sonido y un subtítulo quemado no se puede corregir ni traducir.

## Los diez anuncios

Dos por cada formato que le sirve a un negocio de servicios: imagen, video, carrusel,
formulario de contacto y click-to-Messenger.

**Collection y Dynamic Product Ads no están, a propósito.** Los dos necesitan un catálogo
de productos, que un negocio de servicios no tiene.

## Las cifras

Todo número de la página tiene fuente citada al pie. Las de economía del negocio salen de
operadores del mismo rubro; las de rendimiento por formato son datos de Meta 2026 de toda
la industria. Son una expectativa contra la cual medir, no una promesa — St. Louis es su
propio remate.
