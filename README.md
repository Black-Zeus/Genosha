# Genosha

Repositorio de infraestructura Docker de Genosha. Contiene el script de gestión, compose, Dockerfiles, código fuente de los servicios y directorios de soporte.

---

## Requisitos previos

- Docker Desktop corriendo
- Git Bash (para ejecutar el script en Windows)

---

## Inicio rápido

```bash
# Desde la raíz del repo (Genosha/)
bash docker_tools_v3.sh
```

El menú interactivo permite levantar, detener, reiniciar y monitorear todos los servicios.

---

## Estructura de carpetas

```
Genosha/
├── docker_tools_v3.sh          # Herramienta principal de gestión
├── docker-compose-dev.yml      # Compose para ambiente DEV
│
├── .env                        # Variables base (PROJECT_NAME, rutas)
├── .env.dev                    # Overrides de DEV (credenciales, URLs)
├── .env.example                # Template para crear nuevos ambientes
│
├── volumenes/                  # Código fuente de cada servicio (bind-mounts)
│   ├── web/                    # React + Vite (frontend)
│   ├── api/                    # FastAPI (Python)
│   ├── scheduler/              # Celery Beat (Python)
│   ├── ingestion-worker/       # Celery Worker — cola: ingestion
│   ├── normalization-worker/   # Celery Worker — cola: normalization
│   ├── analysis-worker/        # Celery Worker — cola: analysis
│   ├── orchestrator/           # Celery Worker — cola: orchestration
│   ├── vector-worker/          # Celery Worker — cola: vector
│   └── reporting-worker/       # Celery Worker — cola: reporting
│
├── DockerFiles/                # Un Dockerfile por servicio de aplicación
│   ├── web/Dockerfile
│   ├── api/Dockerfile
│   ├── scheduler/Dockerfile
│   ├── ingestion-worker/Dockerfile
│   ├── normalization-worker/Dockerfile
│   ├── analysis-worker/Dockerfile
│   ├── orchestrator/Dockerfile
│   ├── vector-worker/Dockerfile
│   └── reporting-worker/Dockerfile
│
├── Configs/                    # Configuraciones montadas en contenedores
│   ├── nginx/nginx.conf        # Proxy: / → web, /api/ → api
│   └── postgres/               # (reservado para configuración futura)
│
├── Logs/                       # Logs de contenedores (bind-mount, solo DEV)
│   └── dev/
│       ├── api/
│       ├── web/
│       ├── scheduler/
│       ├── ingestion-worker/
│       ├── normalization-worker/
│       ├── analysis-worker/
│       ├── orchestrator/
│       ├── vector-worker/
│       ├── reporting-worker/
│       ├── postgres/
│       ├── redis/
│       ├── qdrant/
│       ├── minio/
│       └── proxy/
│
├── secrets/                    # Secretos (nunca commitear valores reales)
│   └── .env.secrets.example    # Template de secretos para QA/PRD
│
└── share/                      # Volumen compartido RW entre todos los contenedores
                                # Montado en /genosha/share dentro de cada contenedor
```

---

## Servicios

### Infraestructura (grupo: `dependency`)

| Contenedor | Imagen | Puerto host |
|---|---|---|
| `genosha-postgres` | postgres:16-alpine | 5432 |
| `genosha-redis` | redis:7-alpine | 6379 |
| `genosha-qdrant` | qdrant/qdrant | 6333, 6334 |
| `genosha-minio` | minio/minio | 9000 (API), 9001 (consola) |
| `genosha-gotenberg` | gotenberg/gotenberg:8 | 3001 → container:3000 |

Los volúmenes de infraestructura son **volúmenes Docker nombrados** (`genosha_postgres_data`, etc.), no carpetas locales.

### Aplicación (grupo: `core`)

| Contenedor | Tecnología | Puerto host | Hot-reload |
|---|---|---|---|
| `genosha-web` | React + Vite | 3000 | Vite HMR |
| `genosha-api` | FastAPI + Uvicorn | 8000 | `--reload` |
| `genosha-scheduler` | Celery Beat | — | watchfiles |
| `genosha-ingestion-worker` | Celery Worker | — | watchfiles |
| `genosha-normalization-worker` | Celery Worker | — | watchfiles |
| `genosha-analysis-worker` | Celery Worker | — | watchfiles |
| `genosha-orchestrator` | Celery Worker | — | watchfiles |
| `genosha-vector-worker` | Celery Worker | — | watchfiles |
| `genosha-reporting-worker` | Celery Worker | — | watchfiles |

El código de cada servicio vive en `volumenes/{nombre}/` y se monta como bind-mount en `/app` dentro del contenedor. Cualquier cambio en el editor se refleja de inmediato sin reconstruir la imagen.

### Proxy (grupo: `core`)

| Contenedor | Imagen | Puerto host |
|---|---|---|
| `genosha-proxy` | nginx:alpine | 80 |

Rutas: `/` → `genosha-web:3000` · `/api/` → `genosha-api:8000`

### Herramientas de desarrollo (grupo: `tools`, opcional)

Se activan con `--profile tools` o desde el menú del script.

| Contenedor | Imagen | Puerto host | Descripción |
|---|---|---|---|
| `genosha-mailpit` | axllent/mailpit | 1025 (SMTP), 8025 (UI) | Captura emails enviados en DEV |

Mailpit intercepta cualquier email que los servicios envíen via SMTP (puerto 1025) y los muestra en su interfaz web en `http://localhost:8025`. No se requiere configuración de relay real.

---

## Estructura de un servicio Python

```
volumenes/{servicio}/
├── requirements.txt    # Dependencias pip
└── app/
    ├── __init__.py
    ├── celery_app.py   # Instancia Celery + configuración de cola (workers)
    └── tasks.py        # Tareas registradas en la cola
```

```
volumenes/api/
├── requirements.txt    # fastapi, uvicorn
└── app/
    ├── __init__.py
    └── main.py         # Aplicación FastAPI
```

---

## Variables de entorno

| Archivo | Contenido |
|---|---|
| `.env` | `PROJECT_NAME`, `ENV`, rutas de carpetas |
| `.env.dev` | Credenciales y URLs para el ambiente DEV |
| `.env.example` | Template para cualquier ambiente nuevo |
| `secrets/.env.secrets.example` | Template de secretos para QA/PRD |

Para añadir un nuevo ambiente (ej. `qa`):
1. Copiar `.env.example` como `.env` y ajustar `ENV=qa`
2. Crear `.env.qa` con las credenciales correspondientes
3. El script detectará automáticamente el archivo `docker-compose-qa.yml`

---

## Convenciones del script (`docker_tools_v3.sh`)

El script valida las siguientes reglas en cada servicio del compose:

- `container_name` debe ser `${PROJECT_NAME}-{servicio}` (ej: `genosha-api`)
- Labels obligatorios: `stack`, `env`, `service.group`, `service.lifecycle`
- `service.group` válidos: `dependency`, `core`, `tools`
- Rutas en volumes deben usar variables (`${DATA_ROOT}`, `${LOGS_ROOT}`, etc.), no rutas `./` directas

---

## Ambientes previstos

| Ambiente | Compose | Notas |
|---|---|---|
| `dev` | `docker-compose-dev.yml` | Todos los puertos expuestos, código por bind-mount |
| `qa` | `docker-compose-qa.yml` | Por implementar |
| `prd` | `docker-compose.yml` | Por implementar, solo puerto de nginx expuesto |

En QA y PRD los logs y configuraciones también pasarán a volúmenes Docker; los bind-mounts de `Logs/` son exclusivos de DEV para facilitar el acceso directo a los archivos.
