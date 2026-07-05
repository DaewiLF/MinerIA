# AGENT.md - Memoria Permanente del Proyecto MinerIA

## Descripción General

### Objetivo
MinerIA es un sistema inteligente para la detección de cobre en imágenes de muestras mineras mediante Redes Neuronales Convolucionales (CNNs). Está diseñado para optimizar la fase de exploración inicial en la industria minera, enfocándose en PYMES de exploración y Consultoras Geológicas.

### Problema que resuelve
Reduce la dependencia de métodos tradicionales de laboratorio que generan altos costos operativos (>$500 por muestra) y demoras de hasta 4 semanas, permitiendo análisis en terreno con hardware estándar (Edge Computing).

### Estado actual
- Proyecto funcional con Docker Compose (3 servicios: MariaDB + FastAPI backend + React frontend)
- Dos modelos CNN: binario (cobre/sin cobre) y multiclase (15 minerales)
- Autenticación JWT con roles (admin/analyst)
- Generación de reportes PDF con formato profesional (cumplimiento normativo chileno)
- Soporte para análisis de imágenes, videos MP4/MKV y panoramas
- Grad-CAM integrado en el frontend (feature branch `feature/Gradcama-Nueva-IA`)

---

## Stack Tecnológico

### Backend (Python 3.11+)
| Tecnología | Versión | Propósito |
|---|---|---|
| FastAPI | 0.115.0 | REST API framework |
| Uvicorn | 0.30.6 | ASGI server |
| TensorFlow-cpu | 2.16.1 | Deep Learning inference |
| OpenCV | 4.10.0.84 | Procesamiento de imágenes/video |
| SQLAlchemy | 2.0.34 | ORM para MariaDB |
| PyMySQL | 1.1.1 | Driver MySQL |
| python-jose | 3.3.0 | JWT tokens |
| passlib | 1.7.4 | Password hashing (pbkdf2_sha256) |
| ReportLab | 4.2.4 | PDF generation |
| NumPy | 1.26.4 | Numerical processing |
| Pillow | 10.4.0 | Image loading |

### Frontend (React 19 + TypeScript)
| Tecnología | Versión | Propósito |
|---|---|---|
| React | 19.2.0 | UI framework |
| TypeScript | 5.9.3 | Type safety |
| Vite | 7.2.2 | Build tool |
| TailwindCSS | 3.4.18 | Utility-first CSS |
| Axios | 1.13.2 | HTTP client |
| React Router DOM | 7.9.6 | SPA routing |

### Infraestructura
| Tecnología | Propósito |
|---|---|
| Docker + Docker Compose | Contenedores (3 servicios) |
| MariaDB 10.11 | Base de datos relacional |

---

## Arquitectura

### Patrón: Three-tier + Microservicios monoliticos (dockerizados)

```
┌──────────────┐    HTTP/JSON + JWT    ┌──────────────┐     SQL      ┌──────────────┐
│  Frontend    │ ──────────────────── │  Backend     │ ──────────── │  Database    │
│  React/TS    │    REST API (8000)    │  FastAPI     │              │  MariaDB     │
│  Port 5173   │                       │  Port 8000   │              │  Port 3306   │
└──────────────┘                       └──────────────┘              └──────────────┘
                                              │
                                              ├── ML Models
                                              │   ├── CopperCNN (binario)
                                              │   └── MineralClassifier (15 clases)
                                              │
                                              ├── PDF Reports (ReportLab)
                                              ├── Uploads (imágenes/videos)
                                              └── Panorama Processing (sliding window)
```

### Flujo de datos principal
1. Usuario se autentica (JWT) -> loginPage
2. Dashboard: sube imagen + metadatos selecciona modelo IA
3. Backend recibe multipart: imagen + JSON metadata
4. Ejecuta modelo CNN seleccionado (CopperCNN o MineralClassifier)
5. Guarda imagen + clasificación en BD
6. Genera PDF con ReportLab
7. Guarda reporte (JSON) en BD
8. Retorna AnalysisDetailResponse al frontend

