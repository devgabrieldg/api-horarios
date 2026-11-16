from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="API de Horários (teste)")

# Horários iniciais fixos, apenas para teste
HORARIOS_INICIAIS = [
    "17/11/2026 às 09:00",
    "17/11/2026 às 14:30",
    "18/11/2026 às 10:00",
]

# Estado em memória (volta ao inicial se o serviço reiniciar)
horarios_disponiveis = list(HORARIOS_INICIAIS)
horarios_confirmados = []


class Confirmacao(BaseModel):
    horario: str


@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/horarios")
def listar_horarios():
    return horarios_disponiveis


@app.post("/confirmar")
def confirmar_horario(dados: Confirmacao):
    if dados.horario not in horarios_disponiveis:
        raise HTTPException(status_code=409, detail="Horário indisponível")

    horarios_disponiveis.remove(dados.horario)
    horarios_confirmados.append(dados.horario)
    return {"status": "confirmado", "horario": dados.horario}


class Reagendamento(BaseModel):
    horario_atual: str
    novo_horario: str


@app.post("/reagendar")
def reagendar_horario(dados: Reagendamento):
    if dados.horario_atual not in horarios_confirmados:
        raise HTTPException(status_code=404, detail="Horário atual não encontrado")
    if dados.novo_horario not in horarios_disponiveis:
        raise HTTPException(status_code=409, detail="Novo horário indisponível")

    # Libera o horário antigo e confirma o novo
    horarios_confirmados.remove(dados.horario_atual)
    horarios_disponiveis.append(dados.horario_atual)
    horarios_disponiveis.remove(dados.novo_horario)
    horarios_confirmados.append(dados.novo_horario)
    return {
        "status": "reagendado",
        "horario_anterior": dados.horario_atual,
        "novo_horario": dados.novo_horario,
    }


@app.get("/confirmados")
def listar_confirmados():
    return horarios_confirmados


@app.post("/resetar")
def resetar():
    horarios_disponiveis.clear()
    horarios_disponiveis.extend(HORARIOS_INICIAIS)
    horarios_confirmados.clear()
    return {"status": "resetado"}
