from fastapi import APIRouter, Depends, HTTPException
from app.db.session import db
from app.routes.auth_routes import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me")
async def update_me(update_data: dict, current_user: User = Depends(get_current_user)):
    await db["users"].update_one({"_id": current_user.id}, {"$set": update_data})
    return {"status": "success"}
