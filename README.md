# ⛏️ MinerIA: Sistema Inteligente para la Detección de Cobre en Imágenes de Muestras Mineras

[cite_start]MinerIA es un sistema informático basado en inteligencia artificial que utiliza Redes Neuronales Convolucionales (CNNs) para analizar imágenes de muestras de suelo o rocas y determinar la presencia de cobre[cite: 64]. 

[cite_start]Este proyecto está diseñado para optimizar la fase de exploración inicial en la industria minera, enfocándose en Pequeñas y Medianas Empresas (PYMES) de exploración y Consultoras Geológicas[cite: 153, 154]. [cite_start]Busca reducir la dependencia de los métodos tradicionales de laboratorio, los cuales generan altos costos operativos superando los 500 dólares por muestra y demoras de hasta 4 semanas[cite: 126].

---

## ✨ Características Principales

* [cite_start]**Detección Automatizada:** Utiliza modelos de IA entrenados para ejecutar inferencias sobre imágenes de muestras, entregando predicciones de presencia de cobre con sus respectivos niveles de confianza[cite: 66, 82].
* [cite_start]**Explicabilidad (XAI):** Implementación de mapas de calor (Grad-CAM) para que el geólogo pueda validar visualmente qué áreas de la imagen detectó la inteligencia artificial[cite: 265].
* [cite_start]**Operación Offline (Edge Computing):** Capacidad de procesar la información directamente en terreno mediante hardware estándar, sin depender de una conexión a internet estable en zonas cordilleranas[cite: 234, 235].
* [cite_start]**Cumplimiento Normativo (RegTech):** Generación automatizada de reportes en PDF estructurados para servir como respaldo auditable ante entidades reguladoras (como el Decreto N° 9 de SERNAGEOMIN)[cite: 151, 231].

---

## 🛠️ Stack Tecnológico

El proyecto se divide en una arquitectura moderna basada en microservicios y despliegue en la nube, estructurada de la siguiente manera:

**Backend & API:**
* [cite_start][Python 3.x](https://www.python.org/) - Lenguaje principal[cite: 82].
* [cite_start][FastAPI](https://fastapi.tiangolo.com/) - Framework de alto rendimiento para la construcción de los endpoints (`/upload`, `/predict`)[cite: 82].
* [cite_start][PostgreSQL](https://www.postgresql.org/) - Base de datos relacional para el almacenamiento del historial de análisis y metadatos[cite: 82].

**Inteligencia Artificial & Visión Computacional:**
* [cite_start]**Redes Neuronales Convolucionales (CNNs)**[cite: 64, 86].
* [cite_start]Librerías de procesamiento de imágenes (OpenCV)[cite: 145].
* [cite_start]Técnicas de *Data Augmentation* y normalización para el preprocesamiento de imágenes[cite: 91].

---

## 🚀 Instalación y Configuración Local

Sigue estos pasos para levantar el entorno de desarrollo backend de MinerIA en tu máquina local.

### Prerrequisitos
* Python 3.9 o superior.
* PostgreSQL instalado y corriendo localmente.

### Pasos

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/MinerIA.git](https://github.com/tu-usuario/MinerIA.git)
   cd MinerIA
