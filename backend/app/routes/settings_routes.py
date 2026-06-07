from fastapi import APIRouter

router = APIRouter(prefix="/settings", tags=["Settings"])

# MorphFlow settings are handled via User model for now,
# but we can keep the router for future preferences.

@router.get("")
def get_settings():
    return {"message": "Settings endpoint"}
