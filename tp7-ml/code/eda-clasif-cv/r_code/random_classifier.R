agregar_columna_random <- function(df) {
  
  num_filas <- nrow(df)
  
  numeros_aleatorios <- runif(num_filas)
  
  df$prediction_prob <- numeros_aleatorios
  
  return(df)
}

random_classifier <- function(df){
  
  df$prediction_class <- ifelse(df$prediction_prob > 0.5, 1, 0)
  
  return(df)
}


nombre_archivo <- "arbolado-mendoza-dataset-validation.csv"
mi_df <- read.csv(nombre_archivo)

df_modificado <- agregar_columna_random(mi_df)

df_modificado <- agregar_columna_prediccion(df_modificado)

write.csv(df_modificado, "arbolado-mendoza-dataset-validation.csv", row.names = FALSE)
