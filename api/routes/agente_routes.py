# === ROTAS AGENTE COMUNITÁRIO ===

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from models import AgenteComunitario
from dependencies import pegar_sessao
from main import bcript_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas.login_schemas import AgenteComunitarioLoginSchema
from schemas.agente_comunitario_schema import AgenteComunitarioSchema

agente_router = APIRouter(prefix="/agente/sistema", tags=["agente_comunitario"])

oauth2_scheme_agente = OAuth2PasswordBearer(tokenUrl="/agente/sistema/login")

def criar_token_agente(id_agente: int):
    brasil_tz = timezone(timedelta(hours=-3))
    expiracao = datetime.now(brasil_tz) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(id_agente), "exp": expiracao}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token_agente(token: str = Depends(oauth2_scheme_agente)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_agente = payload.get("sub")
        if id_agente is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return id_agente
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado ou inválido")

@agente_router.post("/criar_conta")
async def criar_conta_agente(agente_schema: AgenteComunitarioSchema, session: Session = Depends(pegar_sessao)):
    agente_existente = session.query(AgenteComunitario).filter(
        (AgenteComunitario.cpf == agente_schema.cpf) |
        (AgenteComunitario.email == agente_schema.email)
    ).first()

    if agente_existente:
        raise HTTPException(status_code=400, detail="Já existe um agente com esse CPF ou e-mail.")

    senha_criptografada = bcript_context.hash(agente_schema.senha)
    novo_agente = AgenteComunitario(
        nome=agente_schema.nome,
        cpf=agente_schema.cpf,
        email=agente_schema.email,
        telefone=agente_schema.telefone,
        senha=senha_criptografada
    )
    session.add(novo_agente)
    session.commit()
    session.close()

    return {"mensagem": "Agente comunitário cadastrado com sucesso."}


@agente_router.post("/login")
async def login_agente(login_data: AgenteComunitarioLoginSchema, session: Session = Depends(pegar_sessao)):
    agente = session.query(AgenteComunitario).filter(AgenteComunitario.email == login_data.email).first()
    if not agente:
        raise HTTPException(status_code=404, detail="Agente comunitário não encontrado")
    if not bcript_context.verify(login_data.senha, agente.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = criar_token_agente(agente.id_acs)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }

