library(dplyr)

biggerclass_classifier <- function(df, columna = "inclinacion_peligrosa") {
  
  major_class <- as.numeric(names(which.max(table(df[[columna]]))))
  
  df <- df %>% mutate(prediction_class = major_class)
  
  return(df)
  
} 

nombre_archivo <- "arbolado-mendoza-dataset-validation.csv"
mi_df <- read.csv(nombre_archivo)

nuevo_df = biggerclass_classifier(mi_df)

write.csv(nuevo_df, "arbolado-mendoza-dataset-validation-biggerclass.csv", row.names = FALSE)