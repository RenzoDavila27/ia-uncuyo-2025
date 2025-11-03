## Ejercicio 1

**El tamaño de la muestra n es extremadamente grande, y el número de predictores p es pequeño:**


Cuando el tamaño de la muestra n es extremadamente grande y el número de predictores p es pequeño, un método de aprendizaje de maquinas flexible es generalmente mejor. La desventaja de los modelos flexibles es la tendencia al sobreajuste (overfitting), esto ocurre cuando el modelo aprende el ruido aleatorio de los datos en lugar de la señal verdadera. Sin embargo, una muestra muy grande mitiga este riesgo, ya que la existencia de muchos datos "promedia" el ruido y estabiliza el ajuste del modelo, reduciendo su varianza. Finalmente, podemos aprovechar la mayor fortaleza de un modelo flexible: su bajo sesgo. Esta caracteristica permite al modelo capturar la verdadera relación entre los predictores y la respuesta. Un modelo inflexible, por el contrario, posee un sesgo inherente que le impediría modelar esta complejidad, sin importar la cantidad de datos disponibles.

**El número de predictores p es extremadamente grande, y el número de observaciones n es pequeño:**

Cuando el número de predictores p es extremadamente grande y el número de observaciones n es pequeño, un método inflexible funcionará mejor. La razón de la eleccion es que los métodos flexibles corren un riesgo extremadamente alto de sobreajuste en esta situación. Con tantos predictores y tan pocas observaciones, un modelo flexible tiene la libertad de encontrar patrones complejos en los datos de entrenamiento que en realidad son solo ruido aleatorio, no una señal verdadera. Esto provoca que la varianza del modelo sea muy alta, aunque el modelo se ajuste perfectamente a los datos de entrenamiento, este tendrá un rendimiento terrible en datos nuevos. Por el contrario, un método inflexible restringe drásticamente el modelo, lo que reduce la varianza de forma significativa. Aunque esta restricción introduce algo de sesgo (el modelo no puede capturar una relación muy compleja), este ligero aumento en el sesgo es un precio pequeño a pagar por la drástica reducción de la varianza.

**La relación entre los predictores y la variable dependiente es altamente no lineal:**

En este caso, la mejor opcion sera un metodo de aprendizaje de maquina flexible, ya que este podra capturar de mejor manera la curva generada por los datos. Estos modelos sufren el sobreajuste, pero es poco el precio a pagar a comparacion del aumento del sesgo en un modelo poco flexible.

**La varianza de los términos de error, σ2 = Var(ϵ), es extremadamente alta:**

En este escenario, un metodo de aprendizaje de maquina inflexible sera el mas adecuado, ya que una varianza de error extremadamente alta significa que los datos son muy ruidosos. La eleccion se debe a que un modelo inflexible es más restrictivo. No puede "doblarse" para capturar los puntos de datos ruidosos e individuales. Esta restricción lo obliga a encontrar solo la tendencia más simple y general, ignorando el ruido aleatorio. En un escenario de alto ruido, esta es una ventaja que resulta en una menor varianza del modelo y, en última instancia, un mejor error de prueba.

## Ejercicio 2

**Se recopila un conjunto de datos sobre las 500 empresas más importantes de Estados Unidos. Para cada una de las empresas se registran las ganancias, el número de empleados, la industria y el salario del director ejecutivo. Se tiene interés en comprender qué factores afectan el salario de los directores ejecutivos.**

* N = 500. "Se recopila un ***conjunto de datos sobre las 500 empresas*** más importantes de Estados Unidos."
* P = 3. "Para cada una de las empresas se registran las ***ganancias***, el ***número de empleados***, la ***industria*** y el salario del director ejecutivo."
* Problema de regresion. "Se tiene interés en comprender qué factores afectan ***el salario*** de los directores ejecutivos."
* Se busca inferir. "Se ***tiene interés en comprender*** qué factores afectan el salario de los directores ejecutivos."

**Se está considerando lanzar un nuevo producto y se desea saber si será un éxito o un fracaso. Se recolectan datos de 20 productos similares que fueron lanzados previamente. Para cada producto se ha registrado si fue un éxito o un fracaso, el precio cobrado por el producto, el presupuesto de marketing, el precio de la competencia, y otras diez variables**

