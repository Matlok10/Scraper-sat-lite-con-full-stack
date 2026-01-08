# Actualización del README - Fase 1 Completada

## Sección a Agregar al README.md

Agrega esta sección después de la descripción de la app Users:

```markdown
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

## 🔄 Plan de Refinamiento Backend (En Progreso)

El backend está siendo refinado sistemáticamente app por app para asegurar robustez antes de la integración frontend.

### Fase 1: App Users ✅ COMPLETADA
- ✅ Sistema de roles (estudiante, colaborador, moderador, admin)
- ✅ Gamificación (puntos, contribuciones aprobadas)
- ✅ API completa con permisos granulares
- ✅ 35+ tests de funcionalidad y seguridad
- ✅ Bug crítico de permisos detectado y corregido

### Fase 2: App Academic 🔄 PRÓXIMA
- [ ] Implementar `DocenteViewSet` con búsqueda
- [ ] Búsqueda difusa de docentes (fuzzy matching)
- [ ] Serializers anidados (docente en comisión)
- [ ] Cálculo de `promedio_sentimiento` por comisión
- [ ] Tests de búsqueda y filtros

### Fase 3: App Recommendations 🎯 CRÍTICA
- [ ] Crear `serializers.py` y `views.py` completos
- [ ] Implementar NLP Processor para análisis de sentimiento
- [ ] Sistema de votación comunitaria
- [ ] Endpoint de recomendaciones con filtros
- [ ] Tests de NLP y votación

### Fase 4: App Scraping 📋 PENDIENTE
- [ ] Validar permisos de scraping por rol
- [ ] Limitar sesiones concurrentes por usuario
- [ ] Preparar integración con extensión Chrome

---

## 🧪 Testing

El proyecto cuenta con una suite completa de tests automatizados.

### Ejecutar Tests

\`\`\`bash
cd backend
source ../venv/bin/activate

# Todos los tests
python manage.py test

# Tests de una app específica
python manage.py test users
python manage.py test tests.test_users

# Con más detalle
python manage.py test --verbosity=2

# Script completo
./run_tests.sh
\`\`\`

### Cobertura Actual

- **Users App**: 35+ tests (modelos, autenticación, permisos, roles)
- **Academic App**: Tests de modelos (Docente, Comision)
- **Recommendations App**: Tests de modelos
- **API Tests**: Tests de endpoints principales

📚 **Documentación de Tests**: Ver `backend/tests/docs/` para guías detalladas de cada suite de tests con ejemplos de curl y resultados esperados.
```

## Endpoints Actualizados para la Tabla de API

Agrega estos endpoints a la tabla de API Reference:

```markdown
| `/api/auth/login/` | POST | Autenticación y obtención de token |
| `/api/auth/logout/` | POST | Cerrar sesión e invalidar token |
| `/api/users/` | GET | Listar usuarios (solo admin) |
| `/api/users/me/` | GET | Ver perfil del usuario actual |
| `/api/users/{id}/assign_role/` | POST | Asignar rol a usuario (solo admin) |
```