### Comunicación entre módulos
- Frontend -> Backend: REST sobre HTTP (Axios con JWT interceptor)
- Backend -> Database: SQLAlchemy ORM (PyMySQL driver)
- Backend -> ML Models: llamada directa a métodos Python (singleton)
- Backend -> PDF: ReportLab (generación síncrona)
- Docker Compose: `depends_on` entre servicios

---

## Responsabilidad de cada carpeta

### Backend_cnn/
| Carpeta | Responsabilidad |
|---|---|
| `app/` | Paquete principal de la aplicación |
| `app/api/` | Route handlers (auth, analysis CRUD, v1/) |
| `app/api/v1/` | Endpoints versionados (video, panorama) |
| `app/core/` | Configuración (Settings) y seguridad (JWT, hashing) |
| `app/db/` | ORM models (SQLAlchemy) y conexión MySQL |
| `app/ml/models/` | Implementaciones de modelos IA (registry pattern) |
| `app/ml/utils/` | Utilidades ML (preprocessing, PDF, sliding window) |
| `app/routes/` | Rutas legacy (Flask/old FastAPI) - NO USAR |
| `model_data/` | Modelos entrenados (.h5, .keras) y labels |
| `training/` | Scripts de entrenamiento de CNNs |
| `uploads/` | Archivos subidos (imágenes, videos, frames) |
| `reports/` | PDFs generados |

### MinerIA/ (frontend)
| Carpeta | Responsabilidad |
|---|---|
| `src/api/` | Clientes HTTP (Axios) y funciones API |
| `src/components/layout/` | Componentes de layout (Sidebar, TopBar) |
| `src/context/` | React Context (AuthProvider, AuthContext, useAuth) |
| `src/pages/` | Páginas principales (Login, Dashboard, History, Detail) |

---

## Convenciones del proyecto

### Nombres
- **Python**: `snake_case` para variables, funciones, archivos, módulos
- **TypeScript/React**: `camelCase` para variables/funciones, `PascalCase` para componentes/interfaces
- **Database**: `snake_case` con prefijo `id_`, `fk_`, `idx_`, `uq_`
- **API Routes**: prefijos `/api/auth`, `/api/analysis`, `/api/v1`
- **Model IDs**: `"copper"` y `"minerals"` (strings lower case)

### Organización
- Backend: modular por capas (api -> core -> db -> ml)
- Frontend: funcional por tipo (api, components, context, pages)
- Cada archivo en backend exporta un router de FastAPI (APIRouter)

### Estilo de código
- Python: type hints obligatorios, dataclasses para DTOs, Protocols para interfaces
- TypeScript: interfaces exportadas en archivos de API, tipado estricto
- Sin comentarios en código a menos que sea necesario (docstrings funcionales)
- TailwindCSS inline (sin CSS modules ni styled-components)

### Manejo de errores
- Backend: HTTPException con códigos HTTP estándar, mensajes en español
- Frontend: try/catch en llamadas API, estado error en componentes
- Validación de tipos de archivo en uploads (imagen, video)
- Logging: `print()` statements (no hay logger formal)

### Configuración
- Variables de entorno en `Backend_cnn/.env`
- Settings class en `app/core/config.py` con defaults seguros
- Frontend usa `import.meta.env.VITE_API_URL` para URL base

---

## Patrones de Diseño

