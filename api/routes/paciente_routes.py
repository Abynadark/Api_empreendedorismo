from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from models import Paciente
from dependencies import pegar_sessao
from main import bcript_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas.paciente_schema import PacienteSchema
from schemas.login_schemas import PacienteLoginSchema

paciente_router = APIRouter(prefix="/paciente/sistema", tags=["pacientes"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/paciente/sistema/login")

def criar_token(id_paciente: int):
    brasil_tz = timezone(timedelta(hours=-3))
    expiracao = datetime.now(brasil_tz) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(id_paciente), "exp": expiracao}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_paciente = payload.get("sub")
        if id_paciente is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return id_paciente
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado ou inválido")

def autenticar_paciente(email: str, senha: str, session: Session):
    paciente = session.query(Paciente).filter(Paciente.pa_email == email).first()
    if not paciente:
        return None, "Paciente não encontrado"
    if not bcript_context.verify(senha, paciente.pa_senha):
        return None, "Credenciais inválidas"
    return paciente, None

@paciente_router.post("/criar_conta")
async def criar_conta(paciente_schema: PacienteSchema, session: Session = Depends(pegar_sessao)):
    paciente = session.query(Paciente).filter(Paciente.pa_cpf == paciente_schema.pa_cpf).first()
    if paciente:
        raise HTTPException(status_code=400, detail="Já existe paciente cadastrado com esse CPF")

    senha_criptografada = bcript_context.hash(paciente_schema.pa_senha)
    novo_paciente = Paciente(
        paciente_schema.pa_cpf,
        paciente_schema.pa_nome,
        paciente_schema.pa_datanasc,
        paciente_schema.pa_telefone,
        paciente_schema.pa_email,
        senha_criptografada,
        paciente_schema.pa_endereco,
        paciente_schema.pa_historico
    )
    session.add(novo_paciente)
    session.commit()
    session.close()

    return {"mensagem": f"Paciente de CPF {paciente_schema.pa_cpf} cadastrado com sucesso."}

@paciente_router.post("/login")
async def login(paciente_login_schema: PacienteLoginSchema, session: Session = Depends(pegar_sessao)):
    paciente, erro = autenticar_paciente(paciente_login_schema.pa_email, paciente_login_schema.pa_senha, session)
    if erro:
        if erro == "Paciente não encontrado":
            raise HTTPException(status_code=404, detail=erro)
        elif erro == "Credenciais inválidas":
            raise HTTPException(status_code=401, detail=erro)
        else:
            raise HTTPException(status_code=400, detail=erro)

    access_token = criar_token(paciente.pa_id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
