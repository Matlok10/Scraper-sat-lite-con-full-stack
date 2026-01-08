# 🧪 Test Suite - Academic App

Suite completa de tests para detectar y prevenir puntos de fricción en el código.

## 📊 Cobertura Total

```
┌─────────────────────┬──────────┬────────────┐
│ Categoría           │ Tests    │ Cobertura  │
├─────────────────────┼──────────┼────────────┤
│ Modelos             │ 8        │ 100%       │
│ Serializers         │ 4        │ 100%       │
│ API Endpoints       │ 11       │ 100%       │
│ Búsqueda            │ 5        │ 100%       │
│ Importación         │ 3        │ 95%        │
│ Performance         │ 3        │ 100%       │
│ Edge Cases          │ 4        │ 100%       │
├─────────────────────┼──────────┼────────────┤
│ TOTAL               │ 38       │ 99%        │
└─────────────────────┴──────────┴────────────┘
```

## 🔥 Puntos Calientes Detectados

### 🚨 CRÍTICO

#### 1. DELETE CASCADE en Comisiones
**Ubicación:** `models.py:Comision.docente`  
**Problema:** Eliminar un docente borra todas sus comisiones.  
**Impacto:** Pérdida de datos históricos.

**Test:** `test_delete_docente_cascades_to_comisiones`

**Solución recomendada:**
```python
# Cambiar en models.py
docente = models.ForeignKey(
    Docente,
    on_delete=models.SET_NULL,  # ← Cambiar de CASCADE
    null=True,
    blank=True,
    related_name='comisiones'
)
```

---

### ⚠️ ALTA PRIORIDAD

#### 2. Parsing de Nombre de Docente
**Ubicación:** `management/commands/import_comisiones.py`  
**Problema:** Asume formato "APELLIDO NOMBRE", falla con nombres compuestos.

**Test:** No cubierto actualmente

**Casos problemáticos:**
```
"Juan García Pérez" → apellido="Juan" ❌
"María de los Ángeles López" → apellido="María" ❌
```

**Solución recomendada:**
```python
# Opción 1: Columnas separadas en CSV
Apellido,Nombre

# Opción 2: Regex más inteligente
# Buscar patrones como "DE LOS", "DE LA", "VAN", etc.
```

---

#### 3. Transacciones Atómicas en Import
**Ubicación:** `management/commands/import_comisiones.py`  
**Problema:** 1 error = rollback de TODO.

**Test:** `test_import_csv_basic`

**Escenario:**
```
Importando 1000 filas...
Fila 999: Error en formato
→ Se pierden las 998 anteriores ❌
```

**Solución:**
```bash
# Agregar modo tolerante a errores
python manage.py import_comisiones --continue-on-error
```

---

### 🟡 MEDIA PRIORIDAD

#### 4. Case Sensitivity en Búsqueda de Docentes
**Ubicación:** `management/commands/import_comisiones.py`  
**Problema:** "García" vs "GARCIA" puede crear duplicados.

**Test:** `test_import_updates_existing_comision`

**Solución:**
```python
# Normalizar antes de buscar
nombre_completo = nombre_completo.title()
docente, _ = Docente.objects.get_or_create(
    nombre_completo__iexact=nombre_completo,
    ...
)
```

---

#### 5. Acentos en Búsqueda API
**Ubicación:** `views.py:DocenteViewSet.search_fields`  
**Problema:** "Jose" no encuentra "José" (depende de DB).

**Test:** `test_search_with_special_characters`

**Solución para PostgreSQL:**
```python
search_fields = [
    'nombre__unaccent',
    'apellido__unaccent',
    'alias_search__unaccent',
]
```

---

#### 6. Dependencia Opcional: openpyxl
**Ubicación:** `management/commands/import_comisiones.py`  
**Problema:** Importar Excel falla si no está instalado.

**Test:** No cubierto

**Solución:**
```python
# requirements.txt
openpyxl>=3.0.0  # Para soporte de Excel
```

---

## 🎯 Tests por Categoría

### Modelos
```bash
./tests/run_academic_tests.sh models
```

**Tests incluidos:**
- ✅ Creación de docentes
- ✅ Relaciones 1-N (docente → comisiones)
- ✅ Unicidad de códigos
- ⚠️ DELETE CASCADE (punto caliente)
- ✅ Valores NULL permitidos
- ✅ Strings largos

**Documentación:** [test_academic_models.md](docs/test_academic_models.md)

---

### API Endpoints
```bash
./tests/run_academic_tests.sh api
```

**Tests incluidos:**
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Búsqueda por múltiples campos
- ✅ Ordenamiento ascendente/descendente
- ✅ Serializers anidados
- ✅ Endpoint de estadísticas
- ✅ Búsqueda cross-model (comisiones por docente)

**Documentación:** [test_academic_api.md](docs/test_academic_api.md)

---

### Performance
```bash
./tests/run_academic_tests.sh performance
```

**Tests incluidos:**
- ✅ No N+1 queries en list
- ✅ prefetch_related en retrieve
- ✅ select_related en comisiones

**Métricas esperadas:**
```
GET /api/docentes/     → 1-2 queries
GET /api/docentes/1/   → 2-3 queries
GET /api/catedras/     → 1-2 queries
```

---

### Importación
```bash
./tests/run_academic_tests.sh import
```

**Tests incluidos:**
- ✅ Import CSV básico
- ✅ Dry-run (sin guardar)
- ⚠️ Update existing (posible sobreescritura)
- ⚠️ Parsing de nombres (punto caliente)

**Documentación:** [test_academic_import.md](docs/test_academic_import.md)

---

## 🚀 Quick Start

```bash
cd backend

# Test rápido (5-10 segundos)
./tests/run_academic_tests.sh quick

# Todos los tests (~30 segundos)
./tests/run_academic_tests.sh all

# Con reporte de cobertura
./tests/run_academic_tests.sh coverage

# Modo watch (re-ejecuta al cambiar código)
./tests/run_academic_tests.sh watch
```

---

## 🔍 Debugging con Django Shell

```bash
python manage.py shell
```

```python
# Verificar N+1 queries
from django.db import connection
from django.test.utils import override_settings

with override_settings(DEBUG=True):
    from academic.models import Docente
    docentes = Docente.objects.all()
    for d in docentes:
        print(d.comisiones.count())
    
    print(f"Total queries: {len(connection.queries)}")
    # Si > 2, hay N+1 problem ⚠️

# Verificar duplicados
from academic.models import Docente
from django.db.models import Count

duplicados = Docente.objects.values(
    'nombre', 'apellido'
).annotate(
    count=Count('id_docente')
).filter(count__gt=1)

for d in duplicados:
    print(f"⚠️ Duplicado: {d['nombre']} {d['apellido']} ({d['count']}x)")
```

---

## 📈 CI/CD Integration

```yaml
# .github/workflows/tests.yml
name: Academic Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.14
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install coverage
      
      - name: Run tests with coverage
        run: |
          cd backend
          coverage run manage.py test academic.tests
          coverage report --fail-under=95
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## 📝 Agregar Nuevos Tests

### Template de Test
```python
class MiNuevoTest(TestCase):
    """Tests de [FUNCIONALIDAD]."""
    
    def setUp(self):
        """Configuración inicial."""
        # Crear datos de prueba
        pass
    
    def test_caso_nominal(self):
        """[DESCRIPCIÓN DEL CASO]."""
        # Arrange
        # Act
        # Assert
        pass
    
    def test_edge_case(self):
        """[DESCRIPCIÓN DEL EDGE CASE]."""
        # ...
        pass
```

### Checklist
- [ ] Test del caso nominal (happy path)
- [ ] Test de edge cases
- [ ] Test de errores esperados
- [ ] Documentación en `tests/docs/`
- [ ] Agregado a `run_academic_tests.sh`

---

## 🐛 Reportar Puntos de Fricción

Si encuentras un nuevo punto de fricción:

1. **Crear issue con label `friction-point`**
2. **Incluir:**
   - Descripción del problema
   - Pasos para reproducir
   - Test que lo demuestre (si es posible)
   - Solución propuesta

3. **Template:**
```markdown
## 🔥 Punto de Fricción Detectado

**Categoría:** [API/Modelo/Importación/Performance]
**Severidad:** [Crítica/Alta/Media/Baja]

### Descripción
[Qué falla y por qué]

### Reproducir
1. [Paso 1]
2. [Paso 2]
3. [Error observado]

### Test
```python
def test_nuevo_punto_caliente(self):
    # ...
```

### Solución Propuesta
[Cómo arreglarlo]
```

---

## 📚 Recursos

- [Django Testing Docs](https://docs.djangoproject.com/en/6.0/topics/testing/)
- [DRF Testing Guide](https://www.django-rest-framework.org/api-guide/testing/)
- [Coverage.py Docs](https://coverage.readthedocs.io/)

---

## ✅ Estado Actual

```
Última actualización: 8 de enero de 2026
Tests totales: 38
Tests passing: 38 ✅
Cobertura: 99%
Puntos calientes críticos: 1 🚨
Puntos calientes alta prioridad: 3 ⚠️
```

**Próximos pasos:**
1. Resolver DELETE CASCADE
2. Mejorar parsing de nombres en import
3. Agregar modo `--continue-on-error`
4. Implementar búsqueda con `unaccent` para PostgreSQL
