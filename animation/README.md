# /animation/ — cinco animaciones de once segundos

`index.html` es la galería. Las cinco escenas viven en `scenes/` y los MP4 que salen de
ellas en `video/`.

Las cinco cuentan lo mismo: un perro hace lo suyo en el patio, la cuadrilla pasa por
detrás y lo levanta, y cierra la placa con el logo, el teléfono y la web. Cambian la luz
y el reparto, no la historia.

| Escena | Qué la distingue |
|---|---|
| `scene-1-morning` | Sol temprano, labrador negro. La lectura simple |
| `scene-2-golden` | Última luz, labrador chocolate. La más cálida |
| `scene-3-dusk` | Hora azul. La cuadrilla trabaja hasta las seis |
| `scene-4-overcast` | Gris y hojas caídas: la visita pasa igual |
| `scene-5-both` | Max y Simon juntos. Más perros es el upsell |

## Cómo están hechas

Cada escena es **un HTML**: dibujo en SVG y animación en CSS. Sin librerías, sin build,
sin nada generado. Se abren solas en cualquier navegador.

El texto de la placa final es **texto de verdad encima de la escena, nunca dibujado
adentro** — la misma regla que siguen los dos comerciales de `/ads/` y por el mismo
motivo: un teléfono dibujado dentro de una imagen no se corrige sin rehacer la imagen.

### El reloj compartido

Las cinco comparten `scenes/_scene.css`, que trae el estilo del dibujo y **una sola línea
de tiempo de 11 segundos**. Todo lo que se mueve corre sobre ese mismo reloj, así que los
porcentajes de los keyframes son una referencia común y no una estimación por elemento:

```
 0 -  3%   patio vacío
 3 - 20%   el perro entra desde la izquierda
20 - 29%   se agacha, hace lo suyo, se levanta
29 - 38%   se va trotando a la derecha
42 - 68%   la cuadrilla recorre la misma línea recogiendo
49 - 56%   cada montón desaparece cuando la pala lo alcanza
70 - 75%   el pasto limpio brilla
76 -100%   placa: logo, eslogan, web, teléfono
```

1% = 110 ms. **Los tiempos de recogida están resueltos, no calculados a ojo**: salen de la
velocidad a la que camina la persona y de la posición de cada montón. Si se mueve un
montón en x, hay que mover su desvanecido — el cálculo está en el comentario de
`_scene.css`.

## Qué se edita y dónde

- **El teléfono, la web o el eslogan** → las seis líneas del final de cada escena.
- **El dibujo o los tiempos, para las cinco** → `_scene.css`.
- **La luz o el perro de una escena** → las propiedades del `:root` de esa escena.

## Los MP4

```bash
python build_video.py                 # las cinco
python build_video.py morning         # solo las que coincidan
python build_video.py --fps 30
```

Necesita **ffmpeg** en el PATH y Chrome. Escribe `video/*.mp4` y un fotograma de portada
en `poster/`.

### Por qué lanza Chrome una vez por fotograma

Porque las escenas se posicionan solas con `?t=`. Abrir
`scenes/scene-1-morning.html?t=6.3` congela el bucle en el segundo 6.3, y de ahí sale el
fotograma.

La alternativa obvia —`--virtual-time-budget`, el reloj virtual de Chrome sin interfaz—
**no sirve acá**: las animaciones de `transform` y `opacity` corren en el compositor,
donde ese reloj no llega, y los 275 fotogramas salen idénticos. Se probó; por eso está
el `?t=`.

Grabar la pantalla tampoco: pierde fotogramas cuando la máquina está ocupada, y entonces
que el teléfono se lea o no depende del humor del equipo.

Son 275 lanzamientos de Chrome por escena, en paralelo entre los núcleos. Unos minutos
por escena.

## Dos cosas para decidir antes de publicar

**El eslogan de la placa dice "We scoop your yard. You enjoy it.", que es lo que se
pidió — y no es el del sitio.** El sitio dice **"We scoop it. You enjoy it."**, y eso es
lo que llevan todas las piezas impresas. Es una línea por escena; lo que no conviene es
dejar dos eslóganes dando vueltas, porque nadie lo nota hasta que el impreso y el feed se
contradicen.

El teléfono es **636-681-4832** en las cinco, igual que el resto del material.
