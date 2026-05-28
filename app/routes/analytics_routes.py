from fastapi import APIRouter

from app.services.analytics_service import (
    get_client_pivot_table,
    get_clients,
    get_dashboard_summary
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
def dashboard_summary():
    return get_dashboard_summary()