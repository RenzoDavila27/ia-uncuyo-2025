import csv
import random
import os

def dividir_csv_aleatoriamente(archivo_entrada, archivo_salida_20, archivo_salida_80):
    """
    Lee un archivo CSV, baraja aleatoriamente sus filas (excepto el encabezado)
    y las divide en dos nuevos archivos (20% y 80%).
    """
    
    filas_datos = []
    encabezado = []

    # --- 1. Leer el archivo CSV de entrada ---
    try:
        with open(archivo_entrada, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            
            # Leer y guardar el encabezado (la primera fila)
            encabezado = next(reader)
            
            # Leer y guardar todas las demás filas de datos
            for row in reader:
                filas_datos.append(row)
        
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no se encontró.")
        return
    except StopIteration:
        print("Error: El archivo CSV está vacío o solo contiene un encabezado.")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return

    if not filas_datos:
        print("No se encontraron filas de datos (después del encabezado). No se crearán archivos.")
        return

    # --- 2. Barajar aleatoriamente las filas de datos ---
    random.shuffle(filas_datos)

    # --- 3. Calcular el punto de división ---
    total_filas = len(filas_datos)
    punto_division = int(total_filas * 0.20)

    # --- 4. Dividir los datos en dos grupos ---
    grupo_20_porciento = filas_datos[:punto_division]
    grupo_80_porciento = filas_datos[punto_division:]

    # --- 5. Escribir el archivo del 20% ---
    try:
        with open(archivo_salida_20, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(encabezado)          # Escribir el encabezado
            writer.writerows(grupo_20_porciento) # Escribir las filas de datos
    except IOError as e:
        print(f"Error al escribir '{archivo_salida_20}': {e}")
        return

    # --- 6. Escribir el archivo del 80% ---
    try:
        with open(archivo_salida_80, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(encabezado)          # Escribir el encabezado
            writer.writerows(grupo_80_porciento) # Escribir las filas de datos
    except IOError as e:
        print(f"Error al escribir '{archivo_salida_80}': {e}")
        return

    # --- 7. Imprimir resumen ---
    print("¡Proceso completado exitosamente!")
    print(f"Archivo de entrada: '{archivo_entrada}' ({total_filas} filas de datos)")
    print(f"Archivo 20%: '{archivo_salida_20}' ({len(grupo_20_porciento)} filas)")
    print(f"Archivo 80%: '{archivo_salida_80}' ({len(grupo_80_porciento)} filas)")


# --- CÓMO USAR EL SCRIPT ---

# 1. Define los nombres de tus archivos
ARCHIVO_ENTRADA = 'data/arbolado-mza-dataset.csv'
ARCHIVO_SALIDA_20 = 'data/arbolado-mendoza-dataset-validation.csv'
ARCHIVO_SALIDA_80 = 'data/arbolado-mendoza-dataset-train.csv'

if __name__ == "__main__":
    dividir_csv_aleatoriamente(ARCHIVO_ENTRADA, ARCHIVO_SALIDA_20, ARCHIVO_SALIDA_80)