### Esto es una primera version, pero no obtiene los resultados deseados en kaggle

## 1) Proceso de Preprocesamiento de Datos

Sí, se realizó un preprocesamiento intensivo en dos fases:

### A. Limpieza de Datos
* **Variables Eliminadas:** Se descartaron columnas de ID (`id`, `seccion`), metadatos (`ultima_modificacion`) y variables redundantes (`diametro_tronco`, ya que `circ_tronco_cm` aporta la misma información de forma numérica).
* **Agrupación de Categorías:** Se utilizó `fct_lump_min(min = 10)` para agrupar categorías poco frecuentes (menos de 10 apariciones) en las variables `especie`, `altura` y `nombre_seccion`. Esto previene errores de validación y mejora la generalización.

### B. Ingeniería de Atributos
Se crearon 3 nuevas variables (features) para mejorar la predicción:
* **`zona_cluster` (Categórica):** Agrupa las coordenadas (`lat`, `long`) en 5 zonas geográficas mediante K-Means.
* **`densidad_arbol` (Numérica):** Un ratio calculado como `circ_tronco_cm / area_seccion`.
* **`especie_seccion` (Categórica):** Una interacción que combina `especie` y `nombre_seccion`.

*No se realizó normalización (escalado 0-1) ya que el modelo (LightGBM) no lo requiere.*

---

## 2) Resultados Obtenidos

Se utilizó Validación Cruzada de 10-Folds, repetida 5 veces con distintas semillas aleatorias. Los resultados (media y desv. estándar) en los conjuntos de validación fueron:

| Métrica | Media | Desv. Estándar |
| :--- | :---: | :---: |
| **AUC** | **0.7710** | **0.0008** |
| Accuracy | 0.7237 | 0.0015 |
| Precision | 0.2404 | 0.0018 |
| Sensitivity | 0.6846 | 0.0043 |
| Specificity | 0.7286 | 0.0011 |

La métrica principal, **AUC**, es de **0.7710**, indicando una buena capacidad de discriminación, lo cual es muy positivo dado el desbalance de los datos. La alta **Sensibilidad** (0.6846) muestra que el modelo es efectivo en detectar la clase positiva (inclinación peligrosa).

---

## 3) Descripción del Algoritmo Propuesto

El algoritmo utilizado fue **LightGBM (Light Gradient Boosting Machine)**.

Es un modelo de *Gradient Boosting* que construye árboles de decisión de forma secuencial. Cada nuevo árbol se entrena para corregir los errores cometidos por los árboles anteriores, enfocándose progresivamente en los casos difíciles.

Se eligió por dos motivos clave:

1.  **Manejo del Desbalance:** Se configuró con `is_unbalance = TRUE`. Esto penaliza más al modelo por errores en la clase minoritaria ("peligrosa"), forzándolo a aprender a detectarla (lo que explica la alta sensibilidad)

2.  **Rendimiento y Eficiencia:** Se optimizó para maximizar el **AUC** (`metric = 'auc'`) y se le informó cuáles variables eran categóricas (`especie`, `zona_cluster`, etc.), permitiéndole manejarlas de forma nativa sin necesidad de *one-hot encoding*.