| Patrón | Ubicación | Descripción |
|---|---|---|
| **Singleton** | `copper_model = CopperCNN()` y `mineral_model = MineralClassifier()` en `model_registry.py` | Instancias globales únicas de modelos (lazy loading) |
| **Registry** | `model_registry.py` con `MODEL_REGISTRY` dict + `get_analysis_model()` | Lookup de modelos por ID |
| **Protocol** | `base.py` con `AnalysisModel` protocol class | Interfaz duck-typing para modelos intercambiables |
| **Dependency Injection** | `Depends(get_db)` y `Depends(get_current_user)` | Inyección de sesiones BD y usuario autenticado |
| **Provider** | `AuthProvider.tsx` / `AuthContext.tsx` | Context API de React para estado de autenticación |
| **Router** | `APIRouter(prefix=...)` en FastAPI | Organización modular de rutas |
| **Private Route** | Componente `PrivateRoute` en `App.tsx` | Guard pattern para rutas protegidas |
| **Interceptor** | Axios `interceptors.request.use()` | Inyección automática de JWT en cada request |
| **DTO/Response Schema** | Pydantic models (`AnalysisDetailResponse`, etc.) | Tipado estricto de respuestas API |
| **Factory** | `_ReportDocTemplate` custom template | Generación de documentos PDF estructurados |

---

## Flujo de Ejecución

### Inicio del sistema (Docker Compose)
1. `docker-compose up` -> MariaDB, backend, frontend
2. MariaDB ejecuta `db_init/proyecto_integracion.sql` (crea DB + tablas + seed data)
3. Backend inicia: `uvicorn app.main:app` -> CORS, StaticFiles, routers
4. Backend intenta `Base.metadata.create_all()` en startup (no bloquea si falla)
5. Frontend inicia: `npm run dev -- --host`

### Proceso de análisis de imagen
1. Frontend: usuario llena metadatos + selecciona archivo + elige modelo
2. POST `/api/analysis/upload` con multipart (file + metadata JSON + model_id)
3. Backend valida tipo de archivo (JPEG/PNG), guarda en disco con UUID
4. Obtiene modelo del registry (`get_analysis_model(model_id)`)
5. Ejecuta `analysis_model.analyze(disk_path)` -> ModelPrediction
6. Guarda `Imagen` y `Clasificacion` en BD
7. Construye textos (aiSummary, recommendations) según resultado
8. Genera PDF en `reports/reporte_{id}.pdf`
9. Guarda `Reporte` en BD con contenido JSON completo
10. Retorna `AnalysisDetailResponse` al frontend

### Proceso de autenticación
1. Frontend: login form (email + password + role)
2. POST `/api/auth/login` -> verifica credenciales + rol
3. Backend: `verify_password` + check `cargo == role` -> JWT (60 min expiry)
4. Frontend: guarda token + user en localStorage
5. Axios interceptor: añade `Authorization: Bearer <token>` a cada request
6. Backend: `get_current_user` decodifica JWT, obtiene usuario de BD

---

## Componentes Principales

### Modelos ML
- **CopperCNN**: binario (MobileNetV2), detecta `con_cobre`/`sin_cobre`, input 224x224
- **MineralClassifier**: multiclase (15 minerales), MobileNetV2, input 224x224
- Ambos cargan lazy (al primer `analyze()`), singleton globales
- Registry pattern para selección dinámica

### API Routes
- `auth.py`: login, register (JWT + password hashing)
- `analysis.py`: CRUD completo de análisis (upload, history, detail, pdf download, upload-batch, queue)
- `v1/analyze_video.py`: procesamiento de video con CopperCNN
- `v1/panorama.py`: upload de panoramas con sliding window grid

