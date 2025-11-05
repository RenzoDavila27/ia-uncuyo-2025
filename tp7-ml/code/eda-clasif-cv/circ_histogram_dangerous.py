import matplotlib.pyplot as plt
import csv
import os
import random

# --- Configuración ---
ARCHIVO_CSV = 'data/arbolado-mendoza-dataset-train.csv'
COLUMNA_HISTOGRAMA = 'circ_tronco_cm' # Variable numérica a graficar
COLUMNA_FILTRO = 'inclinacion_peligrosa' # Variable categórica para separar

def generar_grafico_2x2_bins(datos, titulo_categoria, archivo_salida):
    """
    Función reutilizable para crear una imagen 2x2 con los 4 histogramas
    basados en el % de valores únicos de los 'datos' recibidos.
    """
    
    if not datos:
        print(f"Advertencia: No hay datos para la categoría '{titulo_categoria}'. Saltando gráfico.")
        return

    # --- 1. Calcular el número de bins basado en VALORES ÚNICOS ---
    valores_unicos = set(datos)
    total_valores_unicos = len(valores_unicos)
    
    porcentajes = [(0.10, "10%"), (0.30, "30%"), (0.50, "50%"), (1.00, "100%")]
    
    lista_bins = []
    for pct, _ in porcentajes:
        num_bins = max(1, int(total_valores_unicos * pct))
        lista_bins.append(num_bins)

    print(f"-> Para '{titulo_categoria}': {len(datos)} filas, {total_valores_unicos} vals. únicos. Bins: {lista_bins}")

    # --- 2. Crear los 4 gráficos (en una cuadrícula 2x2) ---
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    axs = axs.flatten() 

    for i in range(len(porcentajes)):
        ax = axs[i]
        num_bins = lista_bins[i]
        etiqueta = porcentajes[i][1]
        
        ax.hist(datos, bins=num_bins, color='darkcyan', edgecolor='k', alpha=0.7)
        ax.set_title(f"Histograma con {num_bins} bins ({etiqueta} de vals. únicos)")
        ax.set_xlabel(COLUMNA_HISTOGRAMA)
        ax.set_ylabel("Frecuencia")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    # --- 3. Ajustar y mostrar ---
    titulo_general = (f"Histogramas para '{COLUMNA_FILTRO}' = '{titulo_categoria}'\n"
                      f"(Total: {len(datos)} datos, {total_valores_unicos} únicos)")
    fig.suptitle(titulo_general, fontsize=16)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.93])
    
    try:
        plt.savefig(archivo_salida)
        print(f"   ¡Gráfico guardado exitosamente como '{archivo_salida}'!")
        plt.show() # Muestra el gráfico
        plt.close(fig) # Cierra la figura para liberar memoria
    except Exception as e:
        print(f"Error al guardar o mostrar el gráfico: {e}")

# --- Ejecución principal del script ---
if __name__ == "__main__":

    # 2. Leer y separar los datos
    # Usamos un diccionario: {'0': [lista de datos], '1': [lista de datos]}
    datos_separados = {}
    
    try:
        with open(ARCHIVO_CSV, mode='r', newline='', encoding='utf-8') as f:
            # Usamos DictReader para leer por nombre de columna
            reader = csv.DictReader(f)
            
            for fila in reader:
                try:
                    categoria = fila[COLUMNA_FILTRO]
                    valor_num = float(fila[COLUMNA_HISTOGRAMA])
                    
                    # Si es la primera vez que vemos esta categoría, creamos su lista
                    if categoria not in datos_separados:
                        datos_separados[categoria] = []
                    
                    # Agregamos el valor numérico a la lista de su categoría
                    datos_separados[categoria].append(valor_num)
                    
                except (ValueError, TypeError):
                    # Omitir filas con datos no válidos
                    pass
        
        print(f"Datos leídos y separados en {len(datos_separados)} categorías: {list(datos_separados.keys())}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ARCHIVO_CSV}'")
        exit()
    except KeyError as e:
        print(f"Error: Columna {e} no encontrada en el CSV.")
        exit()
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        exit()

    # 3. Generar un gráfico por cada categoría encontrada
    
    if not datos_separados:
        print("No se encontraron datos para graficar.")
    else:
        for categoria, lista_de_datos in datos_separados.items():
            # Creamos un nombre de archivo único para cada categoría
            archivo_salida_img = f"images/histogramas_{COLUMNA_FILTRO}_{categoria}.png"
            
            # Llamamos a nuestra función de graficado
            generar_grafico_2x2_bins(lista_de_datos, categoria, archivo_salida_img)