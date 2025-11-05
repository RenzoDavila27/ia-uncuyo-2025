import csv
import os
import random

# --- Configuración ---
ARCHIVO_ENTRADA = 'data/arbolado-mendoza-dataset-train.csv' # El archivo que creamos antes
ARCHIVO_SALIDA = 'data/arbolado-mendoza-dataset-circ_tronco_cm-train.csv' # El nuevo archivo a crear

COLUMNA_FUENTE = 'circ_tronco_cm'
COLUMNA_NUEVA = 'circ_tronco_cm_cat'

def categorizar_circunferencia(circ_str):
    """
    Aplica la lógica de categorización a un valor de circunferencia.
    
    La lógica es:
    - (0, 50]   : 'bajo'
    - (50, 150] : 'medio'
    - (150, 200]: 'alto'
    - (200, inf): 'muy alto'
    """
    try:
        # Convertir el valor de texto a número (float)
        circ = float(circ_str)
        
        # El if/elif/else se evalúa en orden
        if circ <= 50:
            return 'bajo'
        elif circ <= 150: # Esto solo se ejecuta si es > 50
            return 'medio'
        elif circ <= 200: # Esto solo se ejecuta si es > 150
            return 'alto'
        else: # Esto solo se ejecuta si es > 200
            return 'muy alto'
            
    except (ValueError, TypeError):
        # Maneja casos donde el valor no sea un número (ej. "N/A" o celda vacía)
        return 'invalido'

def agregar_columna_categoria(archivo_in, archivo_out, col_fuente, col_nueva):
    """
    Lee el archivo de entrada, agrega la nueva columna y escribe el archivo de salida.
    """
    print(f"Procesando archivo '{archivo_in}'...")
    filas_procesadas = 0
    
    try:
        with open(archivo_in, mode='r', newline='', encoding='utf-8') as infile:
            # Abrir el archivo de salida para escribir
            with open(archivo_out, mode='w', newline='', encoding='utf-8') as outfile:
                
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                
                # --- 1. Procesar el Encabezado ---
                header = next(reader)
                
                # Encontrar el índice de la columna que necesitamos leer
                try:
                    indice_columna_fuente = header.index(col_fuente)
                except ValueError:
                    print(f"Error fatal: No se encontró la columna '{col_fuente}' en el archivo.")
                    return

                # Escribir el nuevo encabezado en el archivo de salida
                writer.writerow(header + [col_nueva])
                
                # --- 2. Procesar las Filas de Datos ---
                for fila in reader:
                    # Obtener el valor de la circunferencia (como string)
                    valor_circ = fila[indice_columna_fuente]
                    
                    # Obtener la nueva categoría llamando a la función
                    categoria = categorizar_circunferencia(valor_circ)
                    
                    # Escribir la fila original + la nueva categoría
                    writer.writerow(fila + [categoria])
                    filas_procesadas += 1

        print(f"¡Proceso completado!")
        print(f"Se ha creado el archivo '{archivo_out}' con {filas_procesadas} filas de datos.")

    except FileNotFoundError:
        print(f"Error fatal: El archivo de entrada '{archivo_in}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# --- Ejecución del script ---
if __name__ == "__main__":
    
    # 2. Ejecutar la función principal de procesamiento
    agregar_columna_categoria(ARCHIVO_ENTRADA, ARCHIVO_SALIDA, COLUMNA_FUENTE, COLUMNA_NUEVA)