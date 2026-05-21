from flask import Flask, jsonify
import time
import random
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Métricas
REQUEST_COUNT = Counter('http_requests_total', 'Total de requests', ['endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Latencia', ['endpoint'])
ACTIVE_REQUESTS = Gauge('active_requests', 'Requests activos')

@app.route('/')
def home():
    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.labels(endpoint='/').inc()
    with REQUEST_LATENCY.labels(endpoint='/').time():
        ACTIVE_REQUESTS.dec()
        return jsonify({"mensaje": "API funcionando", "status": "ok"})

@app.route('/api/datos')
def datos():
    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.labels(endpoint='/api/datos').inc()
    with REQUEST_LATENCY.labels(endpoint='/api/datos').time():
        datos = [{"id": i, "valor": random.randint(1, 100)} for i in range(5)]
        ACTIVE_REQUESTS.dec()
        return jsonify({"datos": datos})

@app.route('/api/lento')
def lento():
    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.labels(endpoint='/api/lento').inc()
    with REQUEST_LATENCY.labels(endpoint='/api/lento').time():
        time.sleep(random.uniform(2, 3))
        ACTIVE_REQUESTS.dec()
        return jsonify({"mensaje": "Procesamiento lento completado"})

@app.route('/api/estado')
def estado():
    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.labels(endpoint='/api/estado').inc()
    with REQUEST_LATENCY.labels(endpoint='/api/estado').time():
        ACTIVE_REQUESTS.dec()
        return jsonify({"status": "saludable", "uptime": "activo"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)