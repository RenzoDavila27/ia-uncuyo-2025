## Clasificadores

### Random classifier

Se realizo un clasificador aleatorio, el cual arrojo los siguientes resultados:

| inclinacion_peligrosa | prediction_class | conteo |
| :--------: | :-------: | :--------: |
| 0 | 0  | 2796 |
| 0 | 1  | 2852 |
| 1 | 0  | 364  |
| 1 | 1  | 370  |

Este clasificador tiene un 50% de posibilidad de marcar al arbol como peligroso, esto se puede ver, ya que ambos valores son bastantes cercanos entre si, tanto en aquellos no peligrosos como en los que si lo eran.

Las metricas en esta tabla dieron de la siguiente manera:

| Accuracy | Precision | Sensitivity | Specificity |
| :--------: | :-------: | :--------: | :--------: |
| 0.496082732685678 | 0.114835505896958  | 0.50408719346049 | 0.495042492917847 |

Aqui se puede ver como la mayoria de metricas se balancean, por la naturaleza del 50% de le clasificacion, exceptuando la precision, que al haber mas arboles seguro que peligrosos en el dataset, esta es muy baja.



### Bigger class classifier

Se realizo un clasificador que asigna el valor mas repetido, el cual arrojo los siguientes resultados:

| inclinacion_peligrosa | prediction_class | conteo |
| :--------: | :-------: | :--------: |
| 0 | 0  | 5648 |
| 0 | 1  | 0 |
| 1 | 0  | 734  |
| 1 | 1  | 0  |

Este clasificador analiza que en la columna inclinacion peligrosa el valor mas comun es 0, para luego asignar este valor a prediction_class. Esto clasifico de forma correcta 5648 casos, siendo bastante bueno, pero de forma forzada.

Las metricas en esta tabla dieron de la siguiente manera:

| Accuracy | Precision | Sensitivity | Specificity |
| :--------: | :-------: | :--------: | :--------: |
| 0.88498903165152 | 0 | 0 | 1 |

Este clasificador tiene muy buenos resultados en Accuracy, debido a la mayor cantidad de arboles seguros, los cuales fueron bien predichos, pero no hay que dejarse engañar. Como se puede ver la precision y sensitivity son 0, ya que no se pudo predecir ningun arbol peligroso.


### Referencias

Los scripts del clasificador aleatorio y de clase mas grande se pueden ver en la carpeta `code/eda-clasif-cv/r-code` como `random_classifier.R` y `biggerclass_clasifier.R`. Tambien los scripts para crear la matriz de confusion y metricas se pueden ver en la misma carpeta nombrada anteriormente, como `create_confusion_matrix.R` y `metrics.R` respectivamente.

Los archivos .csv generados se pueden ver en la carpeta `data`. Aqui estaran los datasets utilizados para el clasificador random (`arbolado-mendoza-dataset-validation-random.csv`) y para el clasificar de mayor clase (`arbolado-mendoza-dataset-validation-biggerclass.csv`); ademas de sus respectivas matrices de confusion (`confusion_matrix_random.csv` y `confusion_matrix_biggerclass.csv`); y metricas correspondientes (`metrics_random.csv` y `metric_biggerclass.csv`)





