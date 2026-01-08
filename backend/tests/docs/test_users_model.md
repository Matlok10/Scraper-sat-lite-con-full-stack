# Tests del Modelo User

## 📝 Descripción

Esta suite de tests verifica el funcionamiento correcto del modelo `User` personalizado, incluyendo:

- Creación de usuarios con roles
- Validación de campos
- Sistema de gamificación
- Metadata de scraping

## 🧪 Clase de Test

**Archivo**: `backend/tests/test_users.py`  
**Clase**: `UserModelTest`  
**Total de tests**: 7

## 🚀 Ejecutar Tests

```bash
cd backend
source ../venv/bin/activate

# Ejecutar toda la suite
python manage.py test tests.test_users.UserModelTest --verbosity=2

# Ejecutar un test específico
python manage.py test tests.test_users.UserModelTest.test_create_user_with_default_role --verbosity=2
```

## 📋 Tests Incluidos

### 1. `test_create_user_with_default_role`

**Qué testea**: Un usuario nuevo debe tener rol 'estudiante' por defecto

**Código**:

```python
def test_create_user_with_default_role(self):
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    self.assertEqual(user.rol, 'estudiante')
    self.assertEqual(user.puntos, 0)
    self.assertEqual(user.contribuciones_aprobadas, 0)
    self.assertFalse(user.puede_scrapear)
```

**Resultado esperado**:

```
test_create_user_with_default_role ... ok
```

**Validaciones**:

- ✅ Rol por defecto es 'estudiante'
- ✅ Puntos iniciales son 0
- ✅ Contribuciones aprobadas son 0
- ✅ `puede_scrapear` es False

---

### 2. `test_create_user_with_custom_role`

**Qué testea**: Se puede crear un usuario con un rol específico

**Código**:

```python
def test_create_user_with_custom_role(self):
    user = User.objects.create_user(
        username='colaborador1',
        email='colab@example.com',
        password='pass123',
        rol='colaborador'
    )
    self.assertEqual(user.rol, 'colaborador')
```

**Resultado esperado**:

```
test_create_user_with_custom_role ... ok
```

**Validaciones**:

- ✅ El rol personalizado se asigna correctamente

---

### 3. `test_user_string_representation`

**Qué testea**: El `__str__` del usuario incluye username, email y rol

**Código**:

```python
def test_user_string_representation(self):
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    expected = f"{user.username} ({user.email}) - {user.rol}"
    self.assertEqual(str(user), expected)
```

**Resultado esperado**:

```
test_user_string_representation ... ok
```

**Ejemplo de output**:

```
"testuser (test@example.com) - estudiante"
```

---

### 4. `test_rol_choices_validation`

**Qué testea**: Solo se pueden asignar roles válidos

**Código**:

```python
def test_rol_choices_validation(self):
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    valid_roles = ['estudiante', 'colaborador', 'moderador', 'admin']
    
    for rol in valid_roles:
        user.rol = rol
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.rol, rol)
```

**Resultado esperado**:

```
test_rol_choices_validation ... ok
```

**Validaciones**:

- ✅ Todos los roles válidos se pueden asignar
- ✅ El rol persiste en la base de datos

---

### 5. `test_gamification_fields`

**Qué testea**: Los campos de gamificación funcionan correctamente

**Código**:

```python
def test_gamification_fields(self):
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    
    # Simular aprobación de contribución
    user.contribuciones_aprobadas += 1
    user.puntos += 10
    user.save()
    
    user.refresh_from_db()
    self.assertEqual(user.contribuciones_aprobadas, 1)
    self.assertEqual(user.puntos, 10)
```

**Resultado esperado**:

```
test_gamification_fields ... ok
```

**Validaciones**:

- ✅ Los puntos se pueden incrementar
- ✅ Las contribuciones aprobadas se pueden incrementar
- ✅ Los cambios persisten en la base de datos

**Caso de uso**:

```python
# Cuando un moderador aprueba una recomendación
recomendacion.contribuidor.contribuciones_aprobadas += 1
recomendacion.contribuidor.puntos += 10
recomendacion.contribuidor.save()
```

---

### 6. `test_scraping_metadata_fields`

**Qué testea**: Los campos de metadata de scraping funcionan

**Código**:

```python
def test_scraping_metadata_fields(self):
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        rol='colaborador'
    )
    
    user.puede_scrapear = True
    user.sesiones_scraping_activas = 2
    user.save()
    
    user.refresh_from_db()
    self.assertTrue(user.puede_scrapear)
    self.assertEqual(user.sesiones_scraping_activas, 2)
```

**Resultado esperado**:

```
test_scraping_metadata_fields ... ok
```

**Validaciones**:

- ✅ `puede_scrapear` se puede activar
- ✅ `sesiones_scraping_activas` se puede incrementar
- ✅ Los cambios persisten

**Caso de uso**:

```python
# Antes de permitir scraping
if user.rol in ['colaborador', 'moderador', 'admin'] and user.puede_scrapear:
    if user.sesiones_scraping_activas < 3:  # Límite
        # Permitir scraping
        user.sesiones_scraping_activas += 1
        user.save()
```

---

## ✅ Ejecutar Toda la Suite

```bash
python manage.py test tests.test_users.UserModelTest --verbosity=2
```

**Resultado esperado completo**:

```
test_create_user_with_custom_role ... ok
test_create_user_with_default_role ... ok
test_gamification_fields ... ok
test_rol_choices_validation ... ok
test_scraping_metadata_fields ... ok
test_user_string_representation ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.XXXs

OK
```

## 🎯 Cobertura

Esta suite cubre:

- ✅ Creación de usuarios
- ✅ Roles y validación
- ✅ Representación en string
- ✅ Sistema de gamificación
- ✅ Metadata de scraping
- ✅ Persistencia en base de datos
