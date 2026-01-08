# Tests de Gestión de Roles

## 📝 Descripción

Esta suite verifica el sistema de asignación de roles y sus permisos asociados.

## 🧪 Clase de Test

**Archivo**: `backend/tests/test_users.py`  
**Clase**: `UserRoleManagementAPITest`  
**Total de tests**: 4

## 🚀 Ejecutar Tests

```bash
python manage.py test tests.test_users.UserRoleManagementAPITest --verbosity=2
```

## 📋 Tests Incluidos

### 1. `test_assign_role_as_admin`

**Qué testea**: Un admin puede asignar roles a otros usuarios

**Código para probar**:

```bash
# 1. Login como admin
ADMIN_TOKEN=$(curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "adminpass123"}' \
  | jq -r '.token')

# 2. Asignar rol 'colaborador' al usuario con ID 1
curl -X POST http://localhost:8000/api/users/1/assign_role/ \
  -H "Authorization: Token $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rol": "colaborador"}'
```

**Resultado esperado**:

```json
{
    "status": "Rol actualizado a colaborador"
}
```

**Status Code**: `200 OK`

**Validación**:

```bash
# Verificar que el rol cambió
curl -X GET http://localhost:8000/api/users/1/ \
  -H "Authorization: Token $ADMIN_TOKEN"

# Resultado esperado:
# {
#     "id": 1,
#     "username": "estudiante1",
#     "rol": "colaborador",  ← Cambió de 'estudiante' a 'colaborador'
#     ...
# }
```

---

### 2. `test_assign_role_as_student`

**Qué testea**: Un estudiante NO puede asignar roles

**Código para probar**:

```bash
# 1. Login como estudiante
STUDENT_TOKEN=$(curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "estudiante1", "password": "pass123"}' \
  | jq -r '.token')

# 2. Intentar asignar rol 'admin' a sí mismo
curl -X POST http://localhost:8000/api/users/1/assign_role/ \
  -H "Authorization: Token $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rol": "admin"}'
```

**Resultado esperado**:

```json
{
    "detail": "You do not have permission to perform this action."
}
```

**Status Code**: `403 FORBIDDEN`

**Importancia**: Este test detectó un **bug crítico de seguridad** donde estudiantes podían auto-asignarse el rol admin. El bug fue corregido.

---

### 3. `test_assign_invalid_role`

**Qué testea**: No se puede asignar un rol que no existe

**Código para probar**:

```bash
curl -X POST http://localhost:8000/api/users/1/assign_role/ \
  -H "Authorization: Token $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rol": "superuser"}'
```

**Resultado esperado**:

```json
{
    "error": "Rol inválido. Opciones: ['estudiante', 'colaborador', 'moderador', 'admin']"
}
```

**Status Code**: `400 BAD REQUEST`

---

### 4. `test_assign_all_valid_roles`

**Qué testea**: Se pueden asignar todos los roles válidos

**Roles válidos**:

- `estudiante`
- `colaborador`
- `moderador`
- `admin`

**Código para probar**:

```bash
# Asignar cada rol secuencialmente
for rol in estudiante colaborador moderador admin; do
  echo "Asignando rol: $rol"
  curl -X POST http://localhost:8000/api/users/1/assign_role/ \
    -H "Authorization: Token $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"rol\": \"$rol\"}"
  echo ""
done
```

**Resultado esperado**: Cada asignación retorna `200 OK` con mensaje de confirmación.

---

## 🔐 Matriz de Permisos por Rol

| Acción | Estudiante | Colaborador | Moderador | Admin |
|--------|------------|-------------|-----------|-------|
| Ver su perfil (`/me/`) | ✅ | ✅ | ✅ | ✅ |
| Ver otros usuarios | ✅ | ✅ | ✅ | ✅ |
| Listar todos los usuarios | ❌ | ❌ | ❌ | ✅ |
| Actualizar usuarios | ❌ | ❌ | ❌ | ✅ |
| Eliminar usuarios | ❌ | ❌ | ❌ | ✅ |
| Asignar roles | ❌ | ❌ | ❌ | ✅ |
| Scrapear datos | ❌ | ✅* | ✅* | ✅* |
| Moderar recomendaciones | ❌ | ❌ | ✅ | ✅ |

*Requiere además `puede_scrapear = True`

---

## 🎬 Escenario Completo: Promoción de Usuario

```bash
# Escenario: Un estudiante activo es promovido a colaborador

# 1. Admin se autentica
ADMIN_TOKEN=$(curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "adminpass123"}' \
  | jq -r '.token')

# 2. Ver usuario actual
curl -X GET http://localhost:8000/api/users/5/ \
  -H "Authorization: Token $ADMIN_TOKEN"

# Resultado:
# {
#     "id": 5,
#     "username": "juan_perez",
#     "rol": "estudiante",
#     "puntos": 150,  ← Usuario activo con muchos puntos
#     "contribuciones_aprobadas": 15
# }

# 3. Promover a colaborador
curl -X POST http://localhost:8000/api/users/5/assign_role/ \
  -H "Authorization: Token $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rol": "colaborador"}'

# Resultado:
# {
#     "status": "Rol actualizado a colaborador"
# }

# 4. Habilitar scraping (opcional, vía admin panel o API)
# user.puede_scrapear = True

# 5. Verificar cambios
curl -X GET http://localhost:8000/api/users/5/ \
  -H "Authorization: Token $ADMIN_TOKEN"

# Resultado:
# {
#     "id": 5,
#     "username": "juan_perez",
#     "rol": "colaborador",  ← Rol actualizado
#     "puntos": 150,
#     "contribuciones_aprobadas": 15
# }
```

---

## ✅ Ejecutar Toda la Suite

```bash
python manage.py test tests.test_users.UserRoleManagementAPITest --verbosity=2
```

**Resultado esperado**:

```
test_assign_all_valid_roles ... ok
test_assign_invalid_role ... ok
test_assign_role_as_admin ... ok
test_assign_role_as_student ... [WARNING] Forbidden: /api/users/1/assign_role/
ok

----------------------------------------------------------------------
Ran 4 tests in 0.XXXs

OK
```

**Nota**: El warning "Forbidden" en `test_assign_role_as_student` es esperado y correcto - indica que el sistema rechazó correctamente el intento.

## 🎯 Cobertura

- ✅ Asignación de roles por admin
- ✅ Prevención de asignación por no-admin
- ✅ Validación de roles válidos
- ✅ Todos los roles se pueden asignar
- ✅ Seguridad contra escalación de privilegios
