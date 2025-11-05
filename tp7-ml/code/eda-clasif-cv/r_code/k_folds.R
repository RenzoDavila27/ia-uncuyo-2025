library(dplyr)
library(rpart)
library(forcats)

create_folds <- function(df, k=10) {
  n <- nrow(df)
  indices <- sample(1:n)  # mezcla aleatoria
  folds <- split(indices, cut(seq_along(indices), breaks=k, labels=FALSE))
  names(folds) <- paste0("Fold", 1:k)
  return(folds)
}

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

nombre_archivo <- "arbolado-mendoza-dataset-train.csv"
mi_df <- read.csv(nombre_archivo)

mi_df$inclinacion_peligrosa <- factor(mi_df$inclinacion_peligrosa)
mi_df <- mi_df %>%
  select(-ultima_modificacion)

mi_df <- mi_df %>%
  mutate(
    especie = fct_lump_n(especie, n = 28)
  )

mi_df <- mi_df %>%
  mutate(
    # Mantiene especies que aparezcan al menos 10 veces
    nombre_seccion = fct_lump_min(nombre_seccion, min = 10) 
  )

resultados_cv <- cross_validation(
  df = mi_df,
  folds = 10,
  target_col = "inclinacion_peligrosa", # 1er cambio: tu columna
  positive_class_value = "1"             # 2do cambio: tu clase positiva (OJO: "1" como texto, porque es un factor)
)


cat("\n--- Resultados de la Validación Cruzada ---\n")
print(resultados_cv$media)
print(resultados_cv$desviacion_estandar)

write.csv(resultados_cv$media, "resultados_cv_media.csv")
write.csv(resultados_cv$desviacion_estandar, "resultados_cv_desvest.csv")
