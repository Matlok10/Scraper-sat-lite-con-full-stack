# Tests de Autenticación (Login/Logout)

## 📝 Descripción

Esta suite verifica el sistema de autenticación basado en tokens, incluyendo login, logout y gestión de tokens.

## 🧪 Clase de Test

**Archivo**: `backend/tests/test_users.py`  
**Clase**: `UserAuthenticationAPITest`  
**Total de tests**: 6

## 🚀 Ejecutar Tests

```bash
python manage.py test tests.test_users.UserAuthenticationAPITest --verbosity=2
```

## 📋 Tests Incluidos

### 1. `test_login_success`

**Qué testea**: Login exitoso retorna token y datos del usuario

**Código para probar**:

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

**Resultado esperado**:

```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "rol": "estudiante"
}
```

**Status Code**: `200 OK`

---

### 2. `test_login_invalid_credentials`

**Qué testea**: Login con credenciales incorrectas falla

**Código para probar**:

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "wrongpassword"}'
```

**Resultado esperado**:

```json
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}
```

**Status Code**: `400 BAD REQUEST`

---

### 3. `test_login_creates_token`

**Qué testea**: Login crea un token en la base de datos

**Validaciones**:

- ✅ Se crea un nuevo token
- ✅ El token se asocia al usuario correcto
- ✅ El token retornado coincide con el almacenado

---

### 4. `test_logout_success`

**Qué testea**: Logout elimina el token del usuario

**Código para probar**:

```bash
# Primero hacer login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}' \
  | jq -r '.token')

# Luego hacer logout
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Token $TOKEN"
```

**Resultado esperado**:

- **Status Code**: `204 NO CONTENT`
- **Body**: Vacío
- **Efecto**: El token es eliminado de la base de datos

**Verificación**:

```bash
# Intentar usar el token después del logout
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Token $TOKEN"

# Resultado esperado: 401 UNAUTHORIZED
```

---

### 5. `test_logout_requires_authentication`

**Qué testea**: Logout sin autenticación falla

**Código para probar**:

```bash
curl -X POST http://localhost:8000/api/auth/logout/
```

**Resultado esperado**:

```json
{
    "detail": "Authentication credentials were not provided."
}
```

**Status Code**: `401 UNAUTHORIZED`

---

## 🔐 Flujo Completo de Autenticación

### Escenario: Usuario se autentica y accede a recursos

```bash
# 1. Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "estudiante1", "password": "pass123"}' \
  | jq -r '.token')

echo "Token obtenido: $TOKEN"

# 2. Acceder a recurso protegido
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Token $TOKEN"

# Resultado esperado:
# {
#     "id": 1,
#     "username": "estudiante1",
#     "email": "estudiante@example.com",
#     "rol": "estudiante",
#     "puntos": 0,
#     ...
# }

# 3. Logout
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Token $TOKEN"

# 4. Intentar acceder de nuevo (debe fallar)
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Token $TOKEN"

# Resultado esperado: 401 UNAUTHORIZED
```

---

## ✅ Ejecutar Toda la Suite

```bash
python manage.py test tests.test_users.UserAuthenticationAPITest --verbosity=2
```

**Resultado esperado**:

```
test_login_creates_token ... ok
test_login_invalid_credentials ... ok
test_login_success ... ok
test_logout_requires_authentication ... ok
test_logout_success ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.XXXs

OK
```

## 🎯 Cobertura

- ✅ Login exitoso con credenciales válidas
- ✅ Login fallido con credenciales inválidas
- ✅ Creación de tokens
- ✅ Logout y eliminación de tokens
- ✅ Protección de endpoints sin autenticación
- ✅ Inclusión de rol en respuesta de login
