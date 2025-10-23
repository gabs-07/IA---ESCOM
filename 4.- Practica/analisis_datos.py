# Script para el análisis y preprocesamiento de datasets
# Este script realiza las siguientes tareas:
# 1. Análisis exploratorio de datos (EDA)
# 2. Manejo de valores faltantes
# 3. Detección y tratamiento de outliers
# 4. Codificación de variables categóricas
# 5. Normalización de datos

# Importación de bibliotecas necesarias
import pandas as pd  # Para manipulación y análisis de datos
import numpy as np   # Para operaciones numéricas
from scipy import stats  # Para análisis estadístico
from sklearn.preprocessing import LabelEncoder, StandardScaler  # Para preprocesamiento
from ydata_profiling import ProfileReport  # Para generación de reportes EDA
import os  # Para operaciones con el sistema de archivos

def manejar_valores_faltantes(df, umbral=0.1):
    """
    Maneja los valores faltantes en el DataFrame.
    Args:
        df: DataFrame a procesar
        umbral: Porcentaje máximo de valores faltantes permitidos (default 0.1 = 10%)
    Returns:
        DataFrame procesado y lista de columnas imputadas
    """
    columnas_faltantes = df.columns[df.isnull().mean() > umbral]
    columnas_imputadas = []
    for columna in columnas_faltantes:
        if df[columna].dtype in ['int64', 'float64']:
            df[columna].fillna(df[columna].mean(), inplace=True)
        else:
            df[columna].fillna(df[columna].mode()[0], inplace=True)
        columnas_imputadas.append(columna)
    return df, list(columnas_imputadas)

def manejar_valores_atipicos(df, columnas, q=0.05):
    """
    Aplica winsorización para manejar valores atípicos.
    Args:
        df: DataFrame a procesar
        columnas: Lista de columnas a procesar
        q: Quantil para winsorización (default 0.05 = 5%)
    Returns:
        DataFrame con valores atípicos tratados
    """
    for columna in columnas:
        if df[columna].dtype in ['int64', 'float64']:
            df[columna] = stats.mstats.winsorize(df[columna], limits=[q, q])
    return df

def analizar_estructura(df, nombre):
    """
    Analiza la estructura básica del dataset y valores faltantes.
    Args:
        df: DataFrame a analizar
        nombre: Nombre identificativo del dataset
    Returns:
        Lista de columnas con más del 10% de valores faltantes
    """
    filas, columnas = df.shape
    print(f"\nEDA: Dataset {nombre}")
    print(f"Instancias (filas): {filas}, Atributos (columnas): {columnas}")
    porcentajes_nulos = df.isnull().mean().sort_values(ascending=False)
    print("Porcentaje de valores faltantes por columna (top 10):")
    print(porcentajes_nulos.head(10).to_string())
    columnas_mas_10pct = porcentajes_nulos[porcentajes_nulos > 0.1].index.tolist()
    if columnas_mas_10pct:
        print(f"Columnas con >10% de valores faltantes: {columnas_mas_10pct}")
    else:
        print("No se encontraron columnas con >10% de valores faltantes.")
    return columnas_mas_10pct

def detectar_outliers(df, columnas, z_thresh=3.0):
    """
    Detecta outliers usando el método de z-score.
    Args:
        df: DataFrame a analizar
        columnas: Lista de columnas a revisar
        z_thresh: Umbral de z-score (default 3.0)
    Returns:
        Diccionario con conteo de outliers por columna
    """
    resumen_outliers = {}
    for col in columnas:
        if col in df.columns and df[col].dtype in ['int64', 'float64']:
            try:
                col_vals = df[col].dropna()
                if col_vals.size == 0:
                    cnt = 0
                else:
                    zscores = np.abs(stats.zscore(col_vals))
                    cnt = int((zscores > z_thresh).sum())
                resumen_outliers[col] = cnt
            except Exception:
                resumen_outliers[col] = 0
    # Mostrar las columnas con outliers detectados
    columnas_con_outliers = {k: v for k, v in resumen_outliers.items() if v > 0}
    if columnas_con_outliers:
        print("Outliers detectados (conteo por columna, z>|3|):")
        for k, v in columnas_con_outliers.items():
            print(f" - {k}: {v}")
    else:
        print("No se detectaron outliers por z-score > 3 en las columnas numéricas revisadas.")
    return resumen_outliers

