from fastapi import FastAPI, HTTPException
from scraping import scrape_tayara
import pandas as pd
import os

app = FastAPI()

# Fonction pour charger les données à partir du fichier CSV
def load_data():
    if not os.path.exists('annonces_tayara.csv'):
        print("Le fichier CSV n'existe pas.")
        return []
    try:
        df = pd.read_csv('annonces_tayara.csv')
        if df.empty:
            print("Le fichier CSV est vide.")
            return []
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
        return []

# Charger les données dans une variable globale
annonces = load_data()

# Endpoint racine
@app.get("/")
def root():
    return {"message": "API de scraping Tayara opérationnelle"}

# Endpoint pour retourner toutes les annonces
@app.get("/annonces")
def get_annonces():
    if not annonces:
        raise HTTPException(status_code=404, detail="Aucune annonce trouvée")
    return annonces

# Endpoint pour lancer une nouvelle session de scraping
@app.post("/scrape")
def scrape_annonces():
    global annonces
    annonces = scrape_tayara()
    if not annonces:
        raise HTTPException(status_code=500, detail="Échec du scraping ou aucune annonce trouvée")
    return {"message": f"{len(annonces)} annonces récupérées avec succès"}
