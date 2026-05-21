# Monitoreo y Observabilidad con Prometheus y Grafana

## Descripción general
Este proyecto implementa un sistema de monitoreo completo para una API REST construida 
en Python con Flask. El sistema recolecta métricas usando Prometheus y las visualiza 
en dashboards de Grafana. Todo corre en contenedores Docker usando docker-compose.

## Componentes
- API REST (Python/Flask) - Puerto 3000
- Prometheus - Puerto 9090
- Grafana - Puerto 3001

## Arquitectura del proyecto

monitoreo-api/
├── docker-compose.yml       
├── README.md                
├── api/
│   ├── app.py               
│   ├── requirements.txt     
│   └── Dockerfile           
├── prometheus/
│   └── prometheus.yml       
└── scripts/
└── generar-trafico.py   

## Endpoints de la API
- `GET /` - Endpoint principal
- `GET /api/datos` - Retorna datos aleatorios
- `GET /api/lento` - Simula procesamiento lento (2-3 seg)
- `GET /api/estado` - Estado de la API
- `GET /metrics` - Métricas en formato Prometheus

## Cómo ejecutar

### Requisitos
- Docker Desktop

### Pasos
```bash
# Clonar el repositorio
git clone <URL-del-repositorio>

# Entrar a la carpeta
cd monitoreo-api

# Levantar todos los servicios
docker-compose up -d

# Verificar que todo esté corriendo
docker-compose ps
```

## Acceder a los servicios
- API: http://localhost:3000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (usuario: admin, contraseña: admin)

## Generar tráfico sintético

python scripts/generar-trafico.py

## Dashboard de Grafana
El dashboard "Dashboard de Monitoreo" contiene 3 paneles:
1. Requests por segundo - Tasa de requests en tiempo real
2. Latencia promedio - Tiempo de respuesta promedio por endpoint
3. Requests activos - Requests siendo procesados simultáneamente

Para configurar Grafana:
1. Entrar a http://localhost:3001 con admin/admin
2. Ir a Connections → Data Sources → Add data source
3. Seleccionar Prometheus y configurar URL: `http://prometheus:9090`
4. Guardar y el dashboard estará disponible

## Nombre: Leslly Natalia Hurtado Galeano 
## Código: 202210011601