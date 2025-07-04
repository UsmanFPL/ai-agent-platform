from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_tools():
    return {"message": "List tools - to be implemented"}