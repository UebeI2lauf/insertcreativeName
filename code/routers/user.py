from fastapi import APIRouter, status, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.routing import run_endpoint_function
from starlette.responses import JSONResponse

import schema

from security import Sicherheit

from database import db


# init router instance
router = APIRouter()


@router.post("/user", response_description="Add a user", response_model=schema.User)
async def create_user(user: schema.User = Body(...)):
    user.password = Sicherheit.get_pwd(user.password)
    print(user.password)
    user = jsonable_encoder(user)
    new_user = await db["user"].insert_one(user)
    lookup_new_user = await db["user"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=lookup_new_user)


@router.get(
    "/user/{username}", response_description="Lookup a User", response_model=schema.User
)
async def show_student(username: str):
    if (user := await db["user"].find_one({"username": username})) is not None:
        return user
    else:
        raise HTTPException(
            status_code=404, detail=f"User {username} wurde nicht gefunden"
        )


@router.post(
    "/user/{username}", response_description="mod User", response_model=schema.User
)
async def update_user(username: str, user: schema.UpdateUser = Body(...)):
    user = {
        key: value for key, value in user.dict().items() if value is not None
    }  # We build a new dict with theb old values
    if len(user) >= 1:
        change = await db["user"].update_one({"username": username}, {"$set": user})
        if change.modified_count == 1:
            if (
                changed := await db["user"].find_one({"username": username})
            ) is not None:
                return changed

    if (user_is_there := await db["user"].find_one({"username": username})) is not None:
        return user_is_there
    raise HTTPException(status_code=404, detail=f"Unable to find User {username}")
