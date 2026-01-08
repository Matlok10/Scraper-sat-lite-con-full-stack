# Scraper SAT - Sistema de Recomendaciones Académicas (Full Stack)

Este proyecto es una plataforma integral para agregar, procesar y visualizar recomendaciones de cátedras universitarias, extraídas automáticamente de grupos de Facebook mediante scraping y procesamiento de lenguaje natural (NLP).

> **Nota**: Este documento se centra principalmente en la arquitectura y funcionalidad del **Backend**.

## 🏗 Arquitectura del Backend

El backend está construido con **Django 6.0** y **Django REST Framework (DRF)**. Utiliza una arquitectura modular separada en aplicaciones con responsabilidades específicas.

### Estructura de Directorios

```text
backend/
├── academic/          # Gestión de entidades académicas (Docentes, Comisiones)
├── recommendations/   # Lógica central de recomendaciones y análisis
├── scraping/          # Gestión de tareas de scraping y datos crudos
├── users/             # Gestión de usuarios y autenticación
├── config/            # Configuración global del proyecto (settings, urls)
└── utils/             # Utilidades transversales
```

---

## 📦 Aplicaciones y Funcionalidad

### 1. 🎓 Academic (`backend/academic`)

Responsable de modelar la estructura estática de la universidad (profesores y cursos).

* **Modelos Principales**:
  * **`Docente`**: Almacena información de profesores. Incluye un campo `alias_search` para mejorar la búsqueda difusa.
  * **`Comision`**: Representa una instancia de una materia (Cátedra). Vincula un código único, un docente titular, horarios y metadatos administrativos.

* **Funcionalidad Clave**:
  * Catalogación unificada de toda la oferta académica.
  * Base sobre la cual se agregan las recomendaciones.

### 2. 🤖 Recommendations (`backend/recommendations`)

El "cerebro" del sistema. Transforma datos crudos en información útil.

* **Modelos Principales**:
  * **`Recomendacion`**: El núcleo del valor. Vincula un `Post_Scrapeado` con una `Comision`.
    * **Análisis NLP**: Campos `sentimiento` (Positivo/Negativo/Neutral) y `confianza` (0-1).
    * **Extracción de Datos**: `prob_aprobar`, `toma_tp`, `asistencia`.
    * **Votación**: Sistema de `votos_utilidad` para ranking comunitario.
  * **`Cache_Metadatos`**: Sistema de versionado (entero incremental) que permite a los clientes (Frontend/Extensión) verificar si necesitan redescargar el dataset de recomendaciones, optimizando el ancho de banda.

### 3. 🕷 Scraping (`backend/scraping`)

Motor de ingesta de datos. Gestiona la orquestación del scraping, aunque la ejecución real puede ocurrir en clientes externos (extensión de navegador o workers).

* **Modelos Principales**:
  * **`Grupos`**: URLs de fuentes de datos (Grupos de Facebook).
  * **`Tarea_Scrapeo`**: Define **qué** buscar. Contiene `keywords` y una frecuencia de actualización.
  * **`Sesion_Scraping`**: Telemetría y logs de cada ejecución de scraping. Registra inicio, fin, estado y cantidad de posts encontrados.
  * **`Post_Scrapeado`**: Data Lake de contenido crudo. Almacena el texto original del post y metadatos de Facebook para auditoría y reprocesamiento.

* **Flujo de Trabajo**:
    1. El Backend genera una `Tarea_Scrapeo`.
    2. Un Worker/Extensión consulta la API por tareas pendientes.
    3. El Worker ejecuta el scraping y sube los resultados como `Post_Scrapeado`.
    4. El Backend (signal/task) procesa el post para crear `Recomendacion`.

### 4. 👥 Users (`backend/users`)

Gestión personalizada de usuarios.

* **Modelos**:
  * **`User`**: Hereda de `AbstractUser` de Django. Preparado para extensión futura (perfiles, avatares, roles académicos).
* **Funcionalidad**:
  * Autenticación vía Token/Session para la API.
  * Control de acceso para colaboradores del scraping.

---

## 🔌 API Reference

El proyecto expone una API RESTful en `/api/`.

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/catedras/` | GET | Listado de comisiones y sus recomendaciones agregadas. |
| `/api/grupos/` | GET, POST | Gestión de grupos de Facebook a monitorear. |
| `/api/tareas/` | GET, POST | Tareas de scraping pendientes para workers. |
| `/api/sesiones/` | POST | Reporte de progreso/finalización de scraping. |
| `/api/posts/` | POST | Ingesta de nuevos posts crudos. |

---

## 🛠 Configuración y Tecnologías

* **Base de Datos**: SQLite (Dev) / PostgreSQL (Prod - Recomendado).
* **Cola de Tareas**: Celery + Redis (para procesamiento asíncrono de NLP).
* **Servidor WSGI**: Gunicorn (Configurado en `requirements.txt`).
* **Variables de Entorno**: Gestionadas via `django-environ` (ver `.env.example`).

### Iniciar Entorno Local

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r backend/requirements.txt

# Migraciones
python backend/manage.py migrate

# Iniciar servidor
python backend/manage.py runserver
```
