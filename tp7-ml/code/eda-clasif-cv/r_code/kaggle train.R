library(dplyr)
library(forcats)
library(readr)
library(lightgbm)

limpiar_dataframe_kaggle <- function(df_bruto) {
  
  cat("--- Iniciando limpieza (v2 con recodificación ordinal - Kaggle Test) ---\n")
  
  df_limpio <- df_bruto %>%
    
    # 1. Selección de Columnas
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
    )
  
  # --- NO USAMOS drop_na() ---
  
  cat("--- Limpieza (Kaggle Test v2) finalizada ---\n")
  return(df_limpio)
}

ingenieria_atributos_kaggle <- function(df_limpio, k_clusters = 5) {
  
  cat("--- Iniciando ingeniería de atributos (v4 con ratio altura - Kaggle Test) ---\n")
  
  # --- 1. Clustering Geográfico (K-Means) ---
  df_limpio$zona_cluster <- NA 
  idx_non_na <- which(!is.na(df_limpio$long) & !is.na(df_limpio$lat))
  coords_data <- df_limpio[idx_non_na, c("long", "lat")]
  num_distinct_points <- nrow(unique(coords_data))
  
  cat(paste("K-Means: Encontrados", num_distinct_points, "puntos de coordenadas únicos.\n"))
  
  if (num_distinct_points >= k_clusters) {
    cat(paste("Ejecutando K-Means con k =", k_clusters, "\n"))
    coords_scaled <- scale(coords_data)
    set.seed(123) 
    kmeans_model <- kmeans(coords_scaled, centers = k_clusters, nstart = 25)
    df_limpio$zona_cluster[idx_non_na] <- kmeans_model$cluster
  } else {
    cat(paste("K-Means: No se ejecutó. Se requieren al menos", k_clusters, "puntos únicos.\n"))
  }
  
  # --- 2. Ratios e Interacciones ---
  df_enriquecido <- df_limpio %>%
    mutate(
      # Ratio Numérico (existente)
      densidad_arbol = ifelse(area_seccion == 0 | is.na(area_seccion), 
                              NA, 
                              circ_tronco_cm / area_seccion),
      
      # --- NUEVA CARACTERÍSTICA ---
      # Ratio de Robustez (Circunferencia / Altura)
      circ_altura_ratio = ifelse(is.na(altura) | altura == 0, 
                                 NA, 
                                 circ_tronco_cm / (altura + 0.01)),
      
      # Interacción Categórica (existente)
      especie_seccion = paste(especie, nombre_seccion, sep = "_"),
      
      # Conversión a Factor (existente)
      zona_cluster = as.factor(zona_cluster),
      especie_seccion = as.factor(especie_seccion)
    ) %>%
    mutate(
      # Limpieza de Interacción (existente)
      especie_seccion = fct_lump_min(especie_seccion, min = 10, other_level = "Interaccion_Otra")
    )
  
  return(df_enriquecido)
}

# Cargar y preparar datos de ENTRENAMIENTO
train_original <- read_csv("arbolado-mza-dataset.csv") # Tu archivo de entrenamiento
train_limpio <- limpiar_dataframe_arboles(train_original)
train_enriquecido <- ingenieria_atributos(train_limpio)

# Preparar datos para LightGBM
target_col <- "inclinacion_peligrosa"
positive_class <- "1"

y_data <- as.numeric(train_enriquecido[[target_col]] == positive_class)
categorical_features <- train_enriquecido %>%
  select(-all_of(target_col)) %>%
  select(where(is.factor) | where(is.character)) %>%
  names()
x_data <- train_enriquecido %>%
  select(-all_of(target_col)) %>%
  data.matrix()

dtrain_final <- lgb.Dataset(
  data = x_data, 
  label = y_data,
  categorical_feature = categorical_features
)

# Parámetros (usa los que mejor te funcionaron)
lgb_params <- list(
  objective = "binary", metric = "auc", is_unbalance = TRUE,
  nrounds = 100, learning_rate = 0.05, verbose = -1
)

# Entrenar el modelo
modelo_final <- lgb.train(
  params = lgb_params,
  data = dtrain_final
)

cat("--- Modelo final entrenado ---\n")

# --- 3. Preparar Datos de Kaggle (test.csv) ---
cat("--- Procesando test.csv ---\n")

# Cargar y preparar datos de PRUEBA (Kaggle)
test_original <- read_csv("arbolado-mza-dataset-test.csv") # El archivo de Kaggle
test_limpio <- limpiar_dataframe_kaggle(test_original)
test_enriquecido <- ingenieria_atributos_kaggle(test_limpio)

# Convertir a matriz numérica
test_matrix <- test_enriquecido %>%
  # (Asegurarse de que las columnas coincidan con x_data)
  data.matrix() 

# --- 4. Hacer Predicciones ---
cat("--- Generando predicciones ---\n")

# Predecir PROBABILIDADES
predicciones_prob <- predict(modelo_final, test_matrix)

# Convertir a clases (0 o 1)
# (Revisa las reglas, a veces Kaggle pide la probabilidad)
predicciones_clase <- ifelse(predicciones_prob > 0.5, 1, 0)

# --- 5. Crear Archivo de Subida ---
submission_df <- data.frame(
  id = test_original$id,  # Usa el 'id' original del test.csv
  inclinacion_peligrosa = predicciones_clase
)

# Guardar
write.csv(submission_df, "submission.csv", row.names = FALSE)

cat("--- ¡Archivo 'submission.csv' creado y listo para subir! ---\n")