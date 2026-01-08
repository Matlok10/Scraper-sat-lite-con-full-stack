# Documentación de Tests - Backend

Esta carpeta contiene documentación detallada de todas las suites de tests del proyecto.

## 📁 Estructura

```
tests/docs/
├── README.md                    (este archivo)
├── test_users_model.md          Documentación de tests del modelo User
├── test_users_auth.md           Documentación de tests de autenticación
├── test_users_viewset.md        Documentación de tests del UserViewSet
├── test_users_roles.md          Documentación de tests de roles y permisos
└── test_users_serializer.md     Documentación de tests del serializer
```

## 🧪 Ejecutar Tests

### Todos los tests

```bash
cd backend
source ../venv/bin/activate
python manage.py test
```

### Tests específicos de Users

```bash
# Suite completa de users
python manage.py test tests.test_users --verbosity=2

# Tests originales en la app
python manage.py test users.tests --verbosity=2

# Una clase específica
python manage.py test tests.test_users.UserModelTest --verbosity=2

# Un test individual
python manage.py test tests.test_users.UserModelTest.test_create_user_with_default_role --verbosity=2
```

### Script automatizado

```bash
./run_tests.sh
```

## 📊 Cobertura de Tests

### Users App (35+ tests)

- ✅ **UserModelTest** (7 tests) - Modelo, roles, gamificación
- ✅ **UserAuthenticationAPITest** (6 tests) - Login, logout, tokens
- ✅ **UserViewSetAPITest** (9 tests) - CRUD, permisos
- ✅ **UserRoleManagementAPITest** (4 tests) - Asignación de roles
- ✅ **UserSerializerTest** (2 tests) - Serialización
- ✅ **UserTests** (5 tests) - Tests originales de la app

### Academic App

- ✅ **AcademicModelTest** - Docente, Comision

### Recommendations App

- ✅ **RecomendacionModelTest** - Modelo de recomendaciones

### API Tests

- ✅ **ComisionAPITest** - Endpoints de comisiones

## 🎯 Guías de Tests por Funcionalidad

Cada archivo de documentación incluye:

- Descripción de qué se está testeando
- Código de ejemplo para ejecutar
- Resultados esperados
- Casos de uso y escenarios

Consulta los archivos individuales para detalles específicos de cada suite de tests.