* N = 20. "Se ***recolectan datos de 20 productos*** similares que fueron lanzados previamente"
* P = 13. "Para cada producto se ha registrado si fue un éxito o un fracaso, el ***precio cobrado por el producto***, el ***presupuesto de marketing***, el ***precio de la competencia***, y ***otras diez variables***"
* Problema de clasificacion. "Se está considerando lanzar un nuevo producto y se desea saber si será un ***éxito o un fracaso***."
* Se busca predecir. "Se está considerando lanzar un nuevo producto y ***se desea saber si será*** un éxito o un fracaso."

**Se tiene interes en predecir el % de cambio en el tipo de cambio USD/Euro en relación a los cambios semanales en los mercados de valores mundiales. Para eso se recolectan datos semanalmente durante todo el 2021. Para cada semana se registran el % de cambio de USD/Euro, el % de cambio en el mercado estadounidense, el % de cambio en el mercado británico, y el % de cambio en el mercado alemán.**

* N = 365 / 7 ≈ 52. "Para eso ***se recolectan datos semanalmente durante todo el 2021***."
* P = 3. "Para cada semana se registran el % de cambio de USD/Euro, el ***% de cambio en el mercado estadounidense***, el ***% de cambio en el mercado británico***, y el ***% de cambio en el mercado alemán***."
* Problema de regresion. "Se tiene interes en predecir ***el % de cambio en el tipo de cambio USD/Euro en relación a los cambios semanales en los mercados de valores mundiales***"
* Se busca predecir. "***Se tiene interes en predecir*** el % de cambio en el tipo de cambio USD/Euro en relación a los cambios semanales en los mercados de valores mundiales"

## Ejercicio 3

### Metodos flexibles

* Ventaja: Potencialmente una mayor precisión en la predicción. Si la relación real es altamente no lineal, un método flexible será capaz de modelarla con mayor precisión.

* Desventaja: Baja interpretabilidad y sobreajuste. Pueden volverse tan complicados que es difícil entender cómo un predictor individual está asociado con la respuesta. Tambien existe un peligro significativo de que el modelo se ajuste al ruido de los datos en lugar de a la señal verdadera.

* Debido a estas caracteristicas nombradas, los metodos flexibles seran la mejor eleccion si el objetivo principal es la predicción, siempre teniendo en cuenta el sobreajuste

### Metodos poco flexibles

* Ventajas: Interpretabilidad. Son mucho más fáciles de interpretar porque la relación entre los predictores y la respuesta es simple y está claramente definida

* Desventaja: Si la verdadera forma de f no es lineal, un modelo inflexible tendrá un mal desempeño en la predicción porque no podrá capturar la relación real.

* Debido a estas caracteristicas nombradas, los metodos poco flexibles seran la mejor eleccion si el objetivo principal es la inferencia, ya que es mucho más interpretable.

## Ejercicio 4

### Diferencias entre Enfoques Paramétricos y No Paramétricos

* **Enfoque Paramétrico**: Este es un enfoque de dos pasos basado en un modelo.
    1.  Primero, se **hace una suposición sobre la forma funcional** o la forma de $f$. Un ejemplo común es asumir que $f$ es lineal, como en un modelo lineal: $f(X) = \beta_0 + \beta_1X_1 + ... + \beta_pX_p$.
    2.  Segundo, después de seleccionar un modelo, se utiliza un procedimiento (como los mínimos cuadrados) para **ajustar o entrenar el modelo** usando los datos de entrenamiento para estimar los parámetros.

* **Enfoque No Paramétrico**: Este enfoque **no hace suposiciones explícitas** sobre la forma funcional de $f$. En lugar de eso, busca una estimación de $f$ que se acerque lo más posible a los puntos de datos sin ser "demasiado brusca o variable".

### Ventajas y Desventajas de un Enfoque Paramétrico

**Ventajas (sobre un enfoque no paramétrico)**

