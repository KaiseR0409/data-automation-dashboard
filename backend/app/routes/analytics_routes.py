from fastapi import APIRouter

from app.services.analytics_service import (
    get_client_pivot_table,
    get_clients,
    get_dashboard_summary,
    get_line_chart_data
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/client-table")
def client_table(
    client: str,
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
    turno: str | None = None
    ):

    return get_client_pivot_table(client,year,month,day,turno)

@router.get("/clients")
def clients():
    return get_clients()

@router.get("/summary")
def dashboard_summary(
    client: str | None = None,
    year: int | None = None
):
    return get_dashboard_summary(client, year)

@router.get("/line-chart")
def line_chart(
    client: str | None = None,
    product: str | None = None,
    year: int | None = None,
    month: int | None = None
):

    return get_line_chart_data(
        client,
        product,
        year,
        month
    )