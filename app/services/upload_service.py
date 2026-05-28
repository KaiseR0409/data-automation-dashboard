import pandas as pd
import os
from fastapi import UploadFile
from processing.data_cleaning import clean_dataframe
from storage import dataset_store

UPLOAD_DIR = "app/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


async def upload_excel(file: UploadFile):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    df = pd.read_excel(file_path)

    # limpiar
    df = clean_dataframe(df)

    # guardar dataset global
    dataset_store.dataset = df

    clients = (
        df["Sucursal"]
        .dropna()
        .unique()
        .tolist()
    )

    return {
        "message": "Excel cargado correctamente",
        "rows": len(df),
        "clients": clients,
        "columns": df.columns.tolist()
    }