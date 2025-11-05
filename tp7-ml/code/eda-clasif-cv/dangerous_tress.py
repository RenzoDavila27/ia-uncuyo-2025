import matplotlib.pyplot as plt
import csv
import os
import random

# --- Configuración ---
ARCHIVO_CSV = 'data/arbolado-mendoza-dataset-train.csv'
COLUMNA_CLASES = 'especie' 
COLUMNA_BINARIA = 'inclinacion_peligrosa' 
GRAFICO_SALIDA = 'images/dangerous_trees_species.png'

def generar_grafico_apilado_100(archivo_csv, col_clases, col_binaria):
    """
    Lee el CSV, calcula los porcentajes y genera el gráfico
    de barras apiladas al 100% solo con Matplotlib.
    """
    
    # --- 1. Leer y procesar los datos del CSV ---
    
    conteo_agregado = {}
    
    valores_binarios_set = set()
    
    try:
        with open(archivo_csv, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f) # Usamos DictReader para fácil acceso por nombre
            
            for fila in reader:
                clase = fila[col_clases]
                valor = fila[col_binaria]
                
                valores_binarios_set.add(valor)
                
                # Inicializar diccionarios si no existen
                if clase not in conteo_agregado:
                    conteo_agregado[clase] = {}
                
                if valor not in conteo_agregado[clase]:
                    conteo_agregado[clase][valor] = 0
                
                # Incrementar el conteo
                conteo_agregado[clase][valor] += 1
                
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_csv}'")
        return
    except KeyError as e:
        print(f"Error: Columna {e} no encontrada en el CSV.")
        return
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    # Nos aseguramos de que solo haya dos valores binarios
    if len(valores_binarios_set) != 2:
        print(f"Error: La columna '{col_binaria}' debe tener exactamente 2 valores únicos.")
        print(f"Valores encontrados: {valores_binarios_set}")
        return

    # Nombres de las dos categorías binarias
    valor_A, valor_B = sorted(list(valores_binarios_set))

    # --- 2. Calcular los porcentajes ---
    
    # Nombres de todas las clases principales (ej. 'Ventas', 'Marketing', ...)
    clases_principales = sorted(conteo_agregado.keys())
    
    porcentajes_A = [] # Lista de porcentajes para el Valor A
    porcentajes_B = [] # Lista de porcentajes para el Valor B
    
    for clase in clases_principales:
        counts_clase = conteo_agregado[clase]
        
        count_A = counts_clase.get(valor_A, 0)
        count_B = counts_clase.get(valor_B, 0)
        
        total = count_A + count_B
        
        if total == 0:
            porcentajes_A.append(0)
            porcentajes_B.append(0)
        else:
            porcentajes_A.append((count_A / total) * 100)
            porcentajes_B.append((count_B / total) * 100)

    # --- 3. Graficar con Matplotlib ---
    
    print("\nDatos procesados (porcentajes):")
    for i, clase in enumerate(clases_principales):
        print(f"- {clase}: {porcentajes_A[i]:.1f}% {valor_A} , {porcentajes_B[i]:.1f}% {valor_B}")

    fig, ax = plt.subplots(figsize=(12, 7)) # Crear figura y ejes
    
    bar_width = 0.8 # Ancho de las barras

    # Dibujar la primera barra (Valor A)
    ax.bar(
        clases_principales, 
        porcentajes_A, 
        width=bar_width, 
        label=valor_A, 
        color="#4183CF" # Un azul
    )
    
    # Dibujar la segunda barra (Valor B) "encima" de la primera
    # La clave es usar el argumento 'bottom=porcentajes_A'
    ax.bar(
        clases_principales, 
        porcentajes_B, 
        width=bar_width, 
        label=valor_B, 
        bottom=porcentajes_A, # <-- Esto es lo que las apila
        color='#C44E52' # Un rojo
    )

    for i in range(len(clases_principales)):
        # Obtener los porcentajes para esta barra
        pct_A = porcentajes_A[i]
        pct_B = porcentajes_B[i]

        # Calcular posiciones Y
        # Posición para A: A la mitad de la barra A
        y_A = pct_A / 2
        # Posición para B: En la base de B (pct_A) + la mitad de la barra B
        y_B = pct_A + (pct_B / 2)

        # Formatear el texto
        texto_A = f"{pct_A:.1f}%"
        texto_B = f"{pct_B:.1f}%"

        # Añadir el texto para A (solo si el espacio es > 5%)
        if pct_A > 5:
            ax.text(i, y_A, texto_A, 
                    ha='center', va='center', 
                    color='white', fontsize=5, fontweight='bold')

        # Añadir el texto para B (solo si el espacio es > 5%)
        if pct_B > 5:
            ax.text(i, y_B, texto_B, 
                    ha='center', va='center', 
                    color='white', fontsize=5, fontweight='bold')

    # --- 4. Añadir etiquetas y formato ---
    ax.set_title(f'Tipos de arboles junto a su porcentaje de ser peligroso')
    ax.set_xlabel(col_clases.capitalize(), fontsize=12)
    ax.set_ylabel('Porcentaje (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right') 
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 10))
    ax.legend(title=col_binaria.capitalize())
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Guardar y mostrar
    try:
        plt.savefig(GRAFICO_SALIDA)
        print(f"\n¡Gráfico guardado exitosamente como '{GRAFICO_SALIDA}'!")
        plt.show()
    except Exception as e:
        print(f"Error al guardar o mostrar el gráfico: {e}")

# --- Ejecución del script ---
if __name__ == "__main__":
    
    # 2. Generar el gráfico
    generar_grafico_apilado_100(ARCHIVO_CSV, COLUMNA_CLASES, COLUMNA_BINARIA)