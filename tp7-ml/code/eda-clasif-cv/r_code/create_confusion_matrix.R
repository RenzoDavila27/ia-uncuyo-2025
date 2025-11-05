library(dplyr)

create_matrix <- function(df) {
  
  confusion_matrix <- df %>%
    count(inclinacion_peligrosa, prediction_class, name = "Conteo")
  
  print(confusion_matrix)
  
  return(confusion_matrix)
    
}

nombre_archivo <- "arbolado-mendoza-dataset-validation.csv"
mi_df <- read.csv(nombre_archivo)

matrix_confusion = create_matrix(mi_df)

write.csv(matrix_confusion, "confusion_matrix.csv", row.names = FALSE)