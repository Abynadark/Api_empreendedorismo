from pydantic import BaseModel, Field
from datetime import datetime, date, time
from typing import Optional

class CriarAgendamentoRequest(BaseModel):
    cpf_paciente: str = Field(..., example="12345678901")
    id_consulta: int = Field(..., example=1)
    observacoes: str = Field(..., example="Primeira consulta")

class AtualizarObservacaoRequest(BaseModel):
    observacoes: str = Field(..., example="Nova observação")

class AgendamentoResponse(BaseModel):
    id_agendamento: int
    status: str
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    observacoes: str

    nome_paciente: str
    nome_profissional: str
    nome_unidade: str
    endereco_unidade: str
    data_consulta: date
    hora_consulta: time

    class Config:
        from_attributes = True
