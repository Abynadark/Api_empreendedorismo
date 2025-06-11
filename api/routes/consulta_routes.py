from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Consulta, ProfissionalSaude, UnidadeSaude
from schemas.consulta_schema import ConsultaCreateSchema, ConsultaResponseSchema
from dependencies import pegar_sessao

consulta_router = APIRouter(prefix="/consultas", tags=["consultas"])

@consulta_router.post("/", response_model=ConsultaResponseSchema)
def criar_consulta(consulta: ConsultaCreateSchema, session: Session = Depends(pegar_sessao)):
    profissional = session.query(ProfissionalSaude).filter_by(ps_registro_profissional=consulta.crm_profissional).first()
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional de saúde não encontrado")

    unidade = session.query(UnidadeSaude).filter_by(un_nome=consulta.nome_unidade).first()
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade de saúde não encontrada")

    nova_consulta = Consulta(
        id_profissional=profissional.ps_id,
        id_unidade=unidade.id_unidade,
        data_consulta=consulta.data_consulta,
        hora_consulta=consulta.hora_consulta,
        status_consulta=consulta.status_consulta,
        tipo_consulta=consulta.tipo_consulta,
        observacoes=consulta.observacoes,
        criada_por=consulta.criada_por
    )

    session.add(nova_consulta)
    session.commit()
    session.refresh(nova_consulta)

    return ConsultaResponseSchema(
        id_consulta=nova_consulta.id_consulta,
        profissional_nome=profissional.ps_nome,
        unidade_nome=unidade.un_nome,
        data_consulta=nova_consulta.data_consulta,
        hora_consulta=nova_consulta.hora_consulta,
        status_consulta=nova_consulta.status_consulta,
        tipo_consulta=nova_consulta.tipo_consulta,
        observacoes=nova_consulta.observacoes,
        criada_por=nova_consulta.criada_por
    )

@consulta_router.get("/", response_model=list[ConsultaResponseSchema])
def listar_consultas(session: Session = Depends(pegar_sessao)):
    consultas = session.query(Consulta).all()
    return [
        ConsultaResponseSchema(
            id_consulta=c.id_consulta,
            profissional_nome=c.profissional.ps_nome,
            unidade_nome=c.unidade.un_nome,
            data_consulta=c.data_consulta,
            hora_consulta=c.hora_consulta,
            status_consulta=c.status_consulta,
            tipo_consulta=c.tipo_consulta,
            observacoes=c.observacoes,
            criada_por=c.criada_por
        ) for c in consultas
    ]

@consulta_router.get("/filtro", response_model=list[ConsultaResponseSchema])
def filtrar_consultas(
    crm_profissional: str = None,
    nome_unidade: str = None,
    session: Session = Depends(pegar_sessao)
):
    query = session.query(Consulta)

    if crm_profissional:
        profissional = session.query(ProfissionalSaude).filter_by(ps_registro_profissional=crm_profissional).first()
        if not profissional:
            raise HTTPException(status_code=404, detail="Profissional não encontrado")
        query = query.filter(Consulta.id_profissional == profissional.ps_id)

    if nome_unidade:
        unidade = session.query(UnidadeSaude).filter_by(un_nome=nome_unidade).first()
        if not unidade:
            raise HTTPException(status_code=404, detail="Unidade não encontrada")
        query = query.filter(Consulta.id_unidade == unidade.id_unidade)

    consultas = query.all()
    return [
        ConsultaResponseSchema(
            id_consulta=c.id_consulta,
            profissional_nome=c.profissional.ps_nome,
            unidade_nome=c.unidade.un_nome,
            data_consulta=c.data_consulta,
            hora_consulta=c.hora_consulta,
            status_consulta=c.status_consulta,
            tipo_consulta=c.tipo_consulta,
            observacoes=c.observacoes,
            criada_por=c.criada_por
        ) for c in consultas
    ]

@consulta_router.delete("/{id_consulta}")
def deletar_consulta(id_consulta: int, session: Session = Depends(pegar_sessao)):
    consulta = session.query(Consulta).filter_by(id_consulta=id_consulta).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    session.delete(consulta)
    session.commit()
    return {"mensagem": f"Consulta {id_consulta} deletada com sucesso."}
