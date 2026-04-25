from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import matplotlib.pyplot as plt

app = FastAPI()

data = []

class Otaku(BaseModel):
    age: int
    hours_anime: float
    mangas_per_month: int
    genre: str
    platform: str
    engagement: str
    sleep: float


@app.get("/plot")
def plot():
    df = pd.DataFrame(data)
    plt.scatter(df["hours_anime"], df["sleep"])
    plt.xlabel("Heures anime")
    plt.ylabel("Sommeil")
    plt.savefig("graph.png")
    return {"message": "Graph généré"}
@app.get("/")

def home():
    return {"message": "OtakuStats API fonctionne"}

@app.post("/submit")
def submit(user: Otaku):
    data.append(user.dict())
    return {"message": "Données enregistrées"}

@app.get("/stats")
def stats():
    if len(data) == 0:
        return {"message": "Pas de données"}

    df = pd.DataFrame(data)

    return {
        "moyenne_heures_anime": df["hours_anime"].mean(),
        "moyenne_manga": df["mangas_per_month"].mean(),
        "moyenne_sommeil": df["sleep"].mean(),
        "genre_populaire": df["genre"].mode()[0]
    }