### Background Queue
- `ml/inference_queue.py`: bucle de inferencia en segundo plano via BackgroundTasks
  - `process_single_item(db, item)`: procesa un item de cola (inferencia + PDF + BD)
  - `process_pending_queue()``: procesa todos los items pendientes secuencialmente
  - `run_queue_background()`: wrapper async para ejecutar en thread pool

### Frontend Pages
- `LoginPage`: formulario de login con selector de rol
- `DashboardPage`: upload de imagen + metadatos, upload de video, carga por lotes, cola de procesamiento, resultados inline
- `HistoryPage`: tabla de historial con links a detalle
- `AnalysisDetailPage`: detalle completo + download PDF

### Database Tables
- `cola_analisis`: cola persistente para procesamiento batch (id_cola, id_usuario, ruta_archivo, metadata_json, modelo_id, estado, error, fechas)

---

## Dependencias entre Módulos

```
app/main.py
  ├── app/api/auth.py -> app/core/security.py -> app/core/config.py
  │                   -> app/db/mysql_connection.py -> app/db/models.py
  │
  ├── app/api/analysis.py -> app/core/security.py
  │                       -> app/db/mysql_connection.py -> app/db/models.py
  │                       -> app/ml/models/model_registry.py
  │                       -> app/ml/utils/report_generator.py
  │
  ├── app/api/v1/analyze_video.py -> app/ml/models/cnn_model.py
  │                                -> app/ml/models/copper_model.py (DEAD LINK: wrong import)
  │
  ├── app/api/v1/analyze_video (correcto) -> app/ml/models/cnn_model.py
  │                                        -> app/ml/models/copper_model.py (correct import)
  │
  └── app/api/v1/panorama.py -> app/ml/utils/sliding_window.py
```

---

## Base de Datos

### Modelo (7 tablas)
```
usuarios (1) ──< imagenes (N) ──< clasificaciones (N) ──< reportes (1)
  │                              │                        │
  │                              │                        ├── errores (N)
  │                              │                        └── revisiones (N)
  │                              │
  │                              └── predicciones (N)
  │                              └── notificaciones (N)
  └── revisiones (N)
