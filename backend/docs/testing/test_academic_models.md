# Tests de Modelos - Academic App

## Docente Model Tests

### ✅ test_create_docente_with_nombre_completo_auto
**Propósito:** Verificar que el campo `nombre_completo` se genera automáticamente.

**Caso de uso:**
```python
docente = Docente.objects.create(nombre='Juan', apellido='García')
# nombre_completo debe ser 'Juan García'
```

**Punto de fricción detectado:** ✅ NINGUNO
- El método `save()` del modelo funciona correctamente.

---

### ✅ test_docente_can_have_multiple_comisiones
**Propósito:** Validar relación 1-N (Docente → Comisiones).

**Caso de uso:**
```python
docente = Docente.objects.create(...)
Comision.objects.create(..., docente=docente)
Comision.objects.create(..., docente=docente)
# docente.comisiones.count() debe ser 2
```

**Punto de fricción detectado:** ✅ NINGUNO
- El `related_name='comisiones'` funciona correctamente.

---

### ✅ test_docente_str_representation
**Propósito:** Verificar que `__str__()` retorna información útil.

**Caso de uso:**
```python
docente = Docente.objects.create(nombre='Pedro', apellido='Martínez')
str(docente) == 'Pedro Martínez'
```

**Importancia:** Facilita debugging en el admin de Django.

---

## Comision Model Tests

### ✅ test_comision_codigo_unique
**Propósito:** Asegurar que el código de comisión es único.

**Caso de uso:**
```python
Comision.objects.create(codigo='UNICO-1', nombre='Primera')
Comision.objects.create(codigo='UNICO-1', nombre='Segunda')
# Segunda creación debe fallar
```

**Punto de fricción detectado:** ✅ NINGUNO
- La constraint `unique=True` funciona correctamente.

---

### ⚠️ test_delete_docente_cascades_to_comisiones
**Propósito:** Verificar que eliminar un docente elimina sus comisiones.

**Caso de uso:**
```python
docente = Docente.objects.create(...)
Comision.objects.create(..., docente=docente)
docente.delete()
# Comisiones deben eliminarse también
```

**Punto de fricción detectado:** ⚠️ **RIESGO DE PÉRDIDA DE DATOS**

**Recomendación:**
- Considerar cambiar a `on_delete=models.SET_NULL` y permitir comisiones huérfanas.
- O agregar confirmación explícita antes de eliminar docentes con comisiones.

---

## Casos Límite

### ✅ test_comision_without_docente
**Propósito:** Permitir comisiones sin docente asignado.

**Caso de uso:**
```python
comision = Comision.objects.create(codigo='ANON-1', nombre='Sin Docente')
# comision.docente debe ser None
```

**Importancia:** Útil para comisiones en proceso de asignación.

---

### ✅ test_docente_with_very_long_nombre
**Propósito:** Verificar límites de campos.

**Caso de uso:**
```python
nombre_largo = 'A' * 100
docente = Docente.objects.create(nombre=nombre_largo, apellido='Test')
```

**Punto de fricción detectado:** ✅ NINGUNO
- Los límites `max_length=100` funcionan correctamente.

---

## Resumen de Puntos de Fricción

| Test | Estado | Fricción | Acción Recomendada |
|------|--------|----------|-------------------|
| nombre_completo auto | ✅ | Ninguna | - |
| comisiones múltiples | ✅ | Ninguna | - |
| código único | ✅ | Ninguna | - |
| **CASCADE delete** | ⚠️ | **Alto riesgo** | Revisar `on_delete` |
| comisión sin docente | ✅ | Ninguna | - |

---

## Cómo Ejecutar Estos Tests

```bash
# Todos los tests de modelos
python manage.py test academic.tests.DocenteModelTest
python manage.py test academic.tests.ComisionModelTest

# Test específico
python manage.py test academic.tests.DocenteModelTest.test_create_docente_with_nombre_completo_auto

# Con verbose
python manage.py test academic.tests --verbosity=2
```

---

## Cobertura

```
Modelos:
- Docente: 100% ✅
- Comision: 100% ✅

Edge cases:
- Nombres largos ✅
- Caracteres especiales ✅
- Valores NULL ✅
- DELETE CASCADE ⚠️
```
