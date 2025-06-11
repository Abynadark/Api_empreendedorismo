from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone
import uuid
from sqlalchemy import Time


DIRECT_URL="postgresql://postgres.azapudafbwcfhprxvchj:meudeuspega@aws-0-sa-east-1.pooler.supabase.com:5432/postgres"

# Cria a conexão com o banco
db = create_engine(DIRECT_URL)

# Cria a base do banco de dados
Base = declarative_base()

def utcnow():
    return datetime.now(timezone.utc)


class UnidadeSaude(Base):
    __tablename__ = "unidade_de_saude"

    id_unidade = Column("id_unidade", Integer, primary_key=True, index=True)
    un_nome = Column("un_nome", String, unique=True, nullable=False)
    un_endereco = Column("un_endereco", Text, nullable=False)
    tipo_unidade = Column("tipo_unidade", String, nullable=False)
    contato = Column("contato", Text, nullable=False)
    orgao_respons = Column("orgao_respons", String, nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), default=utcnow)

 
    consultas = relationship("Consulta", back_populates="unidade")

    def __init__(self, un_nome, un_endereco, tipo_unidade, contato, orgao_respons):
        self.un_nome = un_nome
        self.un_endereco = un_endereco
        self.tipo_unidade = tipo_unidade
        self.contato = contato
        self.orgao_respons = orgao_respons