```

### Tablas principales
| Tabla | Propósito | PK | FKs |
|---|---|---|---|
| `usuarios` | Usuarios del sistema | `id_usuario` | - |
| `imagenes` | Imágenes subidas | `id_imagen` | `id_usuario` |
| `clasificaciones` | Resultados de IA | `id_clasificacion` | `id_imagen` |
| `reportes` | Reportes generados (JSON en contenido) | `id_reporte` | `id_clasificacion` (UNIQUE) |
| `predicciones` | Predicciones legacy | `id_prediccion` | `id_clasificacion` |
| `errores` | Errores de proceso | `id_error` | `id_reporte` |
| `revisiones` | Revisiones humanas | `id_revision` | `id_reporte`, `id_usuario` |
| `notificaciones` | Alertas del sistema | `id_notificacion` | `id_imagen`, `id_clasificacion` |
| `cola_analisis` | Cola de inferencia batch | `id_cola` | `id_usuario` |

### Convenciones BD
- Nombres en español (usuario, imagen, clasificacion, reporte)
- PKs con prefijo `id_` + nombre tabla singular
- FKs sin prefijo especial
- `DECIMAL(5,4)` para confianza (rango 0.0000 a 9.9999)
- Charset: `utf8mb4_spanish_ci`
- Engine: InnoDB con foreign keys + ON DELETE CASCADE

---

## APIs

### Auth (`/api/auth`)
| Method | Path | Auth | Descripción |
|---|---|---|---|
| POST | `/api/auth/login` | No | Login, retorna JWT + user info |
| POST | `/api/auth/register` | No | Registro de nuevo usuario |

### Analysis (`/api/analysis`)
| Method | Path | Auth | Descripción |
|---|---|---|---|
| GET | `/api/analysis/models` | Sí | Lista modelos IA disponibles |
| POST | `/api/analysis/upload` | Sí | Subir imagen + metadata + ejecutar IA |
| POST | `/api/analysis/upload-batch` | Sí | Subir múltiples imágenes + encolar en background |
| GET | `/api/analysis/queue` | Sí | Estado de los items en cola del usuario |
| GET | `/api/analysis/history` | Sí | Historial de análisis del usuario |
| GET | `/api/analysis/{id}` | Sí | Detalle completo de un análisis |
| GET | `/api/analysis/{id}/pdf` | Sí | Descargar PDF del reporte |

### Video Analysis (`/api/v1`)
| Method | Path | Auth | Descripción |
|---|---|---|---|
| POST | `/api/v1/analyze-video` | No | Subir video MP4/MKV, extraer frames, analizar con CNN |

### Panorama (`/api/v1`)
| Method | Path | Auth | Descripción |
|---|---|---|---|
| POST | `/api/v1/analyze-panorama` | No | Subir imagen panorámica, computar sliding window grid |

### Static
| Path | Descripción |
|---|---|
| `/uploads/{filename}` | Archivos subidos (imágenes, frames) |
| `/reports/{filename}` | PDFs generados |
| `/` | Health check: `{"message": "Backend MinerIA OK"}` |

---

## Reglas del Proyecto

1. **Versiones de API**: endpoints nuevos bajo `/api/v1/`, mantener compatibilidad
2. **Autenticación**: todos los endpoints de análisis requieren JWT (excepto v1 legacy)
3. **Roles**: solo "admin" y "analyst" (validado en login y BD)
4. **Formatos de archivo**: imágenes JPEG/PNG, videos MP4/MKV
5. **Modelos**: nuevos modelos deben implementar `AnalysisModel` protocol y registrarse en `MODEL_REGISTRY`
6. **Base de datos**: usar SQLAlchemy ORM, sesiones via `Depends(get_db)`
7. **Frontend**: usar `apiClient` (no `client.ts`), React Router, TailwindCSS
8. **JWT**: almacenar en localStorage, adjuntar via Axios interceptor
9. **Docker**: todo debe funcionar con `docker-compose up`
10. **Respuestas API**: usar Pydantic models para tipado, mensajes en español

---

## Pendientes Técnicos (Deuda Técnica)

1. **Código muerto legacy**: eliminar `Backend_cnn/main.py`, `app/routes/predict.py` (Flask), `app/routes/results.py`, `app/api/v1/analyze-video.py` (guión vs underscore)
2. **API client duplicado**: `client.ts` es idéntico a `apiClient.ts` - eliminar y consolidar
3. **Seguridad**: video y panorama endpoints no tienen autenticación
4. **JWT en localStorage**: vulnerable a XSS, migrar a httpOnly cookies
5. **Confianza 9975%**: seed data y reportes legacy muestran confianza `9975.0%` (bug de normalización en modelo anterior)
6. **CORS hardcodeado**: `allow_origins=["http://localhost:5173"]` debería ser configurable
7. **Paths absolutos en training**: `train_cnn.py` usa rutas Windows absolutas (no portables)
8. **`__init__.py` faltantes**: `app/ml/models/` y `app/ml/utils/` no tienen `__init__.py` (funciona por namespace packages, pero mejor práctica incluir)
9. **Logger formal ausente**: usa `print()` en lugar de logging module
10. **Rate limiting**: no hay límite de requests ni validación de tamaño de archivo real (el límite de 20GB en multipart es excesivo)
11. **Validación de contenido**: panorama solo valida content-type, no verifica que el archivo sea realmente una imagen válida antes de copiar

---

## Riesgos de Arquitectura

1. **Singleton models sin thread-safety**: `CopperCNN` y `MineralClassifier` son singletons globales, no hay garantía de thread safety en inferencia concurrente
2. **Modelos pesados en RAM**: ambos modelos cargados simultáneamente en memoria (~500MB+), puede escalar mal con más modelos
3. **Sin caché de inferencia**: cada request ejecuta el modelo desde cero, sin caché de resultados repetidos
4. **Dependencia de TensorFlow 2.16**: versión específica, puede tener problemas de compatibilidad con Python/OS futuros
5. **Upload sin límite real**: `max_part_size = 20GB` es esencialmente ilimitado, riesgo de DoS por upload gigante
6. **Single point of failure**: backend monolítico (API + ML + PDF), cualquier fallo afecta todo
7. **DB schema en español**: consistente pero puede causar problemas con herramientas que esperan inglés
8. **Frontend sin test**: no hay tests unitarios ni de integración en el frontend
9. **Backend sin tests**: no hay tests automatizados (pytest, etc.)
10. **`.env` con secretos en repositorio**: JWT_SECRET_KEY visible en el código, debería rotarse para producción
