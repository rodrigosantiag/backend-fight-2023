from http import HTTPStatus

from fastapi import FastAPI, Request

from models import Pessoa, get_session
from schemas import PessoaSchema
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.exc import IntegrityError, DataError

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY

    for item in exc.errors():
        message = item["msg"]

        if "Input should be" in message and item["input"] is not None:
            status_code = HTTPStatus.BAD_REQUEST
            break

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({"errors": exc.errors()}),
    )


@app.exception_handler(IntegrityError)
async def unique_index_exception_error(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"errors": str(exc)}),
    )


@app.exception_handler(DataError)
async def exceed_column_size_exception_error(request: Request, exc: DataError):
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"errors": str(exc)}),
    )


@app.get("/")
def hello_world():
    return {"hello": "world"}


@app.post("/pessoas")
async def add_person(data: PessoaSchema, db_session: Session = Depends(get_session)):
    person = Pessoa(**data.model_dump())
    db_session.add(person)
    db_session.commit()

    headers = {"Location": f"/pessoas/{str(person.id)}"}

    return JSONResponse(
        status_code=HTTPStatus.CREATED, content={"uid": str(person.id)}, headers=headers
    )
