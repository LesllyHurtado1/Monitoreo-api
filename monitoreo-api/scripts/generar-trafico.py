import requests
import time
import random

endpoints = [
    "http://localhost:3000/",
    "http://localhost:3000/api/datos",
    "http://localhost:3000/api/estado",
    "http://localhost:3000/api/lento",
]

print("Generando tráfico... (presiona Ctrl+C para parar)")

while True:
    url = random.choice(endpoints)
    try:
        r = requests.get(url, timeout=5)
        print(f"{url} → {r.status_code}")
    except Exception as e:
        print(f" Error: {e}")
    time.sleep(random.uniform(0.5, 2))