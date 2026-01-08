# React Reference - Legacy Frontend

Esta carpeta contiene el código **original de React** que fue migrado a Django Templates.

**NO es parte del proyecto activo**, solo se mantiene como referencia de diseño.

## 📁 Contenido

### Componentes React (components/)
- `Dashboard.tsx` - Referencia de diseño del dashboard
- `Catedras.tsx` - Referencia del catálogo de cátedras
- `Recommendations.tsx` - Referencia de recomendaciones
- `ScrapingCenter.tsx` - Referencia del centro de scraping
- `Sidebar.tsx` - Referencia de la navegación lateral

### Servicios (services/)
- `api.ts` - Cliente API (para referencia de endpoints)
- `gemini.ts` - Integración con Google Gemini AI

### Root Files
- `App.tsx` - Componente principal React
- `index.tsx` - Entry point React
- `types.ts` - TypeScript types
- `constants.tsx` - Constantes y navegación

## 🎯 Propósito

Mantener estos archivos permite:
1. Consultar el diseño original al ajustar los templates Django
2. Recordar la lógica de negocio implementada
3. Migrar features faltantes si es necesario

## ⚠️ Estado

- **NO funcional**: No hay node_modules ni build
- **Solo lectura**: Para consulta de diseño
- **Eliminable**: Puede borrarse cuando todo esté estabilizado

## 🔄 Migrado a

Todos estos componentes fueron migrados a:
```
../templates/
├── base.html           (← Sidebar.tsx)
├── dashboard.html      (← Dashboard.tsx)
├── catedras.html       (← Catedras.tsx)
├── recommendations.html (← Recommendations.tsx)
└── scraping.html       (← ScrapingCenter.tsx)
```

---

**Última actualización**: 8 de enero de 2026
