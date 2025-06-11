from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class PacienteLoginSchema(BaseModel):
    pa_email: EmailStr
    pa_senha: Annotated[str, Field(min_length=6, max_length=100)]

    class Config:
        from_attributes = True

class ProfissionalSaudeLoginSchema(BaseModel):
    ps_email: EmailStr
    ps_senha: Annotated[str, Field(min_length=6, max_length=100)]

    class Config:
        from_attributes = True

class AgenteComunitarioLoginSchema(BaseModel):
    email: EmailStr
    senha: Annotated[str, Field(min_length=6, max_length=100)]

    class Config:
        from_attributes = True
