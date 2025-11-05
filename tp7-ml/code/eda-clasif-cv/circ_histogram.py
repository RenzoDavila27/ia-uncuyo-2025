import matplotlib.pyplot as plt
import csv
import os
import random

# --- Configuración ---
ARCHIVO_CSV = 'data/arbolado-mendoza-dataset-train.csv'
COLUMNA_OBJETIVO = 'circ_tronco_cm'
GRAFICO_SALIDA = 'images/circ_histograms.png'

def generar_histogramas_porcentuales_unicos(archivo_csv, columna):
    """
    Genera 4 histogramas con un número de bins basado en el
    porcentaje del total de VALORES ÚNICOS.
    """
    
    # --- 1. Leer los datos del CSV a una lista ---
    datos = []
    try:
        with open(archivo_csv, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            encabezado = next(reader)
            
            try:
                indice_columna = encabezado.index(columna)
            except ValueError:
                print(f"Error: No se encontró la columna '{columna}' en el CSV.")
                return

            for fila in reader:
                try:
                    datos.append(float(fila[indice_columna]))
                except ValueError:
                    pass # Omitir valores no numéricos
                    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_csv}'")
        return
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    if not datos:
        print("No se encontraron datos para graficar.")
        return

    # --- 2. Calcular el número de bins basado en VALORES ÚNICOS (LA LÓGICA CAMBIA AQUÍ) ---
    
    # Convertimos la lista de datos a un 'set' para eliminar duplicados
    valores_unicos = set(datos)
    
    # Contamos cuántos valores únicos hay
    total_valores_unicos = len(valores_unicos)

    porcentajes = [(0.10, "10%"), (0.2, "20%"), (0.35, "35%"), (0.5, "50%")]

    lista_bins = []
    for pct, _ in porcentajes:
        # Calculamos el bin como % del total de valores ÚNICOS
        num_bins = max(1, int(total_valores_unicos * pct))
        lista_bins.append(num_bins)

    print(f"Total de filas leídas: {len(datos)}")
    print(f"Total de VALORES ÚNICOS encontrados: {total_valores_unicos}")
    print(f"Números de bins a probar: {lista_bins}")

    # --- 3. Crear los 4 gráficos (en una cuadrícula 2x2) ---
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    axs = axs.flatten() 

    for i in range(len(porcentajes)):
        ax = axs[i]
        num_bins = lista_bins[i]
        etiqueta = porcentajes[i][1]
        
        ax.hist(datos, bins=num_bins, color='c', edgecolor='k', alpha=0.7)
        
        # Modificamos el título para reflejar la nueva lógica
        ax.set_title(f"Histograma con {num_bins} bins ({etiqueta} de vals. únicos)")
        ax.set_xlabel(columna)
        ax.set_ylabel("Frecuencia")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    # --- 4. Ajustar y mostrar ---
    
    # Modificamos el título general
    fig.suptitle(f"Prueba de Bins para '{columna}' (Base: {total_valores_unicos} valores únicos)", fontsize=16)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    try:
        plt.savefig(GRAFICO_SALIDA)
        print(f"\n¡Gráfico guardado exitosamente como '{GRAFICO_SALIDA}'!")
        plt.show()
    except Exception as e:
        print(f"Error al guardar o mostrar el gráfico: {e}")

# --- Ejecución del script ---
if __name__ == "__main__":
    
    # 2. Generar los gráficos
    generar_histogramas_porcentuales_unicos(ARCHIVO_CSV, COLUMNA_OBJETIVO)