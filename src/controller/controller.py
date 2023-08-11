from fastapi import APIRouter
from . import data_viewer

router = APIRouter()

router.include_router(data_viewer.router, prefix="/dataviewer", tags=["DataViewer"])
# router.include_router(item_controller.router, prefix="/item", tags=["Item"])