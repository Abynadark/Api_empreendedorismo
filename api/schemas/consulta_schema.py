from pydantic import BaseModel, Field
from datetime import date, time

from pydantic import BaseModel, Field
from datetime import date, time

class ConsultaCreateSchema(BaseModel):
    crm_profissional: str = Field(..., pattern=r"^\d{4,6}-[A-Z]{2}$", description="Ex: 12345-SP")
    nome_unidade: str = Field(..., description="Nome exato da unidade de saúde")
    data_consulta: date
    hora_consulta: time
    status_consulta: str
    tipo_consulta: str
    observacoes: str
    criada_por: str


class ConsultaResponseSchema(BaseModel):
    id_consulta: int
    profissional_nome: str
    unidade_nome: str
    data_consulta: date
    hora_consulta: time
    status_consulta: str
    tipo_consulta: str
    observacoes: str
    criada_por: str

    class Config:
        from_attributes = True
