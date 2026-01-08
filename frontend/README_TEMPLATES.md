# Frontend - Django Templates + Tailwind CSS

Este directorio contiene la interfaz de usuario del proyecto Academia Scraper AI, ahora implementada como **Django Templates** en lugar de una aplicación React separada.

## 📁 Estructura

```
frontend/
├── templates/              # Plantillas HTML (servidas por Django)
│   ├── base.html          # Layout base con navbar y sidebar
│   ├── dashboard.html     # Panel principal
│   ├── catedras.html      # Directorio de cátedras
│   ├── recommendations.html   # Base de recomendaciones
│   ├── scraping.html      # Centro de scraping
│   ├── history.html       # Historial de sesiones
│   └── includes/
│       └── sidebar.html   # Componente de navegación lateral
├── static/                # Archivos estáticos (CSS, JS, imágenes)
│   ├── css/
│   │   ├── tailwind.css   # Compilado de Tailwind (generado)
│   │   └── custom.css     # Estilos personalizados
│   └── js/
│       └── charts.js      # Scripts para gráficos (opcional)
├── components/            # Componentes React originales (referencia)
├── services/              # Servicios TS/JS originales (referencia)
└── package.json          # Dependencias (solo si usamos Tailwind CLI)
```

## 🎨 Tecnologías

- **Django Templates**: Renderizado en servidor
- **Tailwind CSS**: Utilidad-first CSS framework (via CDN en base.html)
- **HTML5/JavaScript vanilla**: Sin frameworks frontend complejos

## 🚀 Desarrollo

### Ver los cambios en tiempo real

1. Asegúrate que Django esté corriendo:
```bash
cd backend
python manage.py runserver
```

2. Abre http://127.0.0.1:8000 en tu navegador

3. Los cambios en los templates se reflejan automáticamente (con recarga de página)

### Editar un template

Simplemente modifica cualquier archivo en `frontend/templates/` y recarga el navegador.

**Ejemplo**: Para agregar una columna a la tabla de cátedras, edita `catedras.html`.

## 📊 Context Variables

Cada template recibe datos del Django view correspondiente:

### Dashboard (`dashboard.html`)
```python
{
    'stats': {
        'total_catedras': int,
        'total_posts': int,
        'total_recommendations': int,
        'active_sessions': int,
    },
    'top_catedras': QuerySet[Comision],
    'recent_sessions': QuerySet[Sesion_Scraping],
    'today': date,
}
```

### Cátedras (`catedras.html`)
```python
{
    'catedras': QuerySet[Comision],  # Con anotación recommendation_count
}
```

### Recomendaciones (`recommendations.html`)
```python
{
    'recommendations': QuerySet[Recomendacion],  # Ordenado por -id
}
```

### Scraping (`scraping.html`)
```python
{
    'grupos': QuerySet[Grupo],
    'tareas': QuerySet[Tarea_Scrapeo],
    'unprocessed_posts_count': int,
}
```

### Historial (`history.html`)
```python
{
    'sesiones': QuerySet[Sesion_Scraping],
}
```

## 🔧 Customización de Estilos

### Agregar estilos globales

Edita `static/css/custom.css`:

```css
.mi-clase {
    @apply bg-white p-6 rounded-lg shadow;
}
```

### Usar Tailwind en los templates

Todos los templates ya usan clases Tailwind. Tailwind está cargado via CDN en `base.html`:

```html
<script src="https://cdn.tailwindcss.com"></script>
```

Si necesitas compilación optimizada para producción, instala Tailwind CLI:

```bash
npm install -D tailwindcss
npm run build:css
```

## 📱 Componentes Reutilizables

Las vistas comunes están en `includes/`:

- **`sidebar.html`**: Navegación principal (incluido en base.html)
- **Más componentes pueden agregarse** en esta carpeta

### Incluir un componente

```html
{% include 'includes/componente.html' %}
```

## 🔗 URLs y Navegación

Las rutas disponibles son:

| Ruta | Template | Nombre |
|------|----------|--------|
| `/` | `dashboard.html` | `dashboard` |
| `/catedras/` | `catedras.html` | `catedras` |
| `/recomendaciones/` | `recommendations.html` | `recommendations` |
| `/scraping/` | `scraping.html` | `scraping` |
| `/historial/` | `history.html` | `history` |

### Enlazar en templates

```html
<a href="{% url 'dashboard' %}">Dashboard</a>
```

## 🚢 Deployment

Para producción, el servidor WSGI (Gunicorn) sirve tanto la API (`/api/`) como los templates (`/`).

No hay necesidad de build step:

```bash
# Solo instalar dependencias Python
pip install -r backend/requirements.txt

# Recolectar statics
python backend/manage.py collectstatic --noinput

# Correr Gunicorn
gunicorn config.wsgi:application
```

## 📚 Referencia de Componentes Originales

Los componentes React originales se mantienen en `components/` como referencia de diseño:

- `Dashboard.tsx` → `templates/dashboard.html`
- `Catedras.tsx` → `templates/catedras.html`
- `Recommendations.tsx` → `templates/recommendations.html`
- `ScrapingCenter.tsx` → `templates/scraping.html`
- `Sidebar.tsx` → `templates/includes/sidebar.html`

Se pueden eliminar cuando todo esté estabilizado.

## 🐛 Troubleshooting

### Los templates no aparecen

Asegúrate que en `backend/config/settings/base.py`:

```python
TEMPLATES[0]['DIRS'] = [BASE_DIR.parent / 'frontend' / 'templates']
```

### Los estilos no se cargan

Ejecuta:

```bash
cd backend
python manage.py collectstatic
```

### Template tag `url` no funciona

Asegúrate que en `urls.py` los nombres son correctos:

```python
path('catedras/', CatedrasView.as_view(), name='catedras'),
```

---

**Última actualización**: 8 de enero de 2026
