# routes/notificacao_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from models import Notificacao, Paciente, Consulta
from dependencies import pegar_sessao
from schemas.notificacao_schema import NotificacaoCreateSchema, NotificacaoResponseSchema

notificacao_router = APIRouter(prefix="/notificacoes", tags=["notificações"])

@notificacao_router.post("/", response_model=NotificacaoResponseSchema)
def criar_notificacao(dados: NotificacaoCreateSchema, session: Session = Depends(pegar_sessao)):
    paciente = session.query(Paciente).filter_by(pa_cpf=dados.cpf_paciente).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    consulta = session.query(Consulta).filter_by(id_consulta=dados.id_consulta).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    nova = Notificacao(
        id_paciente=paciente.pa_id,
        id_consulta=dados.id_consulta,
        canal_comunicacao=dados.canal_comunicacao,
        tipo_notificacao=dados.tipo_notificacao,
        conteudo=dados.conteudo,
        data_envio=datetime.now(),
        enviado=True
    )
    session.add(nova)
    session.commit()
    session.refresh(nova)

    return NotificacaoResponseSchema(
        id_notificacao=nova.id_notificacao,
        nome_paciente=paciente.pa_nome,
        canal_comunicacao=nova.canal_comunicacao,
        tipo_notificacao=nova.tipo_notificacao,
        conteudo=nova.conteudo,
        data_envio=nova.data_envio,
        enviado=nova.enviado
    )

@notificacao_router.get("/", response_model=list[NotificacaoResponseSchema])
def listar_notificacoes(session: Session = Depends(pegar_sessao)):
    notificacoes = session.query(Notificacao).join(Paciente).all()
    return [
        NotificacaoResponseSchema(
            id_notificacao=n.id_notificacao,
            nome_paciente=n.paciente.pa_nome,
            canal_comunicacao=n.canal_comunicacao,
            tipo_notificacao=n.tipo_notificacao,
            conteudo=n.conteudo,
            data_envio=n.data_envio,
            enviado=n.enviado
        )
        for n in notificacoes
    ]
# Continuação de routes/notificacao_routes.py

@notificacao_router.delete("/{id_notificacao}")
def deletar_notificacao(id_notificacao: int, session: Session = Depends(pegar_sessao)):
    notificacao = session.query(Notificacao).filter_by(id_notificacao=id_notificacao).first()
    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")

    session.delete(notificacao)
    session.commit()
    return {"detail": "Notificação deletada com sucesso."}

@notificacao_router.get("/paciente/{cpf_paciente}", response_model=list[NotificacaoResponseSchema])
def listar_notificacoes_por_paciente(cpf_paciente: str, session: Session = Depends(pegar_sessao)):
    paciente = session.query(Paciente).filter_by(pa_cpf=cpf_paciente).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    notificacoes = session.query(Notificacao).filter_by(id_paciente=paciente.pa_id).all()
    return [
        NotificacaoResponseSchema(
            id_notificacao=n.id_notificacao,
            nome_paciente=paciente.pa_nome,
            canal_comunicacao=n.canal_comunicacao,
            tipo_notificacao=n.tipo_notificacao,
            conteudo=n.conteudo,
            data_envio=n.data_envio,
            enviado=n.enviado
        )
        for n in notificacoes
    ]
