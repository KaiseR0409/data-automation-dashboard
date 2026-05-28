from fastapi import APIRouter, UploadFile, File

from app.services.upload_service import upload_excel

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/")
async def upload(file: UploadFile = File(...)):
    return await upload_excel(file)