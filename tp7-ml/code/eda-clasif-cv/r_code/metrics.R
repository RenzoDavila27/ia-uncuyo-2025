library(dplyr)

accuracy <- function(confusion_matrix){
  
  total <- sum(confusion_matrix$Conteo)
  partial <- sum((confusion_matrix %>% 
                   filter(inclinacion_peligrosa == prediction_class))$Conteo)
  
  if (total == 0)
    return(0)
  else
    return(partial/total)
  
}

precision <- function(confusion_matrix){
  
  total <- sum((confusion_matrix %>% 
                 filter(prediction_class == 1))$Conteo)
  partial <- sum((confusion_matrix %>% 
                   filter(prediction_class == 1, inclinacion_peligrosa == 1))$Conteo)

  if (total == 0)
    return(0)
  else
    return(partial/total)
  
}

sensitivity <- function(confusion_matrix){
  
  total <- sum((confusion_matrix %>% 
                  filter(inclinacion_peligrosa == 1))$Conteo)
  partial <- sum((confusion_matrix %>% 
                    filter(prediction_class == 1, inclinacion_peligrosa == 1))$Conteo)

  if (total == 0)
    return(0)
  else
    return(partial/total)
  
}

specificity <- function(confusion_matrix){
  
  total <- sum((confusion_matrix %>% 
                  filter(inclinacion_peligrosa == 0))$Conteo)
  partial <- sum((confusion_matrix %>% 
                    filter(prediction_class == 0, inclinacion_peligrosa == 0))$Conteo)

  if (total == 0)
    return(0)
  else
    return(partial/total)
  
}

nombre_archivo <- "confusion_matrix_biggerclass.csv"
con_matrix <- read.csv(nombre_archivo)

metrics <- data.frame(Accuracy = c(accuracy(con_matrix)), 
                      Precision = c(precision(con_matrix)),
                      Sensitivity = c(sensitivity(con_matrix)),
                      Specificity = c(specificity(con_matrix))) 

write.csv(metrics, "metrics_biggerclass.csv", row.names = FALSE)