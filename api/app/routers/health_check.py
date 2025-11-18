from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
def health_check():
    """returns json server status data"""
    return JSONResponse({
      "status_code": 200,
      "detail": "ok",
      "result": "working"
      })