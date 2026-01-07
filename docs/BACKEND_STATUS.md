# Backend - Sistema de Recomendaciones de Cátedras

## ✅ Estado Actual: COMPLETADO

### 📊 Estructura de Apps Implementada

```
backend/
├── users/              ✅ Gestión de usuarios
│   └── User (AbstractUser)
│
├── academic/           ✅ Datos académicos
│   └── Catedra (~500 cátedras)
│
├── scraping/           ✅ Sistema de scraping colaborativo
│   ├── Grupos (grupos de Facebook)
│   ├── Tarea_Scrapeo (tareas pendientes)
│   ├── Sesion_Scraping (sesiones de usuarios)
│   └── Post_Scrapeado (posts extraídos)
│
└── recommendations/    ✅ Sistema de recomendaciones
    ├── Recomendacion (recomendaciones procesadas)
    └── Cache_Metadatos (control de versiones)
```

### 🗄️ Modelos Implementados (según diagrama ERD)

| Modelo | App | Descripción | Estado |
|--------|-----|-------------|--------|
| **User** | users | Usuario del sistema (AbstractUser) | ✅ |
| **Catedra** | academic | Cátedra universitaria (~500) | ✅ |
| **Grupos** | scraping | Grupos de Facebook a scrapear | ✅ |
| **Tarea_Scrapeo** | scraping | Tareas de scraping pendientes | ✅ |
| **Sesion_Scraping** | scraping | Sesiones de scraping por usuario | ✅ |
| **Post_Scrapeado** | scraping | Posts extraídos (post_id único) | ✅ |
| **Recomendacion** | recommendations | Recomendaciones procesadas con NLP | ✅ |
| **Cache_Metadatos** | recommendations | Control de versiones para cache | ✅ |

### 🔗 Relaciones Implementadas

```
User
  ├── 1:N → Sesion_Scraping
  └── 1:N → Recomendacion (contribuidor)

Grupos
  ├── 1:N → Tarea_Scrapeo
  └── 1:N → Post_Scrapeado

Tarea_Scrapeo
  └── 1:N → Sesion_Scraping

Sesion_Scraping
  ├── FK → User
  ├── FK → Tarea_Scrapeo
  └── 1:N → Post_Scrapeado

Post_Scrapeado
  ├── FK → Grupos
  ├── FK → Sesion_Scraping
  └── 1:N → Recomendacion

Catedra
  └── 1:N → Recomendacion

Recomendacion
  ├── FK → Catedra
  ├── FK → Post_Scrapeado (post_origen)
  ├── FK → User (contribuidor)
  └── FK → Sesion_Scraping
```

### ⚙️ Configuración

- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Cache**: LocMemCache (en memoria, sin Redis)
- **Usuario Modelo**: Custom User (`users.User`)
- **Admin**: Configurado para todos los modelos

### 🔐 Acceso al Admin

```
URL: http://localhost:8000/admin/
Usuario: admin
Contraseña: admin123
```

### 🚀 Comandos Útiles

```bash
# Activar entorno virtual
cd "/mnt/nobara-data/proyectos/Recos completo"
source venv/bin/activate

# Ir al directorio backend
cd backend

# Ejecutar servidor
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell interactivo
python manage.py shell
```

### 📝 Próximos Pasos

1. **API RESTful**
   - Crear serializers para cada modelo
   - Implementar ViewSets con DRF
   - Configurar rutas de la API

2. **Endpoints Principales**
   - `GET /api/catedras/` - Listar cátedras
   - `GET /api/catedras/{codigo}/` - Detalle de cátedra
   - `GET /api/recomendaciones/` - Listar recomendaciones
   - `POST /api/scraping/sesiones/` - Iniciar sesión de scraping
   - `POST /api/scraping/posts/` - Enviar posts scrapeados

3. **Frontend / Extensión**
   - Consumir API desde extensión Chrome
   - Mostrar datos en interfaz web
   - Sistema de búsqueda de cátedras

### 🎯 Características Implementadas

- ✅ Modelo de datos completo según ERD
- ✅ Custom User Model
- ✅ Admin panel configurado
- ✅ Migraciones creadas y aplicadas
- ✅ Cache en memoria (sin dependencias de Redis)
- ✅ Índices optimizados en BD
- ✅ Timestamps automáticos
- ✅ Validaciones y choices

### 📊 Campos Importantes

**Catedra:**
- `codigo` (unique) - Identificador único
- `nombre` - Nombre de la cátedra
- `titular` - Profesor a cargo
- `mencion_fb` - Contador de menciones
- `activa` - Estado actual

**Post_Scrapeado:**
- `post_id` (unique) - Evita duplicados
- `procesado` - Si ya fue analizado con NLP
- `texto` - Contenido del post

**Recomendacion:**
- `sentimiento` - positivo/negativo/neutral
- `confianza` - Nivel de confianza NLP (0-1)
- `votos_utilidad` - Votación comunitaria

**Cache_Metadatos:**
- `version` - Versión actual del dataset
- `hash` - Verificación de integridad
- Métodos: `get_current_version()`, `increment_version()`

### 🔍 Características de Búsqueda

Todos los modelos tienen configurados:
- **search_fields** en el admin
- **list_filter** para filtrado rápido
- **ordering** para ordenamiento por defecto
- **indexes** en BD para consultas rápidas

---

**Fecha**: 7 de enero de 2026  
**Estado**: Backend listo para desarrollo de API
