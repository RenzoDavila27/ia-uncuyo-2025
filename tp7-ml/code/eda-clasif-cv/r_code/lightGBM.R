# --- 1. Cargar Librerías ---
# (Asegúrate de tenerlas instaladas)
library(dplyr)
library(lightgbm)
library(readr)    # Para el script de limpieza
library(forcats)  # Para el script de limpieza
library(tidyr)    # Para el script de limpieza

# --- 2. Función de Limpieza (La que acabamos de crear) ---

limpiar_dataframe_arboles <- function(df_bruto) {
  
  cat("--- Iniciando limpieza (v2 con recodificación ordinal) ---\n")
  
  df_limpio <- df_bruto %>%
    
    # 1. Selección de Columnas
    # (Ya no eliminamos diametro_tronco ni altura)
    select(
      -id,
      -ultima_modificacion,
      -seccion
    ) %>%
    
    # 2. Transformación de Columnas
    mutate(
      
      # --- CAMBIO: Convertir diametro_tronco a número ---
      diametro_tronco = recode(diametro_tronco,
                               "Chico" = 30,
                               "Mediano" = 50,
                               "Grande" = 70,
                               .default = NA_real_), # .default=NA si no coincide
      
      # --- CAMBIO: Convertir altura a número ---
      altura = recode(altura,
                      "Muy bajo (1 - 2 mts)" = 1.5,
                      "Bajo (2 - 4 mts)" = 3,
                      "Medio (4 - 8 mts)" = 6,
                      "Alto (> 8 mts)" = 9,
                      .default = NA_real_),
      
      # --- Limpieza de factores (igual que antes) ---
      especie = fct_lump_min(especie, min = 10, other_level = "Especie_Otra"),
      nombre_seccion = fct_lump_min(nombre_seccion, min = 10, other_level = "Seccion_Otra")
      
    ) %>%
    
    # 3. Manejo de NAs y Objetivo (igual que antes)
    drop_na(inclinacion_peligrosa) %>%
    drop_na() %>% # Esto ahora también elimina filas donde el recode falló
    mutate(
      inclinacion_peligrosa = as.factor(inclinacion_peligrosa)
    )
  
  cat("--- Limpieza (v2) finalizada ---\n")
  return(df_limpio)
}

# --- 3. Función create_folds (Tu función) ---

create_folds <- function(df, folds){
  # ... (Pega tu función create_folds aquí, no la modifico) ...
  if (!is.data.frame(df)) stop("df debe ser un data.frame")
  if (!is.numeric(folds) || length(folds) != 1) stop("folds debe ser un número entero mayor o igual a 2")
  folds <- as.integer(folds)
  if (folds < 2) stop("folds debe ser >= 2")
  
  n <- nrow(df)
  result <- setNames(vector("list", folds), paste0("Fold", seq_len(folds)))
  if (n == 0) return(result)
  if (folds > n) warning("Más folds que registros: algunas particiones quedarán vacías")
  
  shuffled <- df %>%
    mutate(.row = row_number()) %>%
    slice_sample(n = n)
  shuffled$Fold <- rep(seq_len(folds), length.out = n)
  
  grouped <- shuffled %>%
    group_by(Fold) %>%
    summarise(rows = list(.row), .groups = "drop")
  
  for (i in seq_len(folds)){
    row_entry <- grouped$rows[grouped$Fold == i]
    if (length(row_entry) == 0) {
      result[[i]] <- integer(0)
    } else {
      result[[i]] <- as.integer(row_entry[[1]])
    }
  }
  return(result)
}


# --- 4. Función de Cross-Validation para LightGBM ---

