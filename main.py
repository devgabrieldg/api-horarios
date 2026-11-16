from fastapi import FastAPI

app = FastAPI(title="API de Horários Disponíveis (teste)")

# Horários fixos, apenas para teste
HORARIOS_DISPONIVEIS = [
    {"data": "2026-11-17", "horario": "09:00"},
    {"data": "2026-11-17", "horario": "14:30"},
    {"data": "2026-11-18", "horario": "10:00"},
]


@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/horarios")
def listar_horarios():
    return {"horarios_disponiveis": HORARIOS_DISPONIVEIS}
