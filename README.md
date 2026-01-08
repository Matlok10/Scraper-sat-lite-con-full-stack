# Scraper SAT - Sistema de Recomendaciones Académicas (Full Stack)

Este proyecto es una plataforma integral para agregar, procesar y visualizar recomendaciones de cátedras universitarias, extraídas automáticamente de grupos de Facebook mediante scraping y procesamiento de lenguaje natural (NLP).

> **Nota**: Este documento se centra principalmente en la arquitectura y funcionalidad del **Backend**. La interfaz web está implementada como **Django Templates** integrados en el mismo proyecto.

## 🏗 Arquitectura del Backend

El backend está construido con **Django 6.0** y **Django REST Framework (DRF)**. Utiliza una arquitectura modular separada en aplicaciones con responsabilidades específicas.

### Estructura de Directorios

```text
Recos completo/
├── backend/              # Backend Django (core)
│   ├── academic/         # Gestión de entidades académicas
│   ├── recommendations/  # Lógica de recomendaciones
│   ├── scraping/         # Gestión de scraping
│   ├── users/            # Autenticación y usuarios
│   ├── config/           # Configuración global
│   └── utils/            # Utilidades
├── frontend/             # Frontend (Django Templates)
│   ├── templates/        # Plantillas HTML
│   ├── static/           # CSS, JS, imágenes
│   └── components/       # Referencias de diseño React (legacy)
├── extension/            # Extensión de navegador
├── docs/                 # Documentación adicional
└── venv/                 # Entorno virtual Python
```

---

## 📦 Aplicaciones y Funcionalidad

### 1. 🎓 Academic (`backend/academic`)

Responsable de modelar la estructura estática de la universidad (profesores y cursos).

* **Modelos Principales**:
  * **`Docente`**: Almacena información de profesores. Incluye un campo `alias_search` para mejorar la búsqueda difusa.
  * **`Comision`**: Representa una instancia de una materia (Cátedra). Vincula un código único, un docente titular, horarios y metadatos administrativos.
    * **Identificador Único**: `(codigo, docente, horario, cuatrimestre)` - permite múltiples horarios para la misma comisión
    * **Campos de Recomendaciones**: 10 campos estructurados listos para procesamiento por scraper NLP
    * **Modalidad**: Presencial/Remota/Híbrida

* **Funcionalidad Clave**:
  * Catalogación unificada de toda la oferta académica (✅ 1751 comisiones reales importadas)
  * Base sobre la cual se agregan las recomendaciones
  * Sistema de importación CSV robusto con detección automática de encoding
  * Búsqueda fuzzy de docentes con alias
  * API REST completa con filtros y paginación

* **Estado**: ✅ **Fase 2 Completada** - Sistema de importación robusto, modelos refinados, API funcional

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

Gestión personalizada de usuarios con sistema de roles y gamificación.

* **Modelos**:
  * **`User`**: Hereda de `AbstractUser` de Django.
    * **Sistema de Roles**: `estudiante`, `colaborador`, `moderador`, `admin`
    * **Gamificación**: `puntos`, `contribuciones_aprobadas`
    * **Metadata Scraping**: `puede_scrapear`, `sesiones_scraping_activas`

* **Funcionalidad**:
  * Autenticación vía Token para la API (`/api/auth/login/`, `/api/auth/logout/`)
  * Control de acceso granular basado en roles
  * Endpoint `/api/users/me/` para perfil propio
  * Endpoint `/api/users/{id}/assign_role/` para asignación de roles (solo admin)
  * Sistema de puntos para incentivar contribuciones de calidad

* **Estado**: ✅ **Fase 1 Completada** - Sistema de roles, permisos y gamificación implementados y testeados

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

* **Backend**: Django 6.0 + Django REST Framework
* **Base de Datos**: SQLite (Dev) / PostgreSQL (Prod - Recomendado).
* **Cola de Tareas**: Celery + Redis (para procesamiento asíncrono de NLP).
* **Servidor WSGI**: Gunicorn (Configurado en `requirements.txt`).
* **Frontend**: Django Templates + Tailwind CSS (sin framework JS separado)
* **Variables de Entorno**: Gestionadas via `django-environ` (ver `.env.example`).

---

## 🎨 Frontend - Django Templates

El frontend está completamente integrado en el proyecto Django como **templates HTML** + **CSS Tailwind**, eliminando la complejidad de un SPA React separado.

### Características

✅ **Sin build step**: Cambios en templates reflejados inmediatamente  
✅ **Renderizado servidor**: Mejor rendimiento y SEO  
✅ **Integración directa**: Acceso a contexto de Django en templates  
✅ **Tamaño mínimo**: 192KB vs 186MB de node_modules  
✅ **Un solo deploy**: API + UI en el mismo contenedor  

### Vistas Disponibles

| URL | Descripción |
|-----|-------------|
| `/` | Dashboard con estadísticas |
| `/catedras/` | Directorio de cátedras |
| `/recomendaciones/` | Base de recomendaciones |
| `/scraping/` | Centro de scraping |
| `/historial/` | Historial de sesiones |

### Estructura

