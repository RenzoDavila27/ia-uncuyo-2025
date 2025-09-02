Gráfico 1 – Porcentaje promedio limpiado según el tamaño

![Texto alternativo](
https://raw.githubusercontent.com/RenzoDavila27/ia-uncuyo-2025/refs/heads/main/tp2-agentes-racionales/images/grafico1.png)

Este gráfico compara el rendimiento de los agentes reflexivo y random a medida que aumenta el tamaño del entorno (desde 2x2 hasta 128x128).

Los porcentajes de limpieza obtenidos son un promedio de los porcentajes limpiados con cada dirt_rate probado (0.1, 0.2, 0.4 y 0.8). Por ejemplo en el caso del agente 16x16 del agente reflexivo simple, se obtuvieron los siguientes resultados (expresados en casillas_limpiadas/suciedad_total): 18/25, 38/51, 75/102 y 143/204. A partir de estos valores se obtiene el porcentaje de limpieza en cada caso y se busca la media de los mismos: (0.72+0.745098+0.735294+0.700980) / 4 = 0,725343137, aproximadamente el 70%.

Se observa que ambos agentes logran un 100% de limpieza en entornos pequeños (2x2, 4x4 y 8x8).

A partir de entornos más grandes, el rendimiento disminuye:

El agente reflexivo mantiene mejores resultados que el random.

En 16x16 logra limpiar alrededor del 70%, mientras que el random apenas llega al 30%.

En entornos grandes (64x64 y 128x128), ambos agentes caen a niveles muy bajos, pero el reflexivo aún conserva una ligera ventaja.

En conclusion el agente reflexivo escala mejor que el random, aunque ninguno de los dos mantiene un buen desempeño en entornos muy extensos.



Gráfico 2 – Porcentaje limpiado según la cantidad de suciedad (16x16)

![Texto alternativo](https://raw.githubusercontent.com/RenzoDavila27/ia-uncuyo-2025/refs/heads/main/tp2-agentes-racionales/images/grafico2.png)

Este gráfico muestra la influencia del dirt rate (0.1 a 0.8) en el porcentaje de limpieza para ambos agentes, en un entorno fijo de 16x16.

El agente reflexivo mantiene un desempeño relativamente alto, limpiando entre el 70% y 75% de la suciedad en todos los niveles.

El agente random muestra un rendimiento mucho más bajo y estable, alrededor del 30% en todos los casos.

En conclusion el reflexivo es mucho más eficiente, independientemente de la cantidad de suciedad. El random parece no adaptarse a la variación en el dirt rate.

Esta estructura, donde los agentes siempre obtienen un porcentaje de limpieza equivalente a la cantidad de suciedad, se mantiene en todos los graficos mayores a 8x8, mientras que en los entornos mas pequeños, ambos agentes limpian la totalidad del espacio, debido a la cantidad de acciones disponible.

Se decidio incluir unicamente el 16x16 ya que es un caso intermedio, en donde se puede ver de mejor forma la diferencia de la limpieza entre agentes. En los graficos de entornos mas grandes, se vera la misma estructura, pero el porcentaje de limpieza de cada agente va a disminuir de forma equivalente.
