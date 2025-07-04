from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_executions():
    return {"message": "List executions - to be implemented"}