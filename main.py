from fastapi import FastAPI, Query
from typing import Optional
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path=".env")

INSTAGRAM_TOKEN = os.getenv("IEAAJqbHxODuIBOwzZACvx8Fe7ZAcfGuG3IcgpnfkFPdWa3yA1khR4WxkNhHBhYDeMvYw9KGOVuxSO5ejAqTdeitBbl8mmgug2OrN6yreZBCZACw23dMy0zsZC6GsqPgnaLQX7ArfgwcmBbejkQIzIx8yMptdLQcJu33MdcPCRfJZBI2KGJnjmCrXpNz9pmD2m6sxXm2ZBvwh036veC0ZD")
INSTAGRAM_USER_ID = "17841452552407799"  # Tu ID de Instagram Business

app = FastAPI()

@app.get("/eventos")
def buscar_eventos(
    palabraClave: Optional[str] = Query("musica", description="Palabra clave a buscar"),
    ubicacion: Optional[str] = Query(None, description="Ubicación esperada en el caption"),
    fechaMinima: Optional[str] = Query(None, description="Fecha mínima en formato ISO 8601"),
    genero: Optional[str] = Query(None, description="Género musical como techno, house, etc")
):
    url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_USER_ID}/media?fields=id,caption,media_url,permalink,timestamp&access_token={INSTAGRAM_TOKEN}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "No se pudo obtener información de Instagram"}

    publicaciones = response.json().get("data", [])
    resultados = []

    for post in publicaciones:
        caption = post.get("caption", "")
        timestamp = post.get("timestamp", "")
        fecha_evento = datetime.fromisoformat(timestamp.replace("Z", "+00:00")) if timestamp else None

        if palabraClave and palabraClave.lower() not in caption.lower():
            continue
        if ubicacion and ubicacion.lower() not in caption.lower():
            continue
        if genero and genero.lower() not in caption.lower():
            continue
        if fechaMinima and fecha_evento:
            try:
                fecha_minima_dt = datetime.fromisoformat(fechaMinima)
                if fecha_evento < fecha_minima_dt:
                    continue
            except:
                continue

        resultados.append({
            "descripcion": caption,
            "imagen": post.get("media_url"),
            "fecha": timestamp,
            "ubicacion": ubicacion,
            "genero": genero,
            "enlace": post.get("permalink")
        })

    if not resultados:
        return {"mensaje": "No se encontraron eventos que coincidan con los filtros."}

    return {"eventos": resultados}