```
frontend/
├── templates/              # Plantillas Django
│   ├── base.html          # Layout principal
│   ├── dashboard.html     # Panel de control
│   ├── catedras.html      # Catálogo de cátedras
│   ├── recommendations.html
│   ├── scraping.html
│   ├── history.html
│   └── includes/sidebar.html
├── static/css/
│   ├── custom.css         # Estilos personalizados
│   └── tailwind.css       # Tailwind (compilado si es necesario)
└── README_TEMPLATES.md    # Documentación detallada
```

Para más detalles sobre el frontend, ver [frontend/README_TEMPLATES.md](frontend/README_TEMPLATES.md).

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

# Abre http://127.0.0.1:8000
```

---

## 📊 API Reference

El proyecto expone una API RESTful en `/api/`.

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/catedras/` | GET | Listado de comisiones y sus recomendaciones agregadas. |
| `/api/grupos/` | GET, POST | Gestión de grupos de Facebook a monitorear. |
| `/api/tareas/` | GET, POST | Tareas de scraping pendientes para workers. |
| `/api/sesiones/` | POST | Reporte de progreso/finalización de scraping. |
| `/api/posts/` | POST | Ingesta de nuevos posts crudos. |
| `/api/users/` | GET | Listar usuarios (solo admin). |
| `/api/auth/login/` | POST | Autenticación. |
| `/api/auth/logout/` | POST | Cerrar sesión. |

---

## 🚀 Deployment

### Producción

```bash
# Recolectar archivos estáticos
python backend/manage.py collectstatic --noinput

# Correr con Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 config.wsgi:application
```

El serviauth/login/` | POST | Autenticación y obtención de token |
| `/api/auth/logout/` | POST | Cerrar sesión e invalidar token |
| `/api/users/` | GET | Listar usuarios (solo admin) |
| `/api/users/me/` | GET | Ver perfil del usuario actual |
| `/api/users/{id}/assign_role/` | POST | Asignar rol a usuario (solo admin) |
| `/api/docentes/` | GET | Listado de docentes con búsqueda fuzzy |
| `/api/docentes/{id}/` | GET | Detalle de docente con comisiones |
| `/api/comisiones/` | GET | Listado de comisiones con filtros |
| `/api/comisiones/{id}/` | GET | Detalle de comisión con docente |
| `/api/grupos/` | GET, POST | Gestión de grupos de Facebook a monitorear |
| `/api/tareas/` | GET, POST | Tareas de scraping pendientes para workers |
| `/api/sesiones/` | POST | Reporte de progreso/finalización de scraping |
| `/api/posts/` | POST | Ingesta de nuevos posts crudos
- 35+ tests de funcionalidad y seguridad

### ✅ Fase 2: App Academic (COMPLETADA)
- Modelos Docente y Comision refinados
- Importación CSV robusta (1751 comisiones reales)
- Búsqueda fuzzy de docentes
- Serializers anidados funcionales
- Sistema preparado para recomendaciones (10 campos estructurados)
- Tests completos de modelos, API e importación

### 🎯 Fase 3: App Recommendations (PRÓXIMA)
- Crear scraper NLP para procesar recomendaciones
- Implementar análisis de sentimiento
- Sistema de votación comunitaria
- Endpoint de recomendaciones con filtros
- Tests de NLP y votación

### 📋 Fase 4: App Scraping (PENDIENTE)
- Validar permisos de scraping por rol
- Limitar sesiones concurrentes por usuario
- Preparar integración con extensión Chrome

---

## 📚 Documentación

La documentación completa del backend está organizada en `backend/docs/`:

- **[backend/docs/README.md](backend/docs/README.md)** - Índice maestro de documentación
- **[backend/docs/academic/](backend/docs/academic/)** - Documentación de Academic (importación, duplicados, soluciones)
- **[backend/docs/testing/](backend/docs/testing/)** - Guías de tests y cobertura
- **[backend/docs/scraper/](backend/docs/scraper/)** - Preparación del scraper NLP

---

## 🧪 Testing

El proyecto cuenta con una suite completa de tests automatizados.

### Ejecutar Tests

```bash
cd backend
source ../venv/bin/activate

# Todos los tests
python manage.py test

# Tests de una app específica
python manage.py test users
python manage.py test academic
python manage.py test tests.test_academic_search

# Con más detalle
python manage.py test --verbosity=2

# Script automatizado
./run_tests.sh
```

### Cobertura Actual

- **Users**: ✅ 35+ tests (modelos, autenticación, permisos, roles)
- **Academic**: ✅ Tests de modelos, búsqueda fuzzy, importación CSV
- **API**: ✅ Tests de endpoints principales

📚 **Documentación de Tests**: Ver `backend/docs/testing/` para guías detalladas

---

## 🔄 Hoja de Ruta

- ✅ **Fase 1**: Sistema de usuarios con roles y permisos
- 🔄 **Fase 2**: Completar app Academic con búsqueda fuzzy
- 🎯 **Fase 3**: NLP y análisis de sentimiento en Recommendations
- 📋 **Fase 4**: Integración con extensión de navegador (Scraping)
