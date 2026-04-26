from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()

# dossier templates
templates = Jinja2Templates(directory="templates")

# stockage des données (en mémoire)
data = []

# modèle des données
class Otaku(BaseModel):
    age: int
    hours_anime: float
    mangas_per_month: int
    genre: str
    platform: str
    engagement: str
    sleep: float


# page d’accueil (interface web)
@app.get("/")
def home():
    return {"ok": "running"}

# envoyer des données
@app.post("/submit")
def submit(user: Otaku):
    data.append(user.dict())
    return {"message": "Données enregistrées"}


# statistiques
@app.get("/stats")
def stats():
    if len(data) == 0:
        return {"message": "Pas de données"}

    df = pd.DataFrame(data)

    return {
        "moyenne_heures": df["hours_anime"].mean(),
        "moyenne_mangas": df["mangas_per_month"].mean(),
        "genre_populaire": df["genre"].mode()[0]
    }


# obligatoire pour Railway (port dynamique)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)