
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import lightgbm as lgb

def clean_data(df, is_train=True):
    """
    Limpia el dataframe y agrega las columnas que podrian dar informacion.
    """
    print(f"--- Iniciando limpieza {'(train)' if is_train else '(test)'} ---")

    # 1. Selección de Columnas
    df = df.drop(columns=['id', 'ultima_modificacion', 'seccion'], errors='ignore')

    # 2. Transformación de Columnas
    diametro_map = {"Chico": 30, "Mediano": 50, "Grande": 70}
    altura_map = {
        "Muy bajo (1 - 2 mts)": 1.5,
        "Bajo (2 - 4 mts)": 3,
        "Medio (4 - 8 mts)": 6,
        "Alto (> 8 mts)": 9,
    }
    df['diametro_tronco'] = df['diametro_tronco'].map(diametro_map)
    df['altura'] = df['altura'].map(altura_map)

    # 3. Limpieza de factores (Lumping)
    for col in ['especie', 'nombre_seccion']:
        counts = df[col].value_counts()
        mask = df[col].isin(counts[counts < 10].index)
        df.loc[mask, col] = f"{col.capitalize()}_Otra"

    # 4. Manejo de NAs y Objetivo (solo para training set)
    if is_train:
        df = df.dropna(subset=['inclinacion_peligrosa'])
        df = df.dropna()
        df['inclinacion_peligrosa'] = df['inclinacion_peligrosa'].astype(int)

    print("--- Limpieza finalizada ---")
    return df

def feature_engineer(df, kmeans=None, is_train=True):
    """
    Engineers new features like geographic clusters and interaction terms.
    """
    print("--- Iniciando ingeniería de atributos ---")

    # 1. Clustering Geográfico (K-Means)
    coords = df[['long', 'lat']].dropna()
    if kmeans is None:
        print("Entrenando modelo K-Means...")
        kmeans = KMeans(n_clusters=5, random_state=123, n_init=10)
        kmeans.fit(coords)

    df['zona_cluster'] = np.nan
    df.loc[coords.index, 'zona_cluster'] = kmeans.predict(coords)

    # 2. Ratios e Interacciones
    df['densidad_arbol'] = df['circ_tronco_cm'] / df['area_seccion']
    df['densidad_arbol'] = df['densidad_arbol'].replace([np.inf, -np.inf], np.nan)

    df['circ_altura_ratio'] = df['circ_tronco_cm'] / (df['altura'] + 0.01)
    df['circ_altura_ratio'] = df['circ_altura_ratio'].replace([np.inf, -np.inf], np.nan)

    df['especie_seccion'] = df['especie'].astype(str) + "_" + df['nombre_seccion'].astype(str)

    # Lumping para la nueva característica de interacción
    counts = df['especie_seccion'].value_counts()
    mask = df['especie_seccion'].isin(counts[counts < 10].index)
    df.loc[mask, 'especie_seccion'] = "Interaccion_Otra"

    # Convertir a categóricas
    for col in ['zona_cluster', 'especie_seccion', 'especie', 'nombre_seccion']:
        df[col] = df[col].astype('category')

    print("--- Ingeniería de atributos finalizada ---")
    if is_train:
        return df, kmeans
    return df


if __name__ == "__main__":

    train_original = pd.read_csv('code/eda-clasif-cv/r_code/arbolado-mza-dataset.csv')
    test_original = pd.read_csv('code/eda-clasif-cv/r_code/arbolado-mza-dataset-test.csv')
    test_ids = test_original['id']

    # --- Procesar Datos de Entrenamiento ---
    train_limpio = clean_data(train_original.copy(), is_train=True)
    train_enriquecido, kmeans_model = feature_engineer(train_limpio, kmeans=None, is_train=True)

    # --- Preparar Datos para LightGBM ---
    target_col = "inclinacion_peligrosa"
    y_train = train_enriquecido[target_col]
    X_train = train_enriquecido.drop(columns=[target_col])

    categorical_features = X_train.select_dtypes(include=['category']).columns.tolist()

    lgb_params = {
        'objective': 'binary',
        'metric': 'auc',
        'is_unbalance': True,
        'n_estimators': 100,
        'learning_rate': 0.05,
        'verbose': -1
    }

    model = lgb.LGBMClassifier(**lgb_params)
    model.fit(X_train, y_train, categorical_feature=categorical_features)


    test_limpio = clean_data(test_original.copy(), is_train=False)
    test_enriquecido = feature_engineer(test_limpio, kmeans=kmeans_model, is_train=False)

    train_cols = X_train.columns
    test_cols = test_enriquecido.columns
    missing_in_test = set(train_cols) - set(test_cols)
    for c in missing_in_test:
        test_enriquecido[c] = 0
    test_enriquecido = test_enriquecido[train_cols]

    for col in categorical_features:
        train_categories = X_train[col].cat.categories
        test_enriquecido[col] = test_enriquecido[col].astype('category').cat.set_categories(train_categories)

    predicciones_prob = model.predict_proba(test_enriquecido)[:, 1]
    predicciones_clase = (predicciones_prob > 0.5).astype(int)

    submission_df = pd.DataFrame({
        'id': test_ids,
        'inclinacion_peligrosa': predicciones_clase
    })

    submission_path = 'submission.csv'
    submission_df.to_csv(submission_path, index=False)
    print(f"--- ¡Archivo '{submission_path}' creado y listo para subir! ---")
