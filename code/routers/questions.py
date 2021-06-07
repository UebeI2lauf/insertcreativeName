from fastapi import APIRouter, HTTPException, status, Body
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import schema
import random

from database import db

# set seed
random.seed(667)

# Init router instance
router = APIRouter(tags=["Fragen"])


@router.post(
    "/question", response_description="Add a question", response_model=schema.Questions
)
async def create_q(question: schema.Questions = Body(...)):
    question = jsonable_encoder(question)
    new_q = await db["question"].insert_one(question)
    lookup_new_user = await db["question"].find_one({"_id": new_q.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=lookup_new_user)


@router.get(
    "/question/{nr}",
    response_description="Look up a question",
    response_model=schema.Questions,
)
async def show_question(nr: int, current_user: sch):
    if (question := await db["question"].find_one({"nr": nr})) is not None:
        return question
    else:
        raise HTTPException(
            status_code=404, detail=f"Question {nr} wurde nicht gefunden"
        )


@router.get(
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


@router.post(
    "/question/log/{nr}",
    response_description="Answere question",
    response_model=schema.AnswereQuestion,
)
async def push_question(answere: schema.AnswereQuestion = Body(...)):
    answere = jsonable_encoder(answere)
    new_answere = await db["answere"].insert_one(answere)
    lookup = await db["answere"].find_one({"_id": new_answere.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=lookup)
