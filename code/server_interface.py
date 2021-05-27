# Import fastAPI modules
from fastapi import FastAPI, status, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
import random


# Import MongoDB module
from database import db


# import local files ,some highlighting seems to be buggy depends on formatter
import schema

# set seed
random.seed(667)

# create the web application itself
webapp = FastAPI()


@webapp.post("/user", response_description="Add a user", response_model=schema.User)
async def create_user(user: schema.User = Body(...)):
    user = jsonable_encoder(user)
    new_user = await db["user"].insert_one(user)
    lookup_new_user = await db["user"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=lookup_new_user)


@webapp.get(
    "/user/{username}", response_description="Lookup a User", response_model=schema.User
)
async def show_student(username: str):
    if (user := await db["user"].find_one({"username": username})) is not None:
        return user
    else:
        raise HTTPException(
            status_code=404, detail=f"User {username} wurde nicht gefunden"
        )


@webapp.post(
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


@webapp.post(
    "/question", response_description="Add a question", response_model=schema.Questions
)
async def create_q(question: schema.Questions = Body(...)):
    question = jsonable_encoder(question)
    new_q = await db["question"].insert_one(question)
    lookup_new_user = await db["question"].find_one({"_id": new_q.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=lookup_new_user)


@webapp.get(
    "/question/{nr}",
    response_description="Look up a question",
    response_model=schema.Questions,
)
async def show_question(nr: int):
    if (question := await db["question"].find_one({"nr": nr})) is not None:
        return question
    else:
        raise HTTPException(
            status_code=404, detail=f"Question {nr} wurde nicht gefunden"
        )


@webapp.get(
    "/question/",
    response_description="Get a random question",
    response_model=schema.RNDQuestions,
)
async def getRNDquestion(raise_error: bool):
    if raise_error is not False:
        raise HTTPException(
            status_code=404, detail="Any unexpected event accured pls try again"
        )
    else:
        questions = await db["question"].find().to_list(length=100)
        lenght = len(questions)
        selection = random.randint(0, lenght - 1)
        """ raise HTTPException(
            status_code=404,
            detail="Any unexpected event accured pls try again is was True",
        ) """
        return questions[selection]


@webapp.post(
    "/questions/log/{nr}",
    response_description="Answere question",
    response_model=schema.AnswereQuestion,
)
async def push_question(answere: schema.AnswereQuestion = Body(...)):
    answere = jsonable_encoder(answere)
    new_answere = await db["answere"].insert_one(answere)
    lookup = await db["answere"].find_one({"_id": new_answere.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=lookup)
