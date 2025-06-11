from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class AgenteComunitarioSchema(BaseModel):
    nome: Annotated[str, Field(min_length=3, max_length=100)]
    cpf: Annotated[str, Field(min_length=11, max_length=11, pattern=r'^\d{11}$')]
    email: EmailStr
    telefone: Annotated[str, Field(min_length=8, max_length=15)]
    senha: Annotated[str, Field(min_length=6, max_length=100)]

    class Config:
        from_attributes = True
