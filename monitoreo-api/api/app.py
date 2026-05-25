from flask import Flask, jsonify
import time
import random
from prometheus_client import Counter, Histogram, Gauge, Summary, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Métricas básicas
REQUEST_COUNT = Counter('http_requests_total', 'Total de requests', ['endpoint', 'method'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Latencia', ['endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0])
ACTIVE_REQUESTS = Gauge('active_requests', 'Requests activos')

# Métricas avanzadas
REQUEST_SUMMARY = Summary('http_request_summary_seconds', 'Resumen de latencia', ['endpoint'])
ERROR_COUNT = Counter('http_errors_total', 'Total de errores', ['endpoint'])
ITEMS_PROCESSED = Counter('items_processed_total', 'Items procesados')

@app.route('/')
def home():
    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.labels(endpoint='/', method='GET').inc()
    with REQUEST_LATENCY.labels(endpoint='/').time():
        with REQUEST_SUMMARY.labels(endpoint='/').time():
            ACTIVE_REQUESTS.dec()
            return jsonify({"mensaje": "API funcionando", "status": "ok", "version": "1.0"})

@app.route('/api/datos')
def datos():
    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.labels(endpoint='/api/datos', method='GET').inc()
    with REQUEST_LATENCY.labels(endpoint='/api/datos').time():
        with REQUEST_SUMMARY.labels(endpoint='/api/datos').time():
            cantidad = random.randint(5, 15)
            datos = [{"id": i, "valor": random.randint(1, 100)} for i in range(cantidad)]
            ITEMS_PROCESSED.inc(cantidad)
            ACTIVE_REQUESTS.dec()
            return jsonify({"datos": datos, "total": cantidad})

@app.route('/api/lento')
def lento():
    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.labels(endpoint='/api/lento', method='GET').inc()
    with REQUEST_LATENCY.labels(endpoint='/api/lento').time():
        with REQUEST_SUMMARY.labels(endpoint='/api/lento').time():
            time.sleep(random.uniform(2, 3))
            ACTIVE_REQUESTS.dec()
            return jsonify({"mensaje": "Procesamiento lento completado", "tiempo": "2-3s"})

@app.route('/api/estado')
def estado():
    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.labels(endpoint='/api/estado', method='GET').inc()
    with REQUEST_LATENCY.labels(endpoint='/api/estado').time():
        with REQUEST_SUMMARY.labels(endpoint='/api/estado').time():
            ACTIVE_REQUESTS.dec()
            return jsonify({"status": "saludable", "uptime": "activo", "memoria": "ok"})

@app.route('/api/usuarios')
def usuarios():
    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.labels(endpoint='/api/usuarios', method='GET').inc()
    with REQUEST_LATENCY.labels(endpoint='/api/usuarios').time():
        with REQUEST_SUMMARY.labels(endpoint='/api/usuarios').time():
            usuarios = [{"id": i, "nombre": f"Usuario {i}", "activo": random.choice([True, False])} 
                       for i in range(1, random.randint(3, 8))]
            ACTIVE_REQUESTS.dec()
            return jsonify({"usuarios": usuarios})

@app.route('/api/productos')
def productos():
    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.labels(endpoint='/api/productos', method='GET').inc()
    with REQUEST_LATENCY.labels(endpoint='/api/productos').time():
        with REQUEST_SUMMARY.labels(endpoint='/api/productos').time():
            productos = [{"id": i, "nombre": f"Producto {i}", "precio": round(random.uniform(10, 500), 2)} 
                        for i in range(1, random.randint(3, 10))]
            ACTIVE_REQUESTS.dec()
            return jsonify({"productos": productos})

@app.route('/api/error')
def error_simulado():
    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.labels(endpoint='/api/error', method='GET').inc()
    ERROR_COUNT.labels(endpoint='/api/error').inc()
    with REQUEST_LATENCY.labels(endpoint='/api/error').time():
        ACTIVE_REQUESTS.dec()
        if random.random() < 0.5:
            return jsonify({"error": "Error simulado", "codigo": 500}), 500
        return jsonify({"mensaje": "Sin error esta vez"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
