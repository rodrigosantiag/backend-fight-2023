from datetime import date
from typing import List, Optional

from pydantic import BaseModel, model_validator


class PessoaSchema(BaseModel):
    apelido: str
    nome: str
    nascimento: date
    stack: Optional[List[str]] = None

    @model_validator(mode="after")
    def validate_fields(self):
        if self.stack and any(len(stack) > 32 for stack in self.stack):
            raise ValueError("Stack cannot have more than 32 characters")

        if len(self.apelido) > 32:
            raise ValueError("Apelido cannot have more than 32 characters")

        if len(self.nome) > 100:
            raise ValueError("Nome cannot have more than 32 characters")

        return self
