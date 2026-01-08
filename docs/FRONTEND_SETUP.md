# Frontend Setup & Integration

## ✅ Estructura creada

- `/frontend/` - Código React/Vite completo
- Todos los componentes copiados (Sidebar, Dashboard, Catedras, ScrapingCenter, Recommendations)
- Configuración de build apunta a `backend/static/frontend`

## 📋 Pasos para activar el frontend

### 1. Instalar dependencias
```bash
cd frontend
npm install
```

### 2. Build para producción
```bash
npm run build
```
Esto genera los archivos en `backend/static/frontend/`

### 3. Modo desarrollo (opcional)
```bash
npm run dev
```
Corre en http://localhost:3000

### 4. Django ya está configurado
- URL catch-all en `config/urls.py` sirve el SPA
- Visita http://127.0.0.1:8000 (cualquier ruta que no sea /admin)

## 🔄 Próximos pasos

1. Crear serializers y viewsets DRF para las 4 apps
2. Exponer endpoints `/api/catedras/`, `/api/grupos/`, etc.
3. Reemplazar `INITIAL_STATE` en frontend por fetch a esos endpoints
4. Implementar autenticación (JWT/Session)
