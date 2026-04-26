from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# stockage en mémoire
data = []

# modèle
class Otaku(BaseModel):
    age: int
    hours_anime: float
    mangas_per_month: int
    genre: str
    platform: str
    engagement: str
    sleep: float


#  PAGE D'ACCUEIL (INTERFACE HTML)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


#  ENVOI DES DONNÉES
@app.post("/submit")
def submit(user: Otaku):
    data.append(user.dict())
    return {"message": "Données enregistrées"}


#  STATISTIQUES
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


#  LANCEMENT LOCAL (utile en dev)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)