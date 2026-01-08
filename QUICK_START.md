# 🚀 Quick Start - Academia Scraper AI

## ¿Qué acaba de pasar?

La interfaz web ha sido **migrada de React a Django Templates**. Ahora todo es un proyecto monolítico más simple.

```
ANTES:                          AHORA:
├── backend/ (Django)           └── Proyecto Único (Django)
├── frontend/ (React 19)            ├── Backend API
└── package.json                    ├── Frontend Templates
                                    └── Admin Panel
```

## ✅ Iniciar en 3 pasos

### 1. Preparar el entorno
```bash
cd /mnt/nobara-data/proyectos/Recos\ completo
source venv/bin/activate
```

### 2. Ejecutar migraciones (una sola vez)
```bash
cd backend
python manage.py migrate
```

### 3. Correr el servidor
```bash
python manage.py runserver
```

**Listo**. Abre http://127.0.0.1:8000 en tu navegador.

---

## 📍 Rutas disponibles

| URL | Qué hace |
|-----|----------|
| `http://localhost:8000/` | Dashboard |
| `http://localhost:8000/catedras/` | Listado de cátedras |
| `http://localhost:8000/recomendaciones/` | Base de recomendaciones |
| `http://localhost:8000/scraping/` | Centro de scraping |
| `http://localhost:8000/historial/` | Historial |
| `http://localhost:8000/admin/` | Panel admin |

---

## 🔧 Editar la interfaz

**Todo está en una carpeta**: `frontend/`

### Cambiar el Dashboard
```
Edita: frontend/templates/dashboard.html
Recarga: F5 en el navegador
```

### Cambiar estilos
```
Edita: frontend/static/css/custom.css
Recarga: Ctrl+Shift+R (hard refresh)
```

### Cambiar datos mostrados
```
Edita: backend/config/views.py
Reinicia: Ctrl+C en terminal, luego python manage.py runserver
```

---

## 📊 Estructura actual

```
project/
├── backend/
│   ├── config/
│   │   ├── urls.py          ← Las rutas viven aquí
│   │   ├── views.py         ← Las vistas (NUEVO)
│   │   └── settings/base.py ← Configuración
│   ├── academic/            ← Modelos de cátedras
│   ├── recommendations/     ← Modelos de recomendaciones
│   ├── scraping/           ← Modelos de scraping
│   ├── users/              ← Modelos de usuarios
│   └── manage.py           ← Script principal
│
├── frontend/
│   ├── templates/          ← Plantillas HTML (NUEVO)
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── catedras.html
│   │   ├── recommendations.html
│   │   ├── scraping.html
│   │   ├── history.html
│   │   └── includes/sidebar.html
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css
│   │   └── js/
│   └── components/         ← Referencias (legacy)
│
└── venv/                   ← Entorno Python
```

---

## 🎨 Tecnologías

- **Backend**: Django 6.0 + Django REST Framework
- **Frontend**: HTML + Tailwind CSS (via CDN)
- **Base de datos**: SQLite (dev) / PostgreSQL (prod)
- **No necesita**: npm, Node.js, bundler

---

## ❓ FAQ

### ¿Dónde está React?
Eliminado. Los componentes están en `frontend/components/` como referencia.

### ¿Puedo usar JavaScript?
Sí. Agrega scripts en `frontend/templates/` o `frontend/static/js/`.

### ¿Cómo cambio el logo o colores?
- Logo: Edita `frontend/templates/includes/sidebar.html` (línea ~5)
- Colores: Modifica clases Tailwind en los templates

### ¿Los datos son reales?
Depende de tu base de datos. Los templates esperan que los modelos Django estén poblados.

### ¿Cómo agrego una nueva página?
1. Crea `frontend/templates/mi_pagina.html`
2. Crea una vista en `backend/config/views.py`
3. Agrega la ruta en `backend/config/urls.py`

---

## 📈 Próximos pasos

- [ ] Test de la interfaz (verificar que cargue todo)
- [ ] Conectar datos reales desde BD
- [ ] Mejorar responsive design para móvil
- [ ] Agregar formularios interactivos
- [ ] Deploy en producción

---

## 🆘 Algo no funciona?

### Template not found
```bash
python manage.py collectstatic --clear --noinput
python manage.py runserver
```

### 500 Error
Revisa `backend/manage.py runserver` en la terminal (mostrará el error exacto).

### Los estilos no cargan
```bash
# Hard refresh en el navegador
Ctrl+Shift+R (Chrome/Firefox)
Cmd+Shift+R (Mac)
```

---

**¡A coding!** 🚀

Última actualización: 8 de enero de 2026
