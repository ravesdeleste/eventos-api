from fastapi import FastAPI, Query
from typing import Optional
import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

INSTAGRAM_TOKEN = os.getenv("INSTAGRAM_TOKEN")
INSTAGRAM_USER_ID = "17841452552407799"  # Tu ID de Instagram Business

app = FastAPI()

@app.get("/eventos")
def buscar_eventos(
    palabraClave: Optional[str] = Query("musica", description="Palabra clave a buscar")
):
    url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_USER_ID}/media?fields=id,caption,media_url,permalink,timestamp&access_token={INSTAGRAM_TOKEN}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "No se pudo obtener información de Instagram"}

    publicaciones = response.json().get("data", [])
    resultados = []

    for post in publicaciones:
        caption = post.get("caption", "")
        if palabraClave.lower() in caption.lower():
            resultados.append({
                "descripcion": caption,
                "imagen": post.get("media_url"),
                "fecha": post.get("timestamp"),
                "enlace": post.get("permalink")
            })

    if not resultados:
        return {"mensaje": f"No se encontraron publicaciones con la palabra '{palabraClave}'."}

    return {"eventos": resultados}


