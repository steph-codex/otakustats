from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="templates")

data = []

class Otaku(BaseModel):
    age: int
    hours_anime: float
    mangas_per_month: int
    genre: str
    platform: str
    engagement: str
    sleep: float

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
def submit(user: Otaku):
    data.append(user.dict())
    return {"message": "OK"}

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