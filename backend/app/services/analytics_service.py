import pandas as pd
from app.storage import dataset_store

def get_client_pivot_table(client:str, year, month, day, turno):
    df = dataset_store.dataset

    if df is None:
        return{
            "error":"No hay dataset cargado"
        }
    
    #filtrar el cliente
    filtered_df = df[df["Sucursal"] == client].copy()

    #transformar fecha a datetime nuevamente
    filtered_df["Fecha"] = pd.to_datetime(
        filtered_df["Fecha"],
        errors="coerce"
    )

    #generar dia de la semana
    days_map = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }

    filtered_df["Año"] = (
        filtered_df["Fecha"].dt.year
    )

    filtered_df["Mes"] = (
        filtered_df["Fecha"].dt.month
    )

    filtered_df["Dia"] = (
        filtered_df["Fecha"].dt.day
    )
    
    filtered_df["Dia Semana"] = (
        filtered_df["Fecha"]
        .dt.day_name()
        .map(days_map)
    )
    
    if year:
        filtered_df = filtered_df[
            filtered_df["Año"] == year
        ]

    if month:
        filtered_df = filtered_df[
            filtered_df["Mes"] == month
        ]

    if day:
        filtered_df = filtered_df[
            filtered_df["Dia"] == day
        ]

    if turno:
        filtered_df = filtered_df[
            filtered_df["Turno"] == turno
        ]

    
    #pivote
    pivot = pd.pivot_table(
        filtered_df,
        values="Sacos",
        index=[
            "Fecha",
            "Dia Semana",
            "Turno"
        ],
        columns="Formato",
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    pivot.columns.name = None

    pivot["Fecha"] = (
        pivot["Fecha"]
        .dt.strftime("%d-%m-%Y")
    )

    return pivot.to_dict(
        orient="records"
    )

def calculate_variation(current, previous):
    if previous == 0:
        return 0
    
    return round(
        ((current - previous)/ previous) * 100,
        1
    )
    
def get_dashboard_summary(client=None, year=None):

    df = dataset_store.dataset
    previous_df = dataset_store.previous_dataset

    if df is None:
        return {
            "error": "Dataset no cargado correctamente"
        }
    if df.empty:
        return{
            "error": "Dataset vacío"
        }

    df = df.copy()

    df["Despacho"] = pd.to_numeric(
        df["Despacho"],
        errors="coerce"
    ).fillna(0)
    
    if previous_df is not None:

        previous_df = previous_df.copy()

        previous_df["Despacho"] = pd.to_numeric(
            previous_df["Despacho"],
            errors="coerce"
        ).fillna(0)

    # filtrar por año
    if year:

        df = df[
            df["Fecha"].dt.year == year
        ]

        if previous_df is not None:

            previous_df = previous_df[
                previous_df["Fecha"].dt.year == year
            ]
    

    #filtrar por cliente
    if client:
        df = df[
            df["Sucursal"] == client
        ]

        if previous_df is not None:
            previous_df = previous_df[
                previous_df["Sucursal"] == client
            ]
    
    total_sacos = 0
    total_maxisacos = 0
    registros_totales = 0

    if "Formato" in df.columns and "Despacho" in df.columns:

        total_sacos = (
            df[
                df["Formato"] == "SACOS"
            ]["Despacho"]
            .sum()
        )

        total_maxisacos = (
            df[
                df["Formato"] == "MAXISACOS"
            ]["Despacho"]
            .sum()
        )

    if "Sucursal" in df.columns:

        clientes_activos = (
            df["Sucursal"]
            .nunique()
        )

    registros_totales = len(df)

    #variaciones
    sacos_variation = 0
    maxisacos_variation = 0
    clientes_variation = 0
    registros_variation = 0

    if previous_df is not None and not previous_df.empty:
        previous_sacos = (
            previous_df[
                previous_df["Formato"] == "SACOS"
            ]["Despacho"].sum()
        )

        previous_total_maxisacos = (
            previous_df[
                previous_df["Formato"] == "MAXISACOS"
            ]["Despacho"].sum()
        )

        previous_clientes = (
            previous_df["Sucursal"]
            .nunique()
        )

        previous_registros_totales = len(previous_df)

        sacos_variation = calculate_variation(
            total_sacos,
            previous_sacos
        )

        clientes_variation = calculate_variation(
            clientes_activos,
            previous_clientes
        )

        maxisacos_variation = calculate_variation(
            total_maxisacos,
            previous_total_maxisacos
        )

        registros_variation = calculate_variation(
            registros_totales,
            previous_registros_totales
        )


    return {
        "total_sacos": float(round(total_sacos, 2)),
        "total_maxisacos": float(round(total_maxisacos, 2)),
        "clientes_activos": int(clientes_activos),
        "registros_totales": int(registros_totales),

        "variations": {
            "sacos": float(sacos_variation),
            "maxisacos": float(maxisacos_variation),
            "clientes": float(clientes_variation),
            "registros": float(registros_variation)
        }
}

def get_line_chart_data(
  client=None,
  product=None,
  year=None,
  month=None      
):
    df = dataset_store.dataset

    if df is None:
        return []
    
    filtered_df = df.copy()

    filtered_df["Fecha"] = pd.to_datetime(
        filtered_df["Fecha"],
        errors="coerce"
    )

    if client:
        filtered_df = filtered_df[
            filtered_df["Sucursal"] == client
        ]

    if product:
        filtered_df = filtered_df[
            filtered_df["Formato"] == product
        ]

    if year:
        filtered_df = filtered_df[
            filtered_df["Fecha"].dt.year == year
        ]

    if month:
        filtered_df = filtered_df[
            filtered_df["Fecha"].dt.month == month
        ]

    
    grouped = (
        filtered_df
        .groupby(["Fecha", "SEMANA"])["Sacos"]
        .sum()
        .reset_index()
    )

    grouped["Fecha"] = (
        grouped["Fecha"]
        .dt.strftime("%d-%m-%Y")
    )

    grouped.columns = [
        "fecha",
        "semana",
        "cantidad"
    ]

    return grouped.to_dict(
        orient="records"
    )

def get_truck_chart(
    client=None,
    year=None,
    month=None
):
    df = dataset_store.dataset

    if df is None:
        return []

    df = df.copy()

    df["Fecha"] = pd.to_datetime(
        df["Fecha"],
        errors="coerce"
    )

    if client:
        df = df[
            df["Sucursal"] == client
        ]

    if year:
        df = df[
            df["Fecha"].dt.year == year
        ]

    if month:
        df = df[
            df["Fecha"].dt.month == month
        ]

    df["CONTADOR"] = pd.to_numeric(
        df["CONTADOR"],
        errors="coerce"
    ).fillna(0)

    grouped = (
        df
        .groupby(["Fecha", "SEMANA"])["CONTADOR"]
        .sum()
        .reset_index()
    )

    grouped["Fecha"] = (
        grouped["Fecha"]
        .dt.strftime("%d-%m-%Y")
    )

    grouped.columns = [
        "fecha",
        "semana",
        "camiones"
    ]

    return grouped.to_dict(
        orient="records"
    )

def get_clients():

    df = dataset_store.dataset

    if df is None:
        return []

    clients = (
        df["Sucursal"]
        .dropna()
        .unique()
        .tolist()
    )

    clients.sort()

    return clients