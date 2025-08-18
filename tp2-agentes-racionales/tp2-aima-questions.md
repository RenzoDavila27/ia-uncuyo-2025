
2.10: 

    Considere una versión modificada del vacuum environment del Ejercicio 2.8, en la que el agente recibe una penalización de un punto por cada movimiento.

    a. ¿Puede un agente reflexivo simple ser perfectamente racional en este entorno? Explique.

        No, no puede ser perfectamente racional, ya que el agente no conoce la ubicacion de la suciedad, por lo que no puede encontrar el camino con menor cantidad de movimientos para limpiarla en su totalidad. Este caso sera el que ocurrira la mayor parte de las veces, pero pueden existir casos extraordinarios en donde el agente consiga maximizar la medida de desempeño.

    b. ¿Qué ocurre con un agente reflexivo con estado? Diseñe dicho agente.

        Con un agente reflexivo simple la cosa cambia, ya que este tendra conocimiento de aquellas casillas que ya limpio, y por las cuales ya paso. Por lo que podra practicar para poder buscar el mejor recorrido posible, maximizando las celdas limpiadas y minimizando los movimientos.

    c. ¿Cómo cambian sus respuestas a las preguntas a y b si las percepciones del agente le asignan el estado limpio/sucio de cada casilla del entorno?

        Si conocemos todas las casillas sucias y limpias, podemos crear un agente reflexivo simple que se dirija hacia aquellas casillas sucias, las limpie, y cuando se hayan limpado todas simplemente detenerse, haciendo de este mismo perfectamente racional.

2.11: 

    Considere una versión modificada del vacuum environment del Ejercicio 2.8, en la que se desconoce la geografía del entorno (su extensión, límites y obstáculos), así como la configuración inicial de la suciedad. (El agente puede moverse hacia arriba y hacia abajo, así como hacia la izquierda y la derecha).

    a. ¿Puede un agente reflexivo simple ser perfectamente racional en este entorno? Explique.

        No, ya que como se menciono anteriormente, este no tiene nocion de la ubicacion de la suciedad, por lo que podria estar infinitamente ciclando entre diferentes casillas y no terminar de limpiarlas todas.

    b. ¿Puede un agente reflexivo simple con una función de agente aleatoria superar a un agente reflexivo simple? Diseñe dicho agente y mida su rendimiento en varios entornos.

        Si, podria, pero en la mayor parte de los casos, el agente randomizado no limpiara algunas casillas sucias debido a su comportamiento aleatorio, esto hara que quede en desventaja con el que reacciona limpiando las casillas sucias. 


    c. ¿Puede diseñar un entorno en el que su agente aleatorio tenga un rendimiento deficiente? Muestra tus resultados.

        Si, aquellos entornos los cuales tengan "pasillos cerrados", sera deficiente, ya que el agente no podra pasar los mismos con facilidad. Un ejemplo podrian ser dos cuadriculas de n x n, las cuales esten unidas por un pasillo de (1 x m) o (m x 1), para llegar de una cuadricula a la otra el agente deberia conseguir recorrer todo el pasillo de longitud m.

    d. ¿Puede un agente reflexivo con estado superar a un agente reflexivo simple? Diseña dicho agente y mide su rendimiento en varios entornos. ¿Puedes diseñar un agente racional de este tipo?

        En la mayor parte de los casos si, ya que este recordara sobre que celdas ya ha estado, por lo que podra construir un mapa y recorrer unicamente aquellas las cuales no hayan sido observadas.