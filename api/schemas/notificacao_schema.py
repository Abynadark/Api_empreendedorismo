# schemas/notificacao_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class NotificacaoCreateSchema(BaseModel):
    cpf_paciente: str = Field(..., example="12345678900")
    id_consulta: int = Field(..., example=1)
    canal_comunicacao: str = Field(..., example="email")
    tipo_notificacao: str = Field(..., example="lembrete")
    conteudo: str = Field(..., example="Sua consulta está agendada para amanhã às 14h.")
    
class NotificacaoResponseSchema(BaseModel):
    id_notificacao: int
    nome_paciente: str
    canal_comunicacao: str
    tipo_notificacao: str
    conteudo: str
    data_envio: Optional[datetime]
    enviado: bool

    class Config:
        from_attributes = True
