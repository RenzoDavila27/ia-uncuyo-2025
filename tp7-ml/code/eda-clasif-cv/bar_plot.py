import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random

# --- Configuración ---
ARCHIVO_ENTRADA = 'data/arbolado-mendoza-dataset-train.csv'
COLUMNA_OBJETIVO = 'inclinacion_peligrosa' # La columna que queremos analizar
GRAFICO_MATPLOTLIB = 'images/dangerous_distribution.png'

def generar_grafico_matplotlib(archivo_csv, columna):
    """Genera un gráfico de barras con Pandas y Matplotlib."""
    print(f"\n--- Generando gráfico con Matplotlib de '{columna}' ---")
    try:
        # 1. Leer el CSV con pandas
        df = pd.read_csv(archivo_csv)
        
        if columna not in df.columns:
            print(f"Error: La columna '{columna}' no se encuentra en el archivo.")
            return

        # 2. Contar la frecuencia de cada valor en la columna
        conteo_frecuencia = df[columna].value_counts()
        
        print("Datos contados:")
        print(conteo_frecuencia)

        # 3. Graficar con Matplotlib (usando el plotter de pandas)
        plt.figure(figsize=(10, 6)) # Define el tamaño de la figura
        conteo_frecuencia.plot(
            kind='bar',  # Tipo de gráfico
            color='skyblue',
            edgecolor='black'
        )

        plt.text(0, 13000, conteo_frecuencia[0], ha='center', va='center', color='white', fontsize=15, fontweight='bold')
        plt.text(1, 1500, conteo_frecuencia[1], ha='center', va='center', color='white', fontsize=15, fontweight='bold')

        # 4. Añadir títulos y etiquetas
        plt.title(f'Conteo de Frecuencia para la Columna: {columna}')
        plt.ylabel('Cantidad (Frecuencia)')
        plt.xlabel('Valores')
        plt.xticks(rotation=0) # Rota las etiquetas del eje X para mejor lectura
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout() # Ajusta el gráfico para que todo quepa
        
        # 5. Guardar y mostrar
        plt.savefig(GRAFICO_MATPLOTLIB)
        print(f"Gráfico guardado en '{GRAFICO_MATPLOTLIB}'")
        plt.show()

    except Exception as e:
        print(f"Ocurrió un error con Matplotlib: {e}")

# --- Ejecución del script ---
if __name__ == "__main__":
    
    # 2. Generar el gráfico con Matplotlib
    generar_grafico_matplotlib(ARCHIVO_ENTRADA, COLUMNA_OBJETIVO)