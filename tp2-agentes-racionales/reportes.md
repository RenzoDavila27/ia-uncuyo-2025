Gráfico 1 – Porcentaje promedio limpiado según el tamaño

Este gráfico compara el rendimiento de los agentes reflexivo y random a medida que aumenta el tamaño del entorno (desde 2x2 hasta 128x128).

Se observa que ambos agentes logran un 100% de limpieza en entornos pequeños (2x2, 4x4 y 8x8).

A partir de entornos más grandes, el rendimiento disminuye:

El agente reflexivo mantiene mejores resultados que el random.

En 16x16 logra limpiar alrededor del 70%, mientras que el random apenas llega al 30%.

En entornos grandes (64x64 y 128x128), ambos agentes caen a niveles muy bajos, pero el reflexivo aún conserva una ligera ventaja.

En conclusion el agente reflexivo escala mejor que el random, aunque ninguno de los dos mantiene un buen desempeño en entornos muy extensos.



Gráfico 2 – Porcentaje limpiado según la cantidad de suciedad (16x16)

Este gráfico muestra la influencia del dirt rate (0.1 a 0.8) en el porcentaje de limpieza para ambos agentes, en un entorno fijo de 16x16.

El agente reflexivo mantiene un desempeño relativamente alto, limpiando entre el 70% y 75% de la suciedad en todos los niveles.

El agente random muestra un rendimiento mucho más bajo y estable, alrededor del 30% en todos los casos.

En conclusion el reflexivo es mucho más eficiente, independientemente de la cantidad de suciedad. El random parece no adaptarse a la variación en el dirt rate.
