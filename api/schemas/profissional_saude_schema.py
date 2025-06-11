from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class ProfissionalSaudeSchema(BaseModel):
    ps_nome: Annotated[str, Field(min_length=3, max_length=100)]
    ps_cpf: Annotated[str, Field(min_length=11, max_length=11, pattern=r'^\d{11}$')]
    ps_especialidade: Annotated[str, Field(min_length=2, max_length=100)]
    ps_email: EmailStr
    ps_telefone: Annotated[str, Field(min_length=8, max_length=15)]
    ps_registro_profissional: str = Field(..., pattern=r"^\d{4,6}-[A-Z]{2}$", description="Formato: 12345-SP")
    ps_senha: Annotated[str, Field(min_length=6, max_length=100)]

    class Config:
        from_attributes = True
