# Setup del Proyecto Recomendaciones

## Estructura de Entornos Virtuales

Este proyecto tiene **UN ÚNICO entorno virtual** en la raíz:

```
Recos completo/
├── venv/                    ← ÚNICO VENV (todos los proyectos lo usan)
├── backend/
│   ├── manage.py
│   ├── config/
│   ├── requirements.txt
│   └── ...
├── extension/               ← Futuro (Node.js)
└── docs/
```

## Activar el Entorno

```bash
cd "/mnt/nobara-data/proyectos/Recos completo"
source venv/bin/activate

# Verificar que está activado (deberías ver (venv) en el prompt)
which python
```

## Trabajar con Django

```bash
# Con el venv activado:
cd backend
python manage.py runserver
python manage.py migrate
python manage.py startapp <nombre>
```

## Instalar Nuevas Dependencias

```bash
# Con el venv activado
pip install <paquete>
pip freeze > backend/requirements.txt  # Actualizar requirements
```

## ⚠️ IMPORTANTE

- **NO crear venvs adicionales** en `backend/` o en otras carpetas
- Todos los proyectos usan el mismo venv en la raíz
- Después de cualquier `pip install`, actualizar `requirements.txt`
- El venv está en `.gitignore`, no se sube a git