class ProfissionalSaude(Base):
    __tablename__ = "profissional_saude"

    ps_id = Column("ps_id", Integer, primary_key=True, index=True)
    ps_nome = Column("ps_nome", String, nullable=False)
    ps_cpf = Column("ps_cpf", String, unique=True, nullable=False)
    ps_especialidade = Column("ps_especialidade", String, nullable=False)
    ps_email = Column("ps_email", String, unique=True, nullable=False)
    ps_telefone = Column("ps_telefone", String, nullable=False)
    ps_registro_profissional = Column("ps_registro_profissional", String, unique=True, nullable=False)
    ps_senha = Column("ps_senha", String, nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), default=utcnow)
    updated_at = Column("updated_at", DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    consultas = relationship("Consulta", back_populates="profissional")
    

    def __init__(self, ps_nome, ps_cpf, ps_especialidade, ps_email, ps_telefone, ps_registro_profissional, ps_senha):
        self.ps_nome = ps_nome
        self.ps_cpf = ps_cpf
        self.ps_especialidade = ps_especialidade
        self.ps_email = ps_email
        self.ps_telefone = ps_telefone
        self.ps_registro_profissional = ps_registro_profissional
        self.ps_senha = ps_senha


class Paciente(Base):
    __tablename__ = "paciente"

    pa_id = Column("pa_id", Integer, primary_key=True, index=True, autoincrement=True)
    pa_cpf = Column("pa_cpf", String, unique=True, nullable=False)
    pa_nome = Column("pa_nome", String, nullable=False)
    pa_datanasc = Column("pa_datanasc", Date, nullable=False)
    pa_telefone = Column("pa_telefone", String, nullable=False)
    pa_email = Column("pa_email", String, unique=True, nullable=False)
    pa_senha = Column("pa_senha", String, nullable=False)
    pa_endereco = Column("pa_endereco", Text, nullable=False)
    pa_historico = Column("pa_historico", Text)
    created_at = Column("created_at", DateTime(timezone=True), default=utcnow)
    updated_at = Column("updated_at", DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    agendamentos = relationship("Agendamento", back_populates="paciente")
    notificacoes = relationship("Notificacao", back_populates="paciente")

    def __init__(self, pa_cpf, pa_nome, pa_datanasc, pa_telefone, pa_email, pa_senha, pa_endereco, pa_historico):
        self.pa_cpf = pa_cpf
        self.pa_nome = pa_nome
        self.pa_datanasc = pa_datanasc
        self.pa_telefone = pa_telefone
        self.pa_email = pa_email
        self.pa_senha = pa_senha
        self.pa_endereco = pa_endereco
        self.pa_historico = pa_historico


class Agendamento(Base):
    __tablename__ = "agendamento"

    id_agendamento = Column("id_agendamento", Integer, primary_key=True, index=True)
    id_consulta = Column("id_consulta", Integer, ForeignKey("consulta.id_consulta"))  
    id_paciente = Column("id_paciente", Integer, ForeignKey("paciente.pa_id"))  
    data_inicio = Column("data_inicio", DateTime)
    data_fim = Column("data_fim", DateTime)
    observacoes = Column("observacoes", Text, nullable=False)
    status = Column("status", String, nullable=False)

    paciente = relationship("Paciente", back_populates="agendamentos")  
    consulta = relationship("Consulta", back_populates="agendamentos" )  

    def __init__(self, id_consulta, id_paciente, data_inicio, data_fim, observacoes, status= "Pendende"):
        self.id_consulta = id_consulta
        self.id_paciente = id_paciente
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.observacoes = observacoes
        self.status = status



class Consulta(Base):
    __tablename__ = "consulta"

    id_consulta = Column("id_consulta", Integer, primary_key=True, index=True)
    id_profissional = Column("id_profissional", Integer, ForeignKey("profissional_saude.ps_id"))
    id_unidade = Column("id_unidade", Integer, ForeignKey("unidade_de_saude.id_unidade"))
    data_consulta = Column("data_consulta", Date, nullable=False)
    hora_consulta = Column("hora_consulta", Time, nullable=False)
    status_consulta = Column("status_consulta", String, nullable=False)
    tipo_consulta = Column("tipo_consulta", String, nullable=False)
    observacoes = Column("observacoes", Text, nullable=False)
    criada_por = Column("criada_por", String, nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), default=utcnow)
    updated_at = Column("updated_at", DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    
    
    agendamentos = relationship("Agendamento", back_populates="consulta")

    profissional = relationship("ProfissionalSaude", back_populates="consultas")
    unidade = relationship("UnidadeSaude", back_populates="consultas")
    notificacoes = relationship("Notificacao", back_populates="consulta")

    def __init__(self, id_profissional, id_unidade, data_consulta, hora_consulta, status_consulta, tipo_consulta, observacoes, criada_por):
        self.id_profissional = id_profissional
        self.id_unidade = id_unidade
        self.data_consulta = data_consulta
        self.hora_consulta = hora_consulta
        self.status_consulta = status_consulta
        self.tipo_consulta = tipo_consulta
        self.observacoes = observacoes
        self.criada_por = criada_por


class Notificacao(Base):
    __tablename__ = "notificacao"

    id_notificacao = Column("id_notificacao", Integer, primary_key=True, index=True, autoincrement=True)
    id_paciente = Column("id_paciente", Integer, ForeignKey("paciente.pa_id"))
    id_consulta = Column("id_consulta", Integer, ForeignKey("consulta.id_consulta"))
    canal_comunicacao = Column("canal_comunicacao", String)
    tipo_notificacao = Column("tipo_notificacao", String)
    conteudo = Column("conteudo", Text)
    data_envio = Column("data_envio", DateTime)
    enviado = Column("enviado", Boolean)

    consulta = relationship("Consulta", back_populates="notificacoes")
    paciente = relationship("Paciente", back_populates="notificacoes")

    def __init__(self, id_paciente, id_consulta, canal_comunicacao, tipo_notificacao, conteudo, data_envio, enviado):
        self.id_paciente = id_paciente
        self.id_consulta = id_consulta
        self.canal_comunicacao = canal_comunicacao
        self.tipo_notificacao = tipo_notificacao
        self.conteudo = conteudo
        self.data_envio = data_envio
        self.enviado = enviado


class AgenteComunitario(Base):
    __tablename__ = "agente_comunitario"

    id_acs = Column("id_acs", Integer, primary_key=True, index=True)
    nome = Column("nome", String)
    cpf = Column("cpf", String, unique=True, nullable=False)
    email = Column("email", String, unique=True, nullable=False)
    senha = Column("senha", String, nullable=False)
    telefone = Column("telefone", String, nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), default=utcnow)

    def __init__(self, nome, cpf, email, senha, telefone):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.telefone = telefone
