from datetime import date
from typing import List

from pydantic import BaseModel, model_validator


class PessoaSchema(BaseModel):
    apelido: str
    nome: str
    nascimento: date
    stack: List[str] = None

    @model_validator(mode="after")
    def validate_stacks(self):
        if self.stack and any(len(stack) > 32 for stack in self.stack):
            raise ValueError("Stack cannot have more than 32 characters")

        return self
