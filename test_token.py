import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
token = os.getenv("INSTAGRAM_TOKEN")
instagram_user_id = "17841452552407799"  # ID de tu cuenta de IG Business

if not token:
    print("❌ Token no cargado")
    exit()

url = f"https://graph.facebook.com/v17.0/{instagram_user_id}?fields=username&access_token={token}"
r = requests.get(url)

print(f"HTTP Status: {r.status_code}")
print("Respuesta:")
print(r.text)
