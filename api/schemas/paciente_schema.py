from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional
from datetime import date

class PacienteSchema(BaseModel):
    pa_cpf: Annotated[str, Field(min_length=11, max_length=11, pattern=r'^\d{11}$')]
    pa_nome: Annotated[str, Field(min_length=3, max_length=100)]
    pa_datanasc: date
    pa_telefone: Annotated[str, Field(min_length=8, max_length=15)]
    pa_email: EmailStr
    pa_senha: Annotated[str, Field(min_length=6, max_length=100)]
    pa_endereco: Annotated[str, Field(min_length=5, max_length=255)]
    pa_historico: Optional[str] = None

    class Config:
        from_attributes = True
