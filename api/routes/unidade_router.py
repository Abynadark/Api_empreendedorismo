from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models import UnidadeSaude
from schemas.unidade_schema import UnidadeSaudeCreateSchema, UnidadeSaudeResponseSchema
from dependencies import pegar_sessao
from typing import List

unidade_router = APIRouter(prefix="/unidades", tags=["unidades"])

@unidade_router.post("/", response_model=UnidadeSaudeResponseSchema)
def criar_unidade(unidade_data: UnidadeSaudeCreateSchema, session: Session = Depends(pegar_sessao)):
    unidade_existente = session.query(UnidadeSaude).filter(UnidadeSaude.un_nome == unidade_data.un_nome).first()
    if unidade_existente:
        raise HTTPException(status_code=400, detail="Unidade com esse nome já existe")

    nova_unidade = UnidadeSaude(
        un_nome=unidade_data.un_nome,
        un_endereco=unidade_data.un_endereco,
        tipo_unidade=unidade_data.tipo_unidade,
        contato=unidade_data.contato,
        orgao_respons=unidade_data.orgao_respons,
    )

    session.add(nova_unidade)
    session.commit()
    session.refresh(nova_unidade)

    return nova_unidade

@unidade_router.get("/", response_model=List[UnidadeSaudeResponseSchema])
def listar_unidades(session: Session = Depends(pegar_sessao)):
    return session.query(UnidadeSaude).all()

@unidade_router.get("/buscar", response_model=List[UnidadeSaudeResponseSchema])
def buscar_por_nome(nome: str = Query(..., min_length=1), session: Session = Depends(pegar_sessao)):
    resultados = session.query(UnidadeSaude).filter(UnidadeSaude.un_nome.ilike(f"%{nome}%")).all()
    if not resultados:
        raise HTTPException(status_code=404, detail="Nenhuma unidade encontrada com esse nome")
    return resultados

@unidade_router.delete("/deletar_por_nome")
def deletar_unidade_por_nome(nome: str = Query(..., min_length=1), session: Session = Depends(pegar_sessao)):
    unidade = session.query(UnidadeSaude).filter(UnidadeSaude.un_nome.ilike(nome)).first()
    
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade não encontrada com esse nome")
    
    session.delete(unidade)
    session.commit()
    
    return {"mensagem": f"Unidade '{nome}' deletada com sucesso"}