run_lgbm_cv <- function(df, k_folds, target_col, positive_class) {
  
  # --- 4.1. Preparación de Datos (Crucial) ---
  # LightGBM necesita que TODO sea numérico.
  
  # 1. Guardar la etiqueta (Y) como 0 y 1 numérico
  y_data <- as.numeric(df[[target_col]] == positive_class)
  
  # 2. Guardar nombres de columnas categóricas
  # (LightGBM es más eficiente si le decimos cuáles son)
  categorical_features <- df %>%
    select(-all_of(target_col)) %>% # Quita el objetivo
    select(where(is.factor) | where(is.character)) %>% # Selecciona factores/texto
    names()
  
  cat("Columnas categóricas detectadas:", paste(categorical_features, collapse=", "), "\n")
  
  # 3. Convertir predictores (X) a una matriz numérica
  # data.matrix() convierte factores a números (1, 2, 3...) automáticamente
  x_data <- df %>%
    select(-all_of(target_col)) %>%
    data.matrix()
  
  # Definir Parámetros de LightGBM ---
  lgb_params <- list(
    objective = "binary",        # Clasificación binaria
    metric = "auc",              # Optimizar para AUC
    is_unbalance = TRUE,         # <-- ¡Maneja el desbalance!
    nrounds = 200,               # 200 árboles (puedes subirlo)
    learning_rate = 0.05,
    verbose = -1                 # -1 para silenciar (0 imprime warnings)
  )
  
 
  folds_list <- create_folds(df, k_folds)
  all_metrics <- list()
  

  safe_division <- function(num, den) { ifelse(den == 0, NA, num / den) }
  
  cat(paste("Iniciando CV de", k_folds, "folds...\n"))
  
  for (i in seq_len(k_folds)) {
    
    test_indices <- folds_list[[i]]
    train_indices <- setdiff(seq_len(nrow(df)), test_indices)
    
    x_train <- x_data[train_indices, ]
    y_train <- y_data[train_indices]
    
    x_test <- x_data[test_indices, ]
    y_test <- y_data[test_indices]
    

    dtrain <- lgb.Dataset(
      data = x_train, 
      label = y_train,
      categorical_feature = categorical_features # <-- Le decimos cuáles son categóricas
    )
    
    # Entrenar el modelo
    lgb_model <- lgb.train(
      params = lgb_params,
      data = dtrain
    )
    
    prob_preds <- predict(lgb_model, x_test)
    
    class_preds <- ifelse(prob_preds > 0.5, 1, 0)
    
    TP <- sum(y_test == 1 & class_preds == 1)
    TN <- sum(y_test == 0 & class_preds == 0)
    FP <- sum(y_test == 0 & class_preds == 1)
    FN <- sum(y_test == 1 & class_preds == 0)
    
    if (!require(pROC)) { install.packages("pROC"); library(pROC) }
    
    auc_val <- as.numeric(auc(y_test, prob_preds, quiet = TRUE))
    
    all_metrics[[i]] <- data.frame(
      Fold = i,
      Accuracy    = safe_division(TP + TN, TP + TN + FP + FN),
      Precision   = safe_division(TP, TP + FP),
      Sensitivity = safe_division(TP, TP + FN), # Recall
      Specificity = safe_division(TN, TN + FP),
      AUC         = auc_val
    )
  }
  
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


seeds_a_probar <- c(53154889, 20231681, 88484613, 02230162, 49685100)

lista_de_resultados <- list()


mi_df_original <- read_csv("arbolado-mendoza-dataset-train.csv")


for (seed_actual in seeds_a_probar) {
  
  set.seed(seed_actual)
  
  mi_df_limpio <- limpiar_dataframe_arboles(mi_df_original)
  
  resultados_run <- run_lgbm_cv(
    df = mi_df_limpio,
    k_folds = 10,
    target_col = "inclinacion_peligrosa",
    positive_class = "1"
  )
  
  resultados_df <- data.frame(t(resultados_run$media))
  resultados_df$seed <- seed_actual

  lista_de_resultados[[as.character(seed_actual)]] <- resultados_df

  resultados_finales_df <- do.call(rbind, lista_de_resultados)
  
}
  
resultados_finales_df <- resultados_finales_df %>%
  select(seed, everything())

write.csv(resultados_finales_df, "resultados_cv_runs.csv", row.names = FALSE)