import requests
import time
import random

endpoints = [
    "http://localhost:3000/",
    "http://localhost:3000/api/datos",
    "http://localhost:3000/api/estado",
    "http://localhost:3000/api/lento",
    "http://localhost:3000/api/usuarios",
    "http://localhost:3000/api/productos",
    "http://localhost:3000/api/error",
]

print("Generando tráfico... (presiona Ctrl+C para parar)")
contador = 0

while True:
    url = random.choice(endpoints)
    try:
        r = requests.get(url, timeout=5)
        estado = "✅" if r.status_code == 200 else "❌"
        contador += 1
        print(f"{estado} [{contador}] {url} → {r.status_code}")
    except Exception as e:
        print(f" Error: {e}")
    time.sleep(random.uniform(0.3, 1.5))