1.  **Simplicidad**: El enfoque paramétrico simplifica el problema. En lugar de estimar una función $f$ completamente arbitraria y de alta dimensión, el problema se reduce a estimar un pequeño conjunto de parámetros (como $\beta_0, \beta_1, ...$).
2.  **Eficiencia de Datos**: Estimar este pequeño conjunto de parámetros es "generalmente mucho más fácil". Como resultado, los métodos no paramétricos suelen requerir un "número muy grande de observaciones" para obtener una estimación precisa, mientras que los métodos paramétricos son más eficientes con menos datos

### Desventajas (en comparación con un enfoque no paramétrico)

1. **Riesgo de Sesgo del Modelo**: La desventaja más significativa es que el modelo elegido (la forma funcional asumida) "generalmente no coincidirá con la verdadera forma desconocida de $f$". Si el modelo elegido está "demasiado lejos de la verdadera $f$", la estimación será pobre, sin importar cuántos datos se utilicen.
2.  **Riesgo de Sobreajuste (Overfitting)**: Si bien los modelos paramétricos son a menudo más simples, se pueden elegir modelos paramétricos más "flexibles" (modelos más complejos que requieren estimar un mayor número de parámetros). Estos modelos más complejos pueden llevar al **sobreajuste**, lo que significa que "siguen los errores, o el ruido, demasiado de cerca".

## Ejercicio 5

#### Distancia euclidiana entre dos puntos P(a,b,c) y Q(x,y,z)

Distancia = sqrt((x-a)²+(y-b)²+(z-c)²)

* Obs 1: sqrt((0)²+(3)²+(0)²) = 3
* Obs 2: sqrt((2)²+(0)²+(0)²) = 2
* Obs 3: sqrt((0)²+(1)²+(3)²) ≈ 3.16228
* Obs 4: sqrt((0)²+(1)²+(2)²) ≈ 2.23607
* Obs 5: sqrt((-1)²+(0)²+(1)²) ≈ 1.41421
* Obs 6: sqrt((1)²+(1)²+(1)²) ≈ 1.73205

#### Cuál es la predicción con K = 1? Justifique.

Una vez que tenemos K = 1, buscamos los K vecinos mas cercanos a nuestro valor a predecir, en este caso la Observacion 5, con una distancia de 1.41421. Luego se seleccionara de todos los vecinos elegidos, el valor mas Y repetido, en este caso solo tenemos un vecino, por lo que el valor sera el mismo que la observacion 5. 

El valor $Y$ para $X_1 = X_2 = X_3 = 0$ predecido por el modelo es **Verde**

#### Cuál es la predicción con K = 3? Justifique.

Una vez que tenemos K = 3, buscamos los K vecinos mas cercanos a nuestro valor a predecir, en este caso la Observacion 5, Observacion 6 y Observacion 2 con una distancia de 1.41421, 1.73205 y 2 respectivamente. Luego se seleccionara de todos los vecinos elegidos, el valor Y mas repetido, en este caso tenemos los valores Verde (Obs 5) y Rojo (Obs 2 y Obs 6), por lo que el valor Y sera el valor de la Obs 2 y Obs 6.

El valor $Y$ para $X_1 = X_2 = X_3 = 0$ predecido por el modelo es **Rojo**

#### Si el límite de decisión de Bayes en este problema es altamente no lineal, ¿se espera que el mejor valor para K sea grande o pequeño? ¿Por qué?

La mejor decision en el escenario propuesto es un K pequeño, esto se debe a que un valor de estas caracteristicas (como K=1) crea un modelo altamente flexible. Si el verdadero límite de decisión de Bayes es "altamente no lineal y complejo", se necesita un modelo con bajo sesgo que sea capaz de adaptarse a esa forma complicada. Un K pequeño logra esto porque basa su predicción únicamente en los vecinos más inmediatos, permitiendo que el límite de decisión estimado sea muy irregular y siga de cerca las curvas y giros locales de los datos de entrenamiento. Aunque esta flexibilidad extrema conlleva el riesgo de una alta varianza (lo que significa que el modelo podría sobreajustarse al ruido de los datos), es un costo necesario. Si usáramos un K grande, el modelo sería demasiado simple (alto sesgo) y fallaría por completo en capturar la verdadera forma no lineal del límite de Bayes.