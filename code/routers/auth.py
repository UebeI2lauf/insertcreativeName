from fastapi import APIRouter, HTTPException, security
from fastapi.param_functions import Body, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from schema import LogIn, User
from database import db
import security
from JWT import create_token

router = APIRouter(tags=["Authentifizierung"])


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user = request
    # da username nicht permutierbar sein sollen und einzigartig
    # werden diese als schlüssel genutzt neben den _ids
    if (identity := await db["user"].find_one({"username": user.username})) is None:

        raise HTTPException(
            status_code=404, detail=f"User {user.username} wurde nicht gefunden"
        )

    hash = identity["password"]
    if not await security.verify_pwd(user.password, hash):
        raise HTTPException(status_code=404, detail=f"Angaben incorrect")

    access_token = create_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
