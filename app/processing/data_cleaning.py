import pandas as pd

def clean_dataframe(df):
     #eliminar columnas unnamed
    df = df.loc[:,~df.columns.str.contains("^Unnamed")]
    #eliminar filas completamente vacias
    df = df.dropna(how="all")
    #limpiar espacios en nombres de columnas
    df.columns = df.columns.str.strip()
    #convertir columnas a tipo texto
    text_columns = df.select_dtypes(include=["object"]).columns

    for col in text_columns:
        df[col] = df[col].astype(str).str.strip()

    #convertir fechas si existe la columna
    if "Fecha" in df.columns:
        df["Fecha"] = pd.to_datetime(
            df["Fecha"],
            errors="coerce"
        )
    return df