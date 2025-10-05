## Reporte para el Trabajo Practico 5: CSP

### Representacion del sudoku:

Para la resolucion del sudoku se supone un tablero de 9x9, donde cada casilla tiene un dominio de 9 posibilidades (del 1 al 9). Las restricciones es que dos casillas no pueden ser iguales en una linea tanto vertical o horizontal, ni en el subcuadrado (3x3) al que pertenece la casilla.

El algoritmo comenzara seleccionando una casilla, esto lo hara usando MRV, seleccionando la celda con menor opciones en el dominio (en el sudoku, empezara por aquellas casillas ya colocadas), en caso de empate puede seleccionar la que restrinja mas celdas vecinas.

Luego de seleccionar la casilla, se usara Consistencia de arco, en donde se analizaran los 20 vecinos de la casilla modificada (8 por fila + 8 por columna + 4 por subcuadrado), verificando si la solucion parcial es consistente. Esto se hara luego de cada asignacion, en caso de que no se consiga la consistencia, se hara backtrack.

Finalmente si existen casillas con un unico elemento en su dominio, se asiganara, y inmediatamente se comprabaran la consistencia de arco.

### Demostracion 

**Para esta demostracion empezamos con un estado inicial:**

D(x) = {Azul, Rojo, Verde} / x ≠ V ∧ x ≠ WA
D(WA) = {Rojo}
D(V) = {Azul}

**Aristas:**

WA → {SA, NT}
SA → {WA, NT, Q, V, NSW}
NT → {WA, SA, Q}
Q → {NT, SA, NSW}
V → {SA, NSW}
NSW → {SA, Q, V}
T → {}

**Aristas iniciales para el proceso de consistencia de arco** (aquellas que apuntan a variables ya asignadas):

(SA→WA; NT→WA; SA → V; NSW→V)

**Ejecucion de la arco consistencia**

Regla: elimina el valor z de D(X) si D(Y) = {z}

SA → WA ⇒ Elimina Rojo de D(SA)
NT → WA ⇒ Elimina Rojo de D(NT)
SA → V ⇒ Elimina Azul de D(SA)
NWS → V ⇒ Elimina Azul de D(NWS)

Como el dominio de SA ahora es unitario (SA → Verde), ahora se agregan las aristas que van desde variables no asignadas hasta SA.

NT → SA ⇒ Elimina verde de D(NT)
Q → SA ⇒ Elimina verde de D(Q)
NWS → SA ⇒ Elimina verde de D(NWS)

Como el dominio de NT y NWS ahora es unitario (NT → Azul; NWS → Rojo), ahora se agregan las aristas que van desde variables no asignadas hasta ambas variables nombradas.

Q → NT ⇒ Elimina azul de D(Q)
Q → NWS ⇒ Elimina rojo de D(Q)

Finalmente D(Q) = {}, por lo que el proceso de arco consistencia encontro la inconsistencia

### Complejidad de AC-3 en un arbol estructurado

Para empezar a hablar sobre la complejidad de la arco consistencia en un CSP el cual tiene forma de arbol empezaremos analizando el algoritmo de AC-3:

Se define la lista inicial de aristas, al ser un arbol el numero de aristas sera (n-1), siendo n el numero de nodos.

Estas aristas como maximo pueden ser encoladas otra vez un numero maximo d de veces (una encolacion por cada posible valor eliminado del nodo origen).

En este momento tenemos una complejidad de
O((n-1)d)

Luego para cada arista (Xi → Xj) se analiza la consistencia, este procedimiento asigna todos los valores posibles a Xi, con cada posible valor en Xj, eliminando aquellos que son consistentes. Este paso tiene un costo de O(d²)

Finalmente se obtiene una complejidad de **O((n-1)d³)**.








