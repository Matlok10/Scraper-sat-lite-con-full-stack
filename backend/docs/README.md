# 📚 Documentación del Backend

Esta carpeta contiene toda la documentación técnica del backend del Sistema de Recomendaciones Académicas.

## 📁 Estructura

```
docs/
├── README.md                    # Este archivo (índice maestro)
├── academic/                    # Documentación del módulo Academic
│   ├── CAMBIOS_IDENTIFICADOR_UNICO.md
│   ├── EXPLICACION_IMPORTACION.md
│   ├── PROBLEMA_DUPLICADOS_COMISIONES.md
│   ├── README_IMPORTACION.md
│   ├── RESUMEN_SOLUCION_FINAL.md
│   └── SOLUCION_CORRECTA_IDENTIFICADOR_UNICO.md
├── testing/                     # Documentación de tests
│   ├── README.md
│   ├── ESTRUCTURA_TESTS.md
│   ├── README_ACADEMIC_TESTS.md
│   ├── RESUMEN_TESTS_ACADEMIC.md
│   ├── test_academic_api.md
│   ├── test_academic_import.md
│   ├── test_academic_models.md
│   ├── test_users_auth.md
│   ├── test_users_model.md
│   └── test_users_roles.md
└── scraper/                     # Documentación del scraper
    └── PREPARACION_SCRAPER_RECOMENDACIONES.md
```

---

## 🎓 Academic - Gestión de Comisiones y Docentes

### Documentación Principal
- [README_IMPORTACION.md](academic/README_IMPORTACION.md) - Guía completa de importación de comisiones

### Problema y Solución del Identificador Único
1. [PROBLEMA_DUPLICADOS_COMISIONES.md](academic/PROBLEMA_DUPLICADOS_COMISIONES.md) - Descripción del problema inicial
2. [CAMBIOS_IDENTIFICADOR_UNICO.md](academic/CAMBIOS_IDENTIFICADOR_UNICO.md) - Primera iteración de cambios
3. [SOLUCION_CORRECTA_IDENTIFICADOR_UNICO.md](academic/SOLUCION_CORRECTA_IDENTIFICADOR_UNICO.md) - Solución correcta implementada
4. [RESUMEN_SOLUCION_FINAL.md](academic/RESUMEN_SOLUCION_FINAL.md) - Resumen ejecutivo de la solución
5. [EXPLICACION_IMPORTACION.md](academic/EXPLICACION_IMPORTACION.md) - Explicación detallada de la lógica de importación

### Características Principales
- ✅ Importación de 1751 comisiones reales desde CSV
- ✅ Manejo correcto de duplicados (mismo código, diferentes horarios)
- ✅ Identificador único: `(codigo, docente, horario, cuatrimestre)`
- ✅ Soporte para múltiples encodings (UTF-8-SIG, ISO-8859-1, CP1252)
- ✅ Detección automática de headers y skipeo de filas innecesarias
- ✅ Campos preparados para recomendaciones (10 campos estructurados)

---

## 🧪 Testing - Suite de Tests Automatizados

### Documentación de Tests
- [README.md](testing/README.md) - Guía de ejecución de tests
- [ESTRUCTURA_TESTS.md](testing/ESTRUCTURA_TESTS.md) - Estructura de la suite de tests

### Tests de Users
- [test_users_model.md](testing/test_users_model.md) - Tests del modelo User
- [test_users_auth.md](testing/test_users_auth.md) - Tests de autenticación
- [test_users_roles.md](testing/test_users_roles.md) - Tests de roles y permisos

### Tests de Academic
- [README_ACADEMIC_TESTS.md](testing/README_ACADEMIC_TESTS.md) - Guía de tests de Academic
- [RESUMEN_TESTS_ACADEMIC.md](testing/RESUMEN_TESTS_ACADEMIC.md) - Resumen de tests de Academic
- [test_academic_models.md](testing/test_academic_models.md) - Tests de modelos (Docente, Comision)
- [test_academic_api.md](testing/test_academic_api.md) - Tests de API (ViewSets, Serializers)
- [test_academic_import.md](testing/test_academic_import.md) - Tests de importación CSV

### Ejecutar Tests

