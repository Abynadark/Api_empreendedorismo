from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from dependencies import pegar_sessao
from models import Agendamento, Consulta, Paciente
from schemas.agendamento_schema import AgendamentoResponse, CriarAgendamentoRequest, AtualizarObservacaoRequest

agendamento_router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

# POST /agendamentos/novo
@agendamento_router.post("/novo", response_model=AgendamentoResponse)
def criar_agendamento(dados: CriarAgendamentoRequest, session: Session = Depends(pegar_sessao)):
    paciente = session.query(Paciente).filter_by(pa_cpf=dados.cpf_paciente).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    consulta = session.query(Consulta).filter_by(id_consulta=dados.id_consulta).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    agendamento = Agendamento(
        id_consulta=dados.id_consulta,
        id_paciente=paciente.pa_id,
        data_inicio=None,
        data_fim=None,
        observacoes=dados.observacoes,
        status="pendente"
    )

    consulta.status_consulta = "agendada"

    session.add(agendamento)
    session.commit()
    session.refresh(agendamento)

    return AgendamentoResponse(
        id_agendamento=agendamento.id_agendamento,
        cpf_paciente=agendamento.paciente.pa_cpf,
        id_consulta=agendamento.id_consulta,
        data_inicio=agendamento.data_inicio,
        data_fim=agendamento.data_fim,
        observacoes=agendamento.observacoes,
        status=agendamento.status,
        nome_paciente=agendamento.paciente.pa_nome,
        nome_profissional=agendamento.consulta.profissional.ps_nome,
        nome_unidade=agendamento.consulta.unidade.un_nome,
        endereco_unidade=agendamento.consulta.unidade.un_endereco,
        data_consulta=agendamento.consulta.data_consulta,
        hora_consulta=agendamento.consulta.hora_consulta
    )

# PATCH /agendamentos/{id}/entrada
@agendamento_router.patch("/{id}/entrada", response_model=AgendamentoResponse)
def registrar_entrada(id: int, session: Session = Depends(pegar_sessao)):
    agendamento = session.query(Agendamento).get(id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    agendamento.data_inicio = datetime.now()
    agendamento.status = "pendente"
    agendamento.consulta.status_consulta = "em atendimento"

    session.commit()
    session.refresh(agendamento)
    
    return AgendamentoResponse(
        id_agendamento=agendamento.id_agendamento,
        cpf_paciente=agendamento.paciente.pa_cpf,
        id_consulta=agendamento.id_consulta,
        data_inicio=agendamento.data_inicio,
        data_fim=agendamento.data_fim,
        observacoes=agendamento.observacoes,
        status=agendamento.status,
        nome_paciente=agendamento.paciente.pa_nome,
        nome_profissional=agendamento.consulta.profissional.ps_nome,
        nome_unidade=agendamento.consulta.unidade.un_nome,
        endereco_unidade=agendamento.consulta.unidade.un_endereco,
        data_consulta=agendamento.consulta.data_consulta,
        hora_consulta=agendamento.consulta.hora_consulta
    )

# PATCH /agendamentos/{id}/saida
@agendamento_router.patch("/{id}/saida", response_model=AgendamentoResponse)
def registrar_saida(id: int, session: Session = Depends(pegar_sessao)):
    agendamento = session.query(Agendamento).get(id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    agendamento.data_fim = datetime.now()
    agendamento.status = "concluido"
    agendamento.consulta.status_consulta = "finalizada"

    session.commit()
    session.refresh(agendamento)
    
    return AgendamentoResponse(
        id_agendamento=agendamento.id_agendamento,
        cpf_paciente=agendamento.paciente.pa_cpf,
        id_consulta=agendamento.id_consulta,
        data_inicio=agendamento.data_inicio,
        data_fim=agendamento.data_fim,
        observacoes=agendamento.observacoes,
        status=agendamento.status,
        nome_paciente=agendamento.paciente.pa_nome,
        nome_profissional=agendamento.consulta.profissional.ps_nome,
        nome_unidade=agendamento.consulta.unidade.un_nome,
        endereco_unidade=agendamento.consulta.unidade.un_endereco,
        data_consulta=agendamento.consulta.data_consulta,
        hora_consulta=agendamento.consulta.hora_consulta
    )

# GET /agendamentos/
@agendamento_router.get("/", response_model=list[AgendamentoResponse])
def listar_agendamentos(
    cpf_paciente: str = None,
    status: str = None,
    session: Session = Depends(pegar_sessao)
):
    query = session.query(Agendamento)

    if cpf_paciente:
        paciente = session.query(Paciente).filter_by(pa_cpf=cpf_paciente).first()
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        query = query.filter(Agendamento.id_paciente == paciente.pa_id)

    if status:
        query = query.filter(Agendamento.status == status)

    agendamentos = query.all()

    return [
    AgendamentoResponse(
        id_agendamento=ag.id_agendamento,
        cpf_paciente=ag.paciente.pa_cpf,
        id_consulta=ag.id_consulta,
        data_inicio=ag.data_inicio,
        data_fim=ag.data_fim,
        observacoes=ag.observacoes,
        status=ag.status,
        nome_paciente=ag.paciente.pa_nome,
        nome_profissional=ag.consulta.profissional.ps_nome,
        nome_unidade=ag.consulta.unidade.un_nome,
        endereco_unidade=ag.consulta.unidade.un_endereco,
        data_consulta=ag.consulta.data_consulta,
        hora_consulta=ag.consulta.hora_consulta
    )
    for ag in agendamentos
]

    

# PATCH /agendamentos/{id}/observacoes
@agendamento_router.patch("/{id}/observacoes", response_model=AgendamentoResponse)
def atualizar_observacoes(id: int, dados: AtualizarObservacaoRequest, session: Session = Depends(pegar_sessao)):
    agendamento = session.query(Agendamento).get(id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    agendamento.observacoes = dados.observacoes
    session.commit()
    session.refresh(agendamento)

    return AgendamentoResponse(
        id_agendamento=agendamento.id_agendamento,
        cpf_paciente=agendamento.paciente.pa_cpf,
        id_consulta=agendamento.id_consulta,
        data_inicio=agendamento.data_inicio,
        data_fim=agendamento.data_fim,
        observacoes=agendamento.observacoes,
        status=agendamento.status,
        nome_paciente=agendamento.paciente.pa_nome,
        nome_profissional=agendamento.consulta.profissional.ps_nome,
        nome_unidade=agendamento.consulta.unidade.un_nome,
        endereco_unidade=agendamento.consulta.unidade.un_endereco,
        data_consulta=agendamento.consulta.data_consulta,  # vírgula aqui
        hora_consulta=agendamento.consulta.hora_consulta
)


# DELETE /agendamentos/{id}
@agendamento_router.delete("/{id}")
def deletar_agendamento(id: int, session: Session = Depends(pegar_sessao)):
    agendamento = session.query(Agendamento).get(id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    session.delete(agendamento)
    session.commit()
    return {"mensagem": f"Agendamento {id} deletado com sucesso"}
