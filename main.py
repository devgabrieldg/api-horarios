from fastapi import FastAPI

app = FastAPI(title="API de Horários Disponíveis (teste)")

# Horários fixos, apenas para teste
HORARIOS_DISPONIVEIS = [
    "17/11/2026 às 09:00",
    "17/11/2026 às 14:30",
    "18/11/2026 às 10:00",
]


@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/horarios")
def listar_horarios():
    return HORARIOS_DISPONIVEIS
