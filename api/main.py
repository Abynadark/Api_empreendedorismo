from fastapi import FastAPI
from passlib.context import CryptContext #segurança
from dotenv import load_dotenv #segurança
import os #segurança

load_dotenv() #segurança

SECRET_KEY = os.getenv("SECRET_KEY") #segurança
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcript_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #segurança

from routes.paciente_routes import paciente_router
from routes.profissional_routes import profissional_router
from routes.agente_routes import agente_router
from routes.consulta_routes import consulta_router
from routes.unidade_router import unidade_router
from routes.agendamento_routes import agendamento_router
from routes.notificacao_routes import notificacao_router

app.include_router(paciente_router)
app.include_router(profissional_router)
app.include_router(agente_router)
app.include_router(consulta_router)
app.include_router(unidade_router)
app.include_router(agendamento_router)
app.include_router(notificacao_router)