def codificar_categoricas(df):
    """
    Codifica variables categóricas a numéricas usando LabelEncoder.
    Args:
        df: DataFrame con variables categóricas
    Returns:
        DataFrame con variables categóricas codificadas
    """
    codificador = LabelEncoder()
    for columna in df.select_dtypes(include=['object']):
        df[columna] = codificador.fit_transform(df[columna].astype(str))
    return df

def normalizar_datos(df):
    """
    Normaliza las variables numéricas usando StandardScaler.
    Args:
        df: DataFrame con variables numéricas
    Returns:
        DataFrame con variables numéricas normalizadas
    """
    escalador = StandardScaler()
    columnas_numericas = df.select_dtypes(include=['int64', 'float64']).columns
    df[columnas_numericas] = escalador.fit_transform(df[columnas_numericas])
    return df

def procesar_dataset(ruta_archivo, nombre, generar_reporte=True):
    """
    Función principal que coordina todo el procesamiento del dataset.
    Args:
        ruta_archivo: Ruta al archivo CSV
        nombre: Nombre identificativo del dataset
        generar_reporte: Bool para generar reporte HTML (default True)
    Returns:
        Diccionario con resultados del procesamiento
    """
    # Cargar dataset
    df = pd.read_csv(ruta_archivo)
    print(f"\nProcesando dataset {nombre}:")
    print(f"Dimensiones iniciales: {df.shape}")
    
    # Estructura y missing >10%
    columnas_mas_10pct = analizar_estructura(df, nombre)
    
    # Generar reporte de perfil opcional
    if generar_reporte:
        try:
            perfil = ProfileReport(df, title=f"Perfil del Dataset {nombre}")
            perfil.to_file(f"perfil_{nombre}.html")
            print(f"Perfil guardado en perfil_{nombre}.html")
        except Exception as e:
            print(f"No se pudo generar el perfil (posible dataset grande): {e}")
    
    # Manejar valores faltantes (imputar columnas con > umbral)
    df, columnas_imputadas = manejar_valores_faltantes(df, umbral=0.1)
    if columnas_imputadas:
        print(f"Se imputaron las siguientes columnas (>10% nulos): {columnas_imputadas}")
    else:
        print("No se imputó ninguna columna por superar el umbral del 10%.")
    
    # Detectar outliers antes de winsorize (informa conteos por columna)
    columnas_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    resumen_outliers = detectar_outliers(df, columnas_numericas, z_thresh=3.0)
    
    # Aplicar winsorize para columnas numéricas
    df = manejar_valores_atipicos(df, columnas_numericas, q=0.05)
    print("Se aplicó winsorize (limits=0.05) a las columnas numéricas.")
    
    # Codificar variables categóricas
    df = codificar_categoricas(df)
    print("Variables categóricas codificadas a números (LabelEncoder por columna).")
    
    # Normalizar dataset
    df = normalizar_datos(df)
    print("Dataset normalizado (StandardScaler aplicado a columnas numéricas).")
    
    print(f"Dimensiones finales: {df.shape}")
    return {
        "df": df,
        "dim_ini": (None if df is None else df.shape),  # placeholder si desea más detalles
        "columnas_imputadas": columnas_imputadas,
        "resumen_outliers": resumen_outliers
    }

# Verificación inicial del entorno
print(f"Directorio actual: {os.getcwd()}")
print(f"¿El archivo existe?: {os.path.exists('Titanic-Dataset.csv')}")

# Punto de entrada principal
if __name__ == "__main__":
    """
    Sección principal del script donde se definen las rutas de los datasets
    y se ejecuta el procesamiento.
    """
    # Configuración de rutas de datasets
    ruta_dataset1 = "c:/Users/Gabriel Ruiz/IA---ESCOM/4.- Practica/Titanic-Dataset.csv"
    ruta_dataset2 = "c:/Users/Gabriel Ruiz/IA---ESCOM/4.- Practica/segundo_dataset.csv"
    
    # Procesamiento del primer dataset
    if os.path.exists(ruta_dataset1):
        resultado1 = procesar_dataset(ruta_dataset1, "Dataset1")
    else:
        print(f"No se encontró el archivo: {ruta_dataset1}")
    
    # Procesamiento del segundo dataset
    if ruta_dataset2 and os.path.exists(ruta_dataset2):
        resultado2 = procesar_dataset(ruta_dataset2, "Dataset2")
    else:
        print("No se procesó el segundo dataset (ruta vacía o archivo no encontrado).")

