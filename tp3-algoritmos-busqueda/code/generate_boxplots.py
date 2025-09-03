import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === 1. Cargar CSV ===
df = pd.read_csv("results.csv")
df.columns = df.columns.str.strip()

# === 2. Filtrar algoritmos (ej. excluir DFS) ===
df = df[df["algorithm_name"] == "DFS"]

# === 2. Definir las métricas a graficar ===
metrics = ["states_n", "actions_count", "actions_cost", "time"]

# === 3. Crear boxplots para cada métrica ===
list = []
plt.figure(figsize=(14, 10))

for metric in metrics:
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="algorithm_name", y=metric, hue="algorithm_name", palette="Set2", legend=False, width=0.6)
    sns.stripplot(data=df, x="algorithm_name", y=metric, color=".25", size=2, jitter=True)

    plt.title(f"Distribución de {metric}")
    plt.xticks(rotation=45, ha="right", fontsize=9)  # rotar y achicar fuente
    plt.tight_layout()

    # Guardar con nombre dinámico
    filename = f"boxplot_{metric}.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()  # cerrar la figura para liberar memoria