# === ROTAS PROFISSIONAL DE SAÚDE ===

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from models import ProfissionalSaude
from dependencies import pegar_sessao
from main import bcript_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas.profissional_saude_schema import ProfissionalSaudeSchema
from schemas.login_schemas import ProfissionalSaudeLoginSchema

profissional_router = APIRouter(prefix="/profissional/sistema", tags=["profissional_saude"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/profissional/sistema/login")

def criar_token(id_profissional: int):
    brasil_tz = timezone(timedelta(hours=-3))
    expiracao = datetime.now(brasil_tz) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(id_profissional), "exp": expiracao}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token_profissional(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_profissional = payload.get("sub")
        if id_profissional is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return id_profissional
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado ou inválido")

@profissional_router.post("/criar_conta")
async def criar_conta(profissional_schema: ProfissionalSaudeSchema, session: Session = Depends(pegar_sessao)):
    profissional = session.query(ProfissionalSaude).filter(ProfissionalSaude.ps_cpf == profissional_schema.ps_cpf).first()
    if profissional:
        raise HTTPException(status_code=400, detail="Já existe profissional cadastrado com esse CPF")

    senha_criptografada = bcript_context.hash(profissional_schema.ps_senha)
    novo_profissional = ProfissionalSaude(
        ps_nome=profissional_schema.ps_nome,
        ps_cpf=profissional_schema.ps_cpf,
        ps_especialidade=profissional_schema.ps_especialidade,
        ps_email=profissional_schema.ps_email,
        ps_telefone=profissional_schema.ps_telefone,
        ps_registro_profissional=profissional_schema.ps_registro_profissional,
        ps_senha=senha_criptografada
    )
    session.add(novo_profissional)
    session.commit()
    session.close()
    return {"mensagem": "Profissional cadastrado com sucesso."}

@profissional_router.post("/login")
async def login(login_data: ProfissionalSaudeLoginSchema, session: Session = Depends(pegar_sessao)):
    profissional = session.query(ProfissionalSaude).filter(ProfissionalSaude.ps_email == login_data.ps_email).first()
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    if not bcript_context.verify(login_data.ps_senha, profissional.ps_senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = criar_token(profissional.ps_id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }


