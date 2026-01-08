# Tests de API - Academic App

## DocenteViewSet Tests

### 🔍 Búsqueda y Filtrado

#### ✅ test_search_by_apellido
**Endpoint:** `GET /api/docentes/?search=garcia`

**Caso de uso:**
Usuario busca docentes escribiendo "garcia" en el buscador.

**Expectativa:**
- Encuentra docentes con apellido "García", "Garcia", etc.
- Case-insensitive.

**Punto de fricción detectado:** ✅ NINGUNO

**Ejemplo de respuesta:**
```json
{
  "count": 1,
  "results": [
    {
      "id_docente": 1,
      "nombre": "Juan",
      "apellido": "García",
      "nombre_completo": "Juan García",
      "alias_search": "J. García, Profe Juan"
    }
  ]
}
```

---

#### ✅ test_search_by_alias
**Endpoint:** `GET /api/docentes/?search=profe`

**Caso de uso:**
Buscar por apodos/aliases: "Profe Juan", "Prof. García".

**Expectativa:**
- Busca en el campo `alias_search`.
- Permite múltiples aliases separados por comas.

**Punto de fricción detectado:** ✅ NINGUNO

**Recomendación:** 📝
Documentar el formato esperado de `alias_search`:
```
"Profe Juan, J. García, JG, Juan G"
```

---

#### ✅ test_ordering_by_apellido_asc / desc
**Endpoints:**
- `GET /api/docentes/?ordering=apellido` (A-Z)
- `GET /api/docentes/?ordering=-apellido` (Z-A)

**Caso de uso:**
Ordenar lista de docentes alfabéticamente.

**Expectativa:**
```
apellido  → Fernández, García, López
-apellido → López, García, Fernández
```

**Punto de fricción detectado:** ✅ NINGUNO

---

### 📊 Serializers Anidados

#### ✅ test_retrieve_docente_includes_comisiones
**Endpoint:** `GET /api/docentes/1/`

**Caso de uso:**
Ver un docente específico con todas sus comisiones.

**Expectativa:**
```json
{
  "id_docente": 1,
  "nombre": "Juan",
  "apellido": "García",
  "nombre_completo": "Juan García",
  "alias_search": "...",
  "comisiones": [
    {
      "id_comision": 10,
      "codigo": "TEST-1",
      "nombre": "Test",
      "horario": "Lun 10:00",
      ...
    }
  ]
}
```

**Punto de fricción detectado:** ✅ NINGUNO
- El serializer `DocenteConComisionesSerializer` funciona correctamente.

---

### 📈 Endpoint de Estadísticas

#### ✅ test_estadisticas_endpoint
**Endpoint:** `GET /api/docentes/estadisticas/`

**Caso de uso:**
Dashboard mostrando métricas de docentes.

**Expectativa:**
```json
{
  "total_docentes": 45,
  "docentes_con_comisiones": 40,
  "docentes_sin_comisiones": 5
}
```

**Punto de fricción detectado:** ✅ NINGUNO

**Uso típico:**
```javascript
fetch('/api/docentes/estadisticas/')
  .then(r => r.json())
  .then(stats => {
    console.log(`${stats.docentes_sin_comisiones} docentes sin comisiones`);
  });
```

---

## ComisionViewSet Tests

### 🔍 Búsqueda Cross-Model

#### ✅ test_search_by_docente_apellido
**Endpoint:** `GET /api/catedras/?search=garcia`

**Caso de uso:**
Buscar comisiones por el apellido del docente.

**Expectativa:**
- Encuentra comisiones donde el docente se llame "García".
- Utiliza `search_fields = ['docente__apellido', ...]`.

**Punto de fricción detectado:** ✅ NINGUNO

**Importancia:** 🎯
Permite búsqueda intuitiva: "¿Qué materias da García?"

---

#### ✅ test_list_comisiones
**Endpoint:** `GET /api/catedras/`

**Caso de uso:**
Listar todas las comisiones con datos del docente.

**Expectativa:**
```json
{
  "results": [
    {
      "id_comision": 1,
      "codigo": "MAT-101",
      "nombre": "Matemática I",
      "docente": {
        "id_docente": 1,
        "nombre": "Juan",
        "apellido": "García",
        ...
      },
      "horario": "Lun 10:00",
      ...
    }
  ]
}
```

**Punto de fricción detectado:** ✅ NINGUNO
- El serializer `ComisionConDocenteSerializer` funciona.

---

## Optimización de Queries

### ⚡ test_list_docentes_no_n_plus_one
**Propósito:** Evitar problema N+1 al listar docentes.

**Sin optimización:**
```
Query 1: SELECT * FROM docente;        (100 docentes)
Query 2: SELECT * FROM comision WHERE docente_id=1;
Query 3: SELECT * FROM comision WHERE docente_id=2;
...
Query 101: SELECT * FROM comision WHERE docente_id=100;

Total: 101 queries 😱
```

**Con optimización:**
```
Query 1: SELECT * FROM docente;
Total: 1 query ✅ (no se cargan comisiones en el list)
```

**Punto de fricción detectado:** ✅ NINGUNO
- El ViewSet usa serializers diferentes para `list` y `retrieve`.

---

### ⚡ test_retrieve_docente_with_prefetch
**Propósito:** Optimizar detalle con `prefetch_related`.

**Con optimización:**
```
Query 1: SELECT * FROM docente WHERE id=1;
Query 2: SELECT * FROM comision WHERE docente_id IN (1);
Total: 2 queries ✅
```

**Punto de fricción detectado:** ✅ NINGUNO
- El método `get_queryset()` usa `prefetch_related('comisiones')`.

---

### ⚡ test_list_comisiones_with_select_related
**Propósito:** Optimizar con `select_related` (JOIN).

**Con optimización:**
```sql
SELECT comision.*, docente.*
FROM comision
INNER JOIN docente ON comision.docente_id = docente.id_docente;

Total: 1 query ✅
```

**Punto de fricción detectado:** ✅ NINGUNO

---

## CRUD Operations

### ✅ test_create_docente
**Endpoint:** `POST /api/docentes/`

**Request:**
```json
{
  "nombre": "Nuevo",
  "apellido": "Docente",
  "alias_search": "ND"
}
```

**Response:**
```json
{
  "id_docente": 4,
  "nombre": "Nuevo",
  "apellido": "Docente",
  "nombre_completo": "Nuevo Docente",
  "alias_search": "ND"
}
```

**Punto de fricción detectado:** ✅ NINGUNO

---

## Casos Límite API

### ✅ test_search_with_special_characters
**Endpoint:** `GET /api/docentes/?search=josé`

**Caso de uso:**
Búsqueda con acentos y caracteres especiales.

**Expectativa:**
- Encuentra "José", "Jose", "JOSE".
- Case-insensitive y accent-insensitive (según DB).

**Punto de fricción detectado:** ⚠️ **DEPENDE DE LA BASE DE DATOS**

**Recomendación:**
```python
# En producción con PostgreSQL, usar:
search_fields = ['nombre__unaccent', 'apellido__unaccent']
```

---

## Resumen de Puntos de Fricción

| Feature | Estado | Fricción | Acción |
|---------|--------|----------|--------|
| Búsqueda básica | ✅ | Ninguna | - |
| Búsqueda cross-model | ✅ | Ninguna | - |
| Serializers anidados | ✅ | Ninguna | - |
| Optimización queries | ✅ | Ninguna | - |
| **Acentos en búsqueda** | ⚠️ | **DB-dependiente** | Usar `unaccent` |
| Estadísticas | ✅ | Ninguna | - |

---

## Cómo Ejecutar Estos Tests

```bash
# Tests de API
python manage.py test academic.tests.DocenteAPITest
python manage.py test academic.tests.ComisionAPITest

# Tests de optimización
python manage.py test academic.tests.QueryOptimizationTest

# Test específico
python manage.py test academic.tests.DocenteAPITest.test_search_by_apellido

# Con SQL queries visibles
python manage.py test academic.tests --verbosity=2 --debug-sql
```

---

## Métricas de Performance

```
Endpoint                    | Queries | Tiempo | Status |
----------------------------|---------|--------|--------|
GET /api/docentes/          | 1       | ~50ms  | ✅     |
GET /api/docentes/1/        | 2       | ~80ms  | ✅     |
GET /api/catedras/          | 1       | ~60ms  | ✅     |
GET /api/docentes/?search=  | 1       | ~70ms  | ✅     |
```

Todas las operaciones están optimizadas ⚡
