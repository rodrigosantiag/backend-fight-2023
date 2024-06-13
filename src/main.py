import json
from http import HTTPStatus

from fastapi import FastAPI, Request

from src.models import Pessoa, get_session
from src.schemas import PessoaSchema
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

app = FastAPI()


def serialize(data):
    return json.dumps(data, default=str)


def deserialize(data):
    return json.loads(data)


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


@app.get("/")
def hello_world():
    return {"hello": "world"}


@app.post("/pessoas")
async def add_person(
    data: PessoaSchema, db_session: Session = Depends(get_session)
) -> JSONResponse:
    # cached_person = cache.get(data.apelido)
    #
    # if cached_person:
    #     return JSONResponse(
    #         status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
    #         content=jsonable_encoder({"errors": "error"}),
    #     )

    existed_person = db_session.query(Pessoa).filter(Pessoa.apelido == data.apelido).first()

    if existed_person:
        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"errors": "error"}),
        )

    person = Pessoa(**data.model_dump())

    # cache.set(person.apelido, person.apelido)
    # cache.set(str(person.id), serialize(person.__dict__))

    db_session.add(person)
    db_session.commit()

    headers = {"Location": f"/pessoas/{str(person.id)}"}

    return JSONResponse(
        status_code=HTTPStatus.CREATED, content={"uid": str(person.id)}, headers=headers
    )


@app.get("/pessoas/{uid}")
async def get_person(uid: str, db_session: Session = Depends(get_session)) -> JSONResponse:
    # cached_person = cache.get(uid)
    #
    # if cached_person:
    #     return JSONResponse(status_code=HTTPStatus.OK, content=deserialize(cached_person))

    statement = select(Pessoa).where(Pessoa.id == uid).limit(1)
    person = db_session.execute(statement).first()

    if not person:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "Not found"})

    person = person[0]
    # person_data = person.__dict__
    # cache.set(person.apelido, person.apelido)
    # cache.set(str(person.id), serialize(person_data))

    response = {
        "id": str(person.id),
        "apelido": person.apelido,
        "nome": person.nome,
        "nascimento": str(person.nascimento),
        "stack": Pessoa.build_stack_as_list(person.stack),
    }

    return JSONResponse(status_code=HTTPStatus.OK, content=response)


@app.get("/pessoas")
async def get_people_by_term(
    t: str | None = None, db_session: Session = Depends(get_session)
) -> JSONResponse:
    if not t:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "error"})

    result = []

    people = db_session.query(Pessoa).filter(Pessoa.searchable.ilike(f"%{t}%")).limit(50).all()

    for person in people:
        result.append(
            {
                "id": str(person.id),
                "apelido": person.apelido,
                "nome": person.nome,
                "nascimento": person.nascimento.isoformat(),
                "stack": Pessoa.build_stack_as_list(person.stack),
            }
        )

    return JSONResponse(status_code=HTTPStatus.OK, content=result)


@app.get("/contagem-pessoas", status_code=HTTPStatus.OK)
async def count_people(db_session: Session = Depends(get_session)):
    return db_session.query(Pessoa).count()
