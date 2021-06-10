from fastapi import APIRouter, HTTPException, status, Body, Depends
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import time
import schema
import random
import security

from database import db

# set seed
random.seed(667)

# Init router instance
router = APIRouter(tags=["Fragen"])


@router.post(
    "/question", response_description="Add a question", response_model=schema.Questions
)
async def create_q(
    question: schema.Questions = Body(...),
    current_user: schema.TokenData = Depends(security.get_this_user),
):
    question = jsonable_encoder(question)
    new_q = await db["question"].insert_one(question)
    lookup_new_user = await db["question"].find_one({"_id": new_q.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=lookup_new_user)


@router.get(
    "/question/{nr}",
    response_description="Look up a question",
    response_model=schema.Questions,
)
async def show_question(
    nr: int, current_user: schema.TokenData = Depends(security.get_this_user)
):
    if (question := await db["question"].find_one({"nr": nr})) is not None:
        return question
    else:
        raise HTTPException(
            status_code=404, detail=f"Question {nr} wurde nicht gefunden"
        )


@router.get(
    "/question/",
    response_description="Get next question",
    response_model=schema.RNDQuestions,
)
async def get_next_question(
    raise_error: bool, current_user: schema.TokenData = Depends(security.get_this_user)
):
    user = await db["user"].find_one({"username": current_user.username})
    id = user["question_id"]
    if raise_error is not False:
        error_codes = [400, 401, 403, 404, 408]
        code = random.choice(error_codes)
        db["log"].inster_one(
            {"username": current_user.username, "code": code, "question_id": (id + 1)}
        )
        if code == 408:
            time.sleep(30)
        raise HTTPException(
            status_code=code, detail="Any unexpected event accured pls try again"
        )
    else:
        question = await db["question"].find_one({"nr": id})
        return question


@router.post(
    "/question/log/{nr}",
    response_description="Answere question",
    response_model=schema.AnswereQuestion,
)
async def push_question(
    answere: schema.AnswereQuestion = Body(...),
    current_user: schema.TokenData = Depends(security.get_this_user),
):
    answere = jsonable_encoder(answere)
    new_answere = await db["answere"].insert_one(answere)
    lookup = await db["answere"].find_one({"_id": new_answere.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=lookup)
