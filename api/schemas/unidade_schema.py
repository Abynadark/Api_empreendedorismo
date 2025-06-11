from pydantic import BaseModel, Field
from datetime import datetime

class UnidadeSaudeCreateSchema(BaseModel):
    un_nome: str
    un_endereco: str
    tipo_unidade: str
    contato: str
    orgao_respons: str

class UnidadeSaudeResponseSchema(BaseModel):
    id_unidade: int
    un_nome: str
    un_endereco: str
    tipo_unidade: str
    contato: str
    orgao_respons: str
    created_at: datetime

    class Config:
        from_attributes = True  # Para funcionar com SQLAlchemy
