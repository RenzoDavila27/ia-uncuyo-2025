## Ejercicio 7

### Funcion create_folds

```r
create_folds <- function(df, k=10) {
  n <- nrow(df)
  indices <- sample(1:n)
  folds <- split(indices, cut(seq_along(indices), breaks=k, labels=FALSE))
  names(folds) <- paste0("Fold", 1:k)
  return(folds)
}
```

### Funcion cross_validation

```r
cross_validation <- function(df, folds, target_col, positive_class_value) {
  
  # --- 0. Validación de parámetros ---
  if (!target_col %in% names(df)) {
    stop(paste("La columna '", target_col, "' no existe en el dataframe."))
  }
  
  # Convertir la columna objetivo a factor para clasificación
  df[[target_col]] <- as.factor(df[[target_col]])
  
  # Verificar que la clase positiva exista en la columna
  if (!positive_class_value %in% levels(df[[target_col]])) {
     stop(paste("El valor '", positive_class_value, "' no se encuentra en la columna '", target_col, "'."))
  }

  # --- 1. Función auxiliar para división segura ---
  safe_division <- function(numerator, denominator) {
    if (denominator == 0) {
      return(NA) # Devolvemos NA si hay división por cero
    } else {
      return(numerator / denominator)
    }
  }
  
  # --- 2. Crear los folds ---
  folds_list <- create_folds(df, folds)
  
  # --- 3. Preparar el bucle ---
  all_metrics <- list()
  
  # Asignamos la clase positiva y negativa basándonos en tu parámetro
  positive_class <- as.character(positive_class_value) # Aseguramos que sea texto para comparar
  
  cat(paste("Iniciando CV de", folds, "folds.\n"))
  cat(paste("Variable objetivo:", target_col, "\n"))
  cat(paste("Clase positiva para métricas:", positive_class, "\n"))
  
  
  # --- 4. Iniciar el bucle de validación cruzada ---
  for (i in seq_len(folds)) {
    
    test_indices <- folds_list[[i]]
    train_indices <- setdiff(seq_len(nrow(df)), test_indices)
    
    train_set <- df[train_indices, ]
    test_set <- df[test_indices, ]
    
    if (nrow(test_set) == 0 || nrow(train_set) == 0) {
      next 
    }
    
    # --- 5. Entrenar el modelo ---
    # Fórmula: "target_col ~ ."
    formula <- formula(inclinacion_peligrosa~altura+
                         circ_tronco_cm+
                         lat+long+
                         seccion+
                         especie)
    
    model <- rpart(formula, data = train_set, method = "class")
    
    # --- 6. Predecir y Calcular Métricas ---
    predictions <- predict(model, newdata = test_set, type = "class")
    actuals <- test_set[[target_col]]
    
    # Asegurar niveles
    predictions <- factor(predictions, levels = levels(actuals))
    
    # Calcular Métricas (TP, TN, FP, FN)
    # Comparamos contra el valor "positive_class" que nos diste
    TP <- sum(actuals == positive_class & predictions == positive_class)
    TN <- sum(actuals != positive_class & predictions != positive_class)
    FP <- sum(actuals != positive_class & predictions == positive_class)
    FN <- sum(actuals == positive_class & predictions != positive_class)
    
    # Calcular métricas
    accuracy1 <- safe_division(TP + TN, TP + TN + FP + FN)
    precision1 <- safe_division(TP, TP + FP)
    sensitivity1 <- safe_division(TP, TP + FN) # Recall
    specificity1 <- safe_division(TN, TN + FP)
    
    all_metrics[[i]] <- data.frame(
      Fold = i,
      Accuracy = accuracy1,
      Precision = precision1,
      Sensitivity = sensitivity1,
      Specificity = specificity1
    )
  }
  
  # --- 7. Calcular resultados finales ---
  metrics_df <- do.call(rbind, all_metrics)
  
  mean_metrics <- sapply(metrics_df[, -1], mean, na.rm = TRUE)
  sd_metrics <- sapply(metrics_df[, -1], sd, na.rm = TRUE)
  
  result <- list(
    media = mean_metrics,
    desviacion_estandar = sd_metrics,
    metricas_por_fold = metrics_df
  )
  
  return(result)
}
```

A la hora de ejecutar esta funcion, se hicieron algunos cambios en el dataset, aquellos datos con especias poco repetidas (Algarrobo, Arabia, Maiten y Arbol del cielo) se convirtieron en categoria Others, para que el modelo en caso de encontrar uno de estos en el fold de test sepa que hacer. Lo mismo se hizo con la seccion San Agustin

### Metricas obtenidas

Metricas en la media:

| Accuracy | Precision | Sensitivity | Specificity |
| :--------: | :-------: | :--------: | :--------: |
| 0.888562475518997 | 0 | 0 | 1 |

Metricas en la desviacion estandar:

| Accuracy | Precision | Sensitivity | Specificity |
| :--------: | :-------: | :--------: | :--------: |
| 0.00397420844894227 | 0 | 0 | 0 |

Las tablas tienen esta forma tan peculiar, porque el modelo descubrio que la mejor forma de clasificar es clasificar todo como "no peligroso", ya que el dataset esta bastante desbalanceado