```bash
cd backend
source ../venv/bin/activate

# Todos los tests
python manage.py test

# Tests específicos de una app
python manage.py test users
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

---

## 🤖 Scraper - Procesamiento de Recomendaciones

### Documentación
- [PREPARACION_SCRAPER_RECOMENDACIONES.md](scraper/PREPARACION_SCRAPER_RECOMENDACIONES.md) - Guía completa para desarrollo del scraper

### Estado
- ✅ **Fase 1 Completada**: Sistema preparado para absorber recomendaciones
  - Modelo actualizado con 10 campos estructurados
  - Importación de CSV funcional con 1751 comisiones reales
  - Campo `recomendacion_raw` para texto original
  - Campos estructurados listos para scraper:
    * `tipo_catedra` (recomendable/no_recomendable/exigente/para_aprender/accesible)
    * `toma_asistencia` (Boolean)
    * `tipo_parciales` (CharField)
    * `toma_trabajos_practicos` (Boolean)
    * `nivel_aprobados` (alto/medio/bajo)
    * `llegada_docente` (buena/mala/regular)
    * `bibliografia_info` (TextField)
    * `recomendacion_procesada` (Boolean)

- 🎯 **Próxima Fase**: Desarrollo del scraper NLP
  - Crear command `process_recomendaciones.py`
  - Implementar extracción con regex/NLP
  - Procesar 1751 recomendaciones
  - Marcar como procesadas

---

## 🔄 Hoja de Ruta del Backend

### ✅ Fase 1: App Users (COMPLETADA)
- Sistema de roles (estudiante, colaborador, moderador, admin)
- Gamificación (puntos, contribuciones aprobadas)
- API completa con permisos granulares
- 35+ tests de funcionalidad y seguridad

### ✅ Fase 2: App Academic (COMPLETADA)
- Modelos Docente y Comision refinados
- Importación CSV robusta (1751 comisiones)
- Búsqueda fuzzy de docentes
- Serializers anidados funcionales
- Tests completos de modelos y API
- Sistema preparado para recomendaciones

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

## 📊 Convenciones de Documentación

### Nombres de Archivos
- `README.md` - Documento principal de cada carpeta
- `PROBLEMA_*.md` - Descripción de problemas identificados
- `SOLUCION_*.md` - Soluciones implementadas
- `test_*.md` - Documentación de tests específicos
- `ESTRUCTURA_*.md` - Documentación de arquitectura

### Formato de Documentos
- Markdown con sintaxis GitHub-flavored
- Código con syntax highlighting (```python, ```bash)
- Emojis para mejor navegación visual
- Secciones claramente delimitadas
- Ejemplos prácticos con comandos ejecutables

### Actualización
- Documentar cambios significativos en tiempo real
- Mantener historial de problemas y soluciones
- Incluir ejemplos de uso actualizados
- Referencias cruzadas entre documentos relacionados

---

## 🚀 Acceso Rápido

### Empezar a Trabajar
1. [Instalar dependencias](../README.md#-configuración-y-tecnologías)
2. [Ejecutar migraciones](../README.md#iniciar-entorno-local)
3. [Ejecutar tests](testing/README.md)
4. [Importar datos](academic/README_IMPORTACION.md)

### Guías de Desarrollo
- **Nuevo desarrollador**: Leer README.md principal → testing/README.md → academic/README_IMPORTACION.md
- **Trabajar en Academic**: Revisar academic/ → testing/test_academic_*.md
- **Trabajar en Scraper**: Leer scraper/PREPARACION_SCRAPER_RECOMENDACIONES.md
- **Debugging**: Revisar PROBLEMA_*.md y SOLUCION_*.md correspondientes

---

## 📝 Notas de Mantenimiento

### Última Actualización
- **Fecha**: Enero 2026
- **Versión**: Backend v2.0 (Fase 2 completada)
- **Cambios**:
  - ✅ Reorganización completa de documentación
  - ✅ Eliminación de archivos compilados (.pyc, __pycache__)
  - ✅ Estructura de carpetas más clara (academic/, testing/, scraper/)
  - ✅ Índice maestro creado
  - ✅ Sistema de importación completado y testeado

### Próximos Pasos de Documentación
- [ ] Documentar API de Recommendations
- [ ] Guía de desarrollo del scraper NLP
- [ ] Documentación de deployment
- [ ] Guía de contribución para colaboradores

---

**Para más información sobre el proyecto completo, ver [README.md principal](../../README.md)